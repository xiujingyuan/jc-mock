$(function(){

    $.each($("#program_sel div"), function (i, item) {
        $(item).change(function () {
            var program_id_name = $(item).attr("id").split("_");
            var program_id = program_id_name[program_id_name.length - 1];
            update_program_info(program_id);
            update_program_table_info(program_id);
        });
    });

    $("#sel_coverage_program").change(function () {
        init_table();
    });

    $(window).resize(function (){
        setTabContent();
    });

    // $('a[data-toggle="tab"]').on('show.bs.tab', function(e) {
    //     var href = $(this).attr("href");
    //     clear_iter();
    //     if(href.indexOf("_") == -1){
    //         var program_id = href.replace("#tab", "");
    //         $("#total_time").addClass("hidden");
    //         $("#child_time_" + program_id).removeClass("hidden");
    //     }
    //     else{
    //         $("#total_time").removeClass("hidden");
    //     }
    // });
    set_select_width();
});

function get_current_id() {
    var id = 0;
    $.each($("#myTab li"), function (index, item) {
        if($(item).hasClass("active")){
            var href = $(item).children().attr("href");
            if(href.indexOf("index") > 0){
                id = -1
            }
        else{
            id = href.replace("#tab", "");
            }
        }
    });
    console.log("id ", id);
    return id
}

function set_select_width() {
    $.each(program_list, function (i, item) {
        $("#sel_program_time_" + item).selectpicker({"width": 140});
    })
}

function clear_iter() {
    $.each(program_list, function (i, item) {
        $("#child_time_" + item).addClass("hidden");
    })
}

function setTabContent(){
    $(".report-content").css('height', $(window).height() - 100);
    var item_width =  Math.floor($(".report-content").width() / 12),
        real_width = 100;
    if(item_width > 100){
        real_width = item_width;
    }
    $(".item").css('width', real_width);
}

setTabContent();

function init_git_commit_table(program) {
    $("#tb_git_commit_" + program).bootstrapTable("destroy");
    var query_time = $("#sel_total_time_start input").val(),
        query_time_end = $("#sel_total_time_end input").val();
    var get_url = '/api/statistics_report/commit/program/' + program + "/" + query_time + "/" + query_time_end;
    $.ajax({
        url: get_url,
        type: "GET",
        success: function (data) {
            if (data.code == 0) {
                // toastr.success("获取需求/缺陷/日构建月统计成功", 'success');
                console.log("program commit ", data);
                var git_commit_table = GitCommitTableInit($("#tb_git_commit_" + program), data.data);
                git_commit_table.Init();
                // showSonarInfo(data.rows);
                // $(".bootstrap-table").addClass("col-md-6")
            }
            else {
                toastr.error("获取提交统计失败", 'fail');
            }
        }
    });

}

function show_program_info(program_id){
    update_program_info(program_id);
    init_program_coverage_table(program_id);
    init_program_sonar_table(program_id);
    init_git_commit_table(program_id);
};

function update_program_table_info(program_id) {
    update_program_info(program_id);
    init_program_coverage_table(program_id);
    init_program_sonar_table(program_id);
    init_git_commit_table(program_id);
}

function update_program_info(item) {

    var query_time = $("#sel_total_time_start input").val(),
        query_time_end = $("#sel_total_time_end input").val();
    var get_url = '/api/statistics_report/iteration/program/' + item + "/" + query_time + "/" + query_time_end;
    $.ajax({
    url: get_url,
    type: "GET",
    success: function (data) {
        if (data.code == 0) {
            // toastr.success("获取需求/缺陷/日构建月统计成功", 'success');
            // api/statistics_report/iteration/program/15/2020-05-10/2020-05-11
            $("#story_close_a_" + item).text(data.data.story.story_close);
            $("#story_close_a_" + item).attr("href", data.data.story.close_url);
            $("#story_total_a_" + item).text(data.data.story.story_total);
            $("#story_total_a_" + item).attr("href", data.data.story.total_url);
            $("#bug_close_a_" + item).text(data.data.bug.bug_close);
            $("#bug_close_a_" + item).attr("href", data.data.bug.close_url);
            $("#bug_total_a_" + item).text(data.data.bug.bug_total);
            $("#bug_total_a_" + item).attr("href", data.data.bug.total_url);
            $("#online_bug_closed_a_" + item).text(data.data.online_bug.bug_close);
            $("#online_bug_closed_a_" + item).attr("href", data.data.online_bug.close_url);
            $("#online_bug_total_a_" + item).text(data.data.online_bug.bug_total);
            $("#online_bug_total_a_" + item).attr("href", data.data.online_bug.total_url);

            $("#test_plan_close_a_" + item).text(data.data.test_plan.test_plan_close);
            $("#test_plan_close_a_" + item).attr("href", data.data.test_plan.close_url);
            $("#test_plan_total_a_" + item).text(data.data.test_plan.test_plan_total);
            $("#test_plan_total_a_" + item).attr("href", data.data.test_plan.total_url);
        }
        else {
            toastr.error("获取项目信息失败", 'fail');
        }
    }
});
}

function init_program_coverage_table(program) {
    console.log("init_program_coverage_table", program);
    $('#tb_program_coverage_month_' + program).bootstrapTable("destroy");
    var query_time = $("#sel_total_time_start input").val(),
        query_time_end = $("#sel_total_time_end input").val();
    var get_url = '/api/statistics_report/coverage/program/' + program + "/" + query_time + "/" + query_time_end;
    $.ajax({
        url: get_url,
        type: "GET",
        success: function (data) {
            if (data.code == 0) {
                console.log("program coverage", data);
                // toastr.success("获取需求/缺陷/日构建月统计成功", 'success');
                $("#average_coverage_" + program).text(data.average_coverage + "%");
                $("#branch_count_" + program).text(data.branch_count);
                $("#miss_count_" + program).text(data.miss_count);
                $("#change_code_" + program).text(data.change_code);
                var coverage_table = CoverageTableInit($('#tb_program_coverage_month_' + program), data.data);
                coverage_table.Init();
            }
            else {
                toastr.error("获取覆盖率统计失败", 'fail');
            }
        }
    });


}


function init_program_sonar_table(program) {
    $('#tb_sonar_' + program).bootstrapTable("destroy");
    var query_time = $("#sel_total_time_start input").val(),
        query_time_end = $("#sel_total_time_end input").val();
    var get_url = '/api/statistics_report/sonar/program/' + program + "/" + query_time + '/' + query_time_end;
    $.ajax({
        url: get_url,
        type: "GET",
        success: function (data) {
            if (data.code == 0) {
                // toastr.success("获取需求/缺陷/日构建月统计成功", 'success');
                // var sonar_data = new Array();
                // $.each(data.rows, function (i, data) {
                //     if(data.program_id == program){
                //         sonar_data.push(data);
                //     }
                // });
                // var sonar_table = SonarTableInit($('#tb_sonar_' + program), sonar_data);
                var sonar_table = SonarTableInit($('#tb_sonar_' + program), data.data);
                sonar_table.Init();
                showProgramSonarInfo(data.data, program)
                // showSonarInfo(data.rows);
                // $(".bootstrap-table").addClass("col-md-6")
            }
            else {
                toastr.error("获取代码质量统计失败", 'fail');
            }
        }
    });
}


function showSonarInfo(data) {
    var all_content = "";
    for(var sonar in data){
        all_content += generate_div(data[sonar], sonar);
    }
    $("#sonar_list").html("");
    $("#sonar_list").html(all_content);
}

function showProgramSonarInfo(data, program) {
    var all_content = "";
    for(var sonar in data){
        all_content += generate_div(data[sonar], sonar);
    }
    $("#sonar_list_" + program).html("");
    $("#sonar_list_" + program).html(all_content);
}


function generate_div(data, index) {
    var div_content = "                     <div style=\"height: 103px; left: 0px; top: " + index * 123 + "px; margin-bottom: 15px;width: 100%;background: #9e9e9e;\">\n" +
        "                                    <div class=\"boxed-group project-card\" data-key=\"" + data["sonar_program_name"] + "\" style=\"height: 103px;\">\n" +
        "                                        <div class=\"boxed-group-header clearfix\">\n" +
        "                                            <div class=\"project-card-header\">\n" +
        "                                                <h2 class=\"project-card-name\">" + data["sonar_program_name"] + "</h2>\n" +
        "                                                <div class=\"project-card-quality-gate big-spacer-left\">\n" +
        "                                                    <div class=\"project-card-measure-inner\">\n" +
        //"                                                        <span class=\"level level-OK level-small\"></span>\n" +
        "                                                    </div>\n" +
        "                                                </div>\n" +
        "                                                <div class=\"project-card-header-right\"></div>\n" +
        "                                            </div>\n" +
        "                                            <div class=\"project-card-dates note text-right\">\n" +
        "                                                <span class=\"big-spacer-left\">最新更新时间:" + data["sonar_branch_time"] + "</span>" +
        "                                                <span class=\"big-spacer-left\">分支名:" + data["sonar_branch"] + "</span>\n" +
        "                                            </div>\n" +
        "                                        </div>\n" +
        "                                        <div class=\"boxed-group-inner\">\n" +
        "                                            <div class=\"project-card-measures\">\n";
    // reliability_rating
    div_content += "<div class=\"project-card-measure\" data-key=\"reliability_rating\">" +
        "<div class=\"project-card-measure-inner\"><div class=\"project-card-measure-number\">" +
        "<span class=\"spacer-right\">" + data["sonar_bugs"] + "</span><span class=\"rating rating-" + data["sonar_reliability_rating"] +"\">" + data["sonar_reliability_rating"] + "</span></div>" +
        "<div class=\"project-card-measure-label-with-icon\">" +
        "<svg class=\"little-spacer-right vertical-bottom\" height=\"16\" version=\"1.1\" viewBox=\"0 0 16 16\" width=\"16\" xml:space=\"preserve\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" style=\"fill-rule: evenodd; clip-rule: evenodd; stroke-linejoin: round; stroke-miterlimit: 1.41421;\">" +
        "<path d=\"M11 9h1.3l.5.8.8-.5-.8-1.3H11v-.3l2-2.3V3h-1v2l-1 1.2V5c-.1-.8-.7-1.5-1.4-1.9L11 1.8l-.7-.7-1.8 1.6-1.8-1.6-.7.7 1.5 1.3C6.7 3.5 6.1 4.2 6 5v1.1L5 5V3H4v2.3l2 2.3V8H4.2l-.7 1.2.8.5.4-.7H6v.3l-2 1.9V14h1v-2.4l1-1C6 12 7.1 13 8.4 13h.8c.7 0 1.4-.3 1.8-.9.3-.4.3-.9.2-1.4l.9.9V14h1v-2.8l-2-1.9V9zm-2 2H8V6h1v5z\" style=\"fill: currentcolor;\"></path>" +
        "</svg>Bugs</div></div></div>";
    //security_rating
    div_content += "<div class=\"project-card-measure\" data-key=\"security_rating\">" +
        "<div class=\"project-card-measure-inner\"><div class=\"project-card-measure-number\">" +
        "<span class=\"spacer-right\">" + data["sonar_vulnerabilities"] + "</span><span class=\"rating rating-" + data["sonar_security_rating"] + "\">" + data["sonar_security_rating"] + "</span></div>" +
        "<div class=\"project-card-measure-label-with-icon\">" +
        "<svg class=\"little-spacer-right vertical-bottom\" height=\"16\" version=\"1.1\" viewBox=\"0 0 16 16\" width=\"16\" xml:space=\"preserve\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" style=\"fill-rule: evenodd; clip-rule: evenodd; stroke-linejoin: round; stroke-miterlimit: 1.41421;\">" +
        "<path d=\"M10.8 5H6V3.9a2.28 2.28 0 0 1 2-2.5 2.22 2.22 0 0 1 1.8 1.2.48.48 0 0 0 .7.2.48.48 0 0 0 .2-.7A3 3 0 0 0 8 .4a3.34 3.34 0 0 0-3 3.5v1.2a2.16 2.16 0 0 0-2 2.1v4.4a2.22 2.22 0 0 0 2.2 2.2h5.6a2.22 2.22 0 0 0 2.2-2.2V7.2A2.22 2.22 0 0 0 10.8 5zm-2.2 5.5v1.2H7.4v-1.2a1.66 1.66 0 0 1-1.1-1.6A1.75 1.75 0 0 1 8 7.2a1.71 1.71 0 0 1 .6 3.3z\" style=\"fill: currentcolor;\"></path>" +
        "</svg>Vulnerabilities</div></div></div>";

    //sqale_rating
    div_content += "<div class=\"project-card-measure\" data-key=\"sqale_rating\">" +
        "<div class=\"project-card-measure-inner\"><div class=\"project-card-measure-number\">" +
        "<span class=\"spacer-right\">" + data["sonar_code_smells"] + "</span><span class=\"rating rating-" + data["sonar_sqale_rating"] + "\">" + data["sonar_sqale_rating"] + "</span></div>" +
        "<div class=\"project-card-measure-label-with-icon\">" +
        "<svg class=\"little-spacer-right vertical-bottom\" height=\"16\" version=\"1.1\" viewBox=\"0 0 16 16\" width=\"16\" xml:space=\"preserve\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" style=\"fill-rule: evenodd; clip-rule: evenodd; stroke-linejoin: round; stroke-miterlimit: 1.41421;\">" +
        "<path d=\"M8 2C4.7 2 2 4.7 2 8s2.7 6 6 6 6-2.7 6-6-2.7-6-6-6zm-.5 5.5h.9v.9h-.9v-.9zm-3.8.2c-.1 0-.2-.1-.2-.2 0-.4.1-1.2.6-2S5.3 4.2 5.6 4c.2 0 .3 0 .3.1l1.3 2.3c0 .1 0 .2-.1.2-.1.2-.2.3-.3.5-.1.2-.2.4-.2.5 0 .1-.1.2-.2.2l-2.7-.1zM9.9 12c-.3.2-1.1.5-2 .5-.9 0-1.7-.3-2-.5-.1 0-.1-.2-.1-.3l1.3-2.3c0-.1.1-.1.2-.1.2.1.3.1.5.1s.4 0 .5-.1c.1 0 .2 0 .2.1l1.3 2.3c.2.2.2.3.1.3zm2.5-4.1L9.7 8c-.1 0-.2-.1-.2-.2 0-.2-.1-.4-.2-.5 0-.1-.2-.3-.3-.4-.1 0-.1-.1-.1-.2l1.3-2.3c.1-.1.2-.1.3-.1.3.2 1 .7 1.5 1.5s.6 1.6.6 2c0 0-.1.1-.2.1z\" style=\"fill: currentcolor;\"></path>" +
        "</svg>Code Smells</div></div></div>";

    //coverage
    div_content += "<div class=\"project-card-measure\" data-key=\"coverage\">" +
        "<div class=\"project-card-measure-inner\"><div class=\"project-card-measure-number\">" +
        "<span class=\"spacer-right\"><svg class=\"donut-chart\" height=\"24\" width=\"24\">" +
        "<g transform=\"translate(0, 0)\"><g transform=\"translate(12, 12)\"><path d=\"M7.347880794884119e-16,-12L5.51091059616309e-16,-9Z\" style=\"fill: rgb(0, 170, 0);\"></path>" +
        "<path d=\"M7.347880794884119e-16,-12A12,12,0,1,1,-7.347880794884119e-16,12A12,12,0,1,1,7.347880794884119e-16,-12M6.3403325984522e-15,-9A9,9,0,1,0,-6.3403325984522e-15,9A9,9,0,1,0,6.3403325984522e-15,-9Z\" style=\"fill: rgb(212, 51, 63);\"></path></g></g></svg></span>" +
        "<span>" + data["sonar_coverage"] + "%</span></div><div class=\"project-card-measure-label\">Coverage</div></div>" +
        "</div>";

    //duplicated_lines_density
    div_content += "<div class=\"project-card-measure\" data-key=\"duplicated_lines_density\">" +
        "<div class=\"project-card-measure-inner\"><div class=\"project-card-measure-number\">" +
        "<span class=\"spacer-right\"><div class=\"duplications-rating duplications-rating-E\"></div></span>" +
        "<span>" + data["sonar_duplicated_lines_density"] + "%</span></div>" +
        "<div class=\"project-card-measure-label\">Duplications</div></div></div>";

    div_content += "                                   </div>\n" +
    "                                        </div>\n" +
    "                                    </div>\n" +
    "                                </div>";
    return div_content;
}

function get_data(day) {
    var nowDate = new Date(new Date().toLocaleDateString()),//获取当前时间
        date = new Date();
    if(day != 0){
        date = new Date(nowDate.getTime()+24*60*60* 1000 * day);
    }
    return date
}

function init_table() {
    $("#tb_program_coverage_month").bootstrapTable("destroy");
    var query_time = $("#sel_total_time_start input").val(),
        query_time_end = $("#sel_total_time_end input").val();
    var get_url = '/api/statistics_report/coverage/' + query_time + "/" + query_time_end;
    $.ajax({
        url: get_url,
        type: "GET",
        success: function (data) {
            if (data.code == 0) {
                // toastr.success("获取需求/缺陷/日构建月统计成功", 'success');
                console.log("coverage data :", data.data);
                var coverage = new Array();
                $.each(data.data,function (index, item) {
                    if(item["organization"] == organization){
                        coverage.push(item);
                    }
                });
                var coverage_table = CoverageTotalTableInit($("#tb_program_coverage_month"), coverage);
                coverage_table.Init();
                // $(".bootstrap-table").addClass("col-md-6")
            }
            else {
                toastr.error("获取覆盖率统计失败", 'fail');
            }
        }
    });
}

function init_sonar_table(program_list, organization) {
    $("#tb_sonar").bootstrapTable("destroy");
    var query_time = $("#sel_total_time_start input").val(),
        query_time_end = $("#sel_total_time_end input").val();
    var get_url = '/api/statistics_report/sonar/' + query_time + "/" + query_time_end;
    $.ajax({
        url: get_url,
        type: "GET",
        success: function (data) {
            if (data.code == 0) {
                console.log("data", data);
                var sonar = new Array();
                $.each(data.data, function (index, item) {
                    if(item["organization"] == organization){
                        sonar.push(item);
                    }
                });
                var sonar_table = SonarTableInit($("#tb_sonar"), sonar);
                sonar_table.Init();
                showSonarInfo(sonar);
                // $(".bootstrap-table").addClass("col-md-6")
            }
            else {
                toastr.error("获取代码质量统计失败", 'fail');
            }
        }
    });

}

<!--月需求，缺陷和构建统计-->
function init_story_bug_build_month_data(program_list) {
    var query_time = $("#sel_total_time_start input").val(),
        query_time_end = $("#sel_total_time_end input").val();
    var query_time_list = query_time_end.split("-"),
        year = query_time_list[0],
        month = query_time_list[1];
    var get_url = "/api/statistics_report/story_bug_build/" + query_time + "/" + query_time_end;
    $.ajax({
        url: get_url,
        type: "GET",
        success: function (data) {
            if (data.code == 0) {
                // toastr.success("获取需求/缺陷/日构建月统计成功", 'success');
                console.log("获取需求：", data.data);
                showStoryBugBuildMonth(data.data, year, month, program_list);
            }
            else {
                toastr.error("获取需求/缺陷/日均构建数统计失败", 'fail');
            }
        }
    });
}

function showStoryBugBuildMonth(data, year, month, program_list) {
    var main = echarts.init(document.getElementById("story_bug_build_month"));
    $('.panel-body').resize(function(){
        main.resize();
    });
    var mainOption = getStoryBugBuildOption(year, month);
    for(var i = 0;i < data.length;i++){
        if($.inArray(data[i].program_id, program_list) > -1){
            mainOption.xAxis.data.push(data[i].program_name);
            mainOption.series[0].data.push(data[i].story_publish);
            mainOption.series[1].data.push(data[i].bug_created);
            mainOption.series[2].data.push(data[i].build_average);
        }
    }
    main.setOption(mainOption);
}

function getStoryBugBuildOption(year, month) {
    // 指定图表的配置项和数据
    var option = {
        title: {
        },
        color: ["#24a4f8", "#56bc43", "#9018c8"],
        tooltip: {},
        legend: {
            data:['已完成需求', '缺陷数', '日均构建数'],
            x: 'center',
            y: 'bottom'
        },
        xAxis: {
            data: []
        },
        yAxis: {},
        series: [{
            name: '已完成需求',
            type: 'bar',
            data: [],
            itemStyle: {
                normal: {
                    label: {
                        show: true, //开启显示
                        position: 'inside', //在上方显示
                        textStyle: { //数值样式
                            color: 'white',
                            fontSize: 16
                        }
                    }
                }
            },
        }, {
            name: '缺陷数',
            type: 'bar',
            data: [],
            itemStyle: {
                normal: {
                    label: {
                        show: true, //开启显示
                        position: 'inside', //在上方显示
                        textStyle: { //数值样式
                            color: 'white',
                            fontSize: 16
                        }
                    }
                }
            },
        },{
            name: '日均构建数',
            type: 'bar',
            data: [],
            itemStyle: {
                normal: {
                    label: {
                        show: true, //开启显示
                        position: 'inside', //在上方显示
                        textStyle: { //数值样式
                            color: 'white',
                            fontSize: 16
                        }
                    }
                }
            },
        }]
    };
    return option
}

<!--上线情况统计-->
function init_tag_online_month_data(program_list) {
    var query_time = $("#sel_total_time_start input").val(),
        query_time_end = $("#sel_total_time_end input").val(),
        query_time_list = query_time_end.split("-"),
        year = query_time_list[0],
        month = query_time_list[1],
        organization = $("#myTabContent").find("div").attr("id").split("_"),
        organization_id = organization[organization.length - 1];
    var get_url = "/api/statistics_report/tag_online_bug/" + query_time + "/" + query_time_end;
    $.ajax({
        url: get_url,
        type: "GET",
        success: function (data) {
            if (data.code == 0) {
                // toastr.success("获取需求/缺陷/日构建月统计成功", 'success');
                console.log("上线情况：", data.data);
                showTagOnlineMonth(data.data, year, month, program_list);
            }
            else {
                toastr.error("获取上线次数，线上BUG统计失败", 'fail');
            }
        }
    });
}

function showTagOnlineMonth(data, year, month, program_list) {
    var main = echarts.init(document.getElementById("tag_online_month"));
    $('.panel-body').resize(function(){
        main.resize();
    });
    var mainOption = getTagOnlineOption(year, month);
    for(var i = 0;i < data.length;i++){
        if($.inArray(data[i].program_id, program_list) > -1) {
            mainOption.xAxis.data.push(data[i].program_name);
            mainOption.series[0].data.push(data[i].tag_created);
            mainOption.series[1].data.push(data[i].online_bug_created);
        }
    }
    main.setOption(mainOption);
}

function getTagOnlineOption(year, month) {
    // 指定图表的配置项和数据
    var option = {
        color: ["#56bc43", "#d414cd"],
        tooltip: {},
        legend: {
            data:['上线次数', '线上BUG'],
            x: 'center',
            y: 'bottom'
        },
        xAxis: {
            data: []
        },
        yAxis: {},
        series: [{
            name: '上线次数',
            type: 'bar',
            data: [],
            itemStyle: {
                normal: {
                    label: {
                        show: true, //开启显示
                        position: 'inside', //在上方显示
                        textStyle: { //数值样式
                            color: 'white',
                            fontSize: 16
                        }
                    }
                }
            },
        },{
            name: '线上BUG',
            type: 'bar',
            data: [],
            itemStyle: {
                normal: {
                    label: {
                        show: true, //开启显示
                        position: 'inside', //在上方显示
                        textStyle: { //数值样式
                            color: 'white',
                            fontSize: 16
                        }
                    }
                }
            },
        }]
    };
    return option
}

var CoverageTableInit = function (item, data) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $(item).bootstrapTable({
            data: data,
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            paginationPreText:"上一页",
            paginationNextText:"下一页",
            pageSize: 50,                       //每页的记录行数（*）
            pageList: [50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: false,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: false,                //是否启用点击选中行
            //height: 700,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                field: 'git_name',
                title: 'git项目名',
                align:'center'
            }, {
                field: 'merge_time',
                title: 'merge日期',
                align:'center',
                visible: true,
            }, {
                field: 'static_time',
                title: '提测日期',
                align: 'center',
                visible: true,
            }, {
                field: 'publish_time',
                title: '发布日期',
                align: 'center',
                visible: true,
            }, {
                field: 'publish_week',
                title: '本月周',
                align: 'center',
                visible: true,
            }, {
                field: 'coverage_branch',
                title: '分支',
                align:'left'
            }, {
                field: 'story_name',
                title: '需求',
                align: 'left',
                formatter:function (value, row, index) {
                    if(row["static_time"] == "未统计分支"){
                        return ""
                    }
                    else{
                        return "<a class='table_story_name' href='" + row["story_url"] + "' target='_blank'>" + row["story_name"] + "</a>"
                    }
                }
            }, {
                field: 'coverage_logic',
                title: '逻辑覆盖率',
                align:'center',
                formatter:function (value, row, index) {
                    if(row["static_time"] != "未统计分支"){
                        //return (value * 100).toFixed(2) + "%"
                        return "<a class='table_story_name' href='" + row["coverage_url"] + "' target='_blank'>" + value  + "%" + "</a>"
                    }
                    else{
                        return ""
                    }
                }
            }, {
                field: 'change_code',
                title: '代码变更',
                align:'center'
            }],
        });
    };

    return oTableInit;
};

var CoverageTotalTableInit = function (item, data) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $(item).bootstrapTable({
            data: data,
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            paginationPreText:"上一页",
            paginationNextText:"下一页",
            pageSize: 50,                       //每页的记录行数（*）
            pageList: [50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: false,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: false,                //是否启用点击选中行
            //height: 700,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                field: 'program_name',
                title: '统计时间',
                align: 'center',
                visible: true,
                formatter: function (value, row , index) {
                        var query_time = $("#sel_total_time_start input").val(),
                            query_time_end = $("#sel_total_time_end input").val();
                        return query_time + " 至 " + query_time_end
                }
            }, {
                field: 'program_name',
                title: '所属系统',
                align: 'center',
                visible: true,
            }, {
                field: 'branch_count',
                title: '测试覆盖分支数',
                align: 'center',
                visible: true,
            }, {
                field: 'miss_count',
                title: '未统计覆盖分支',
                align: 'center',
                visible: true,
            }, {
                field: 'average_coverage',
                title: '平均覆盖率',
                align:'left',
                formatter: function (value, row , index) {
                    return value + '%'
                }
            }, {
                field: 'total_add_lines',
                title: '代码新增总行数',
                align: 'left'
            }, {
                field: 'total_del_lines',
                title: '代码删除总行数',
                align: 'left'
            }, {
                field: 'total_commit_count',
                title: '总提交次数',
                align: 'left'
            }, {
                field: 'total_change_files',
                title: '代码变更总文件数',
                align: 'left'
            }, {
                field: 'change_code',
                title: '代码变更总行数',
                align: 'left',
                cellStyle:{
                　　　　css:{"color":"#b0d513"}
                　　},
                formatter: function(value, row, index){
                    return row["total_add_lines"] + row["total_del_lines"]
                }
            }]
        });
    };

    return oTableInit;
};

var SonarTableInit = function (item, data) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $(item).bootstrapTable({
            data: data,
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            paginationPreText:"上一页",
            paginationNextText:"下一页",
            pageSize: 50,                       //每页的记录行数（*）
            pageList: [50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: false,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: false,                //是否启用点击选中行
            //height: 700,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                field: 'sonar_program_name',
                title: '系统名',
                align: 'center',
                formatter:function (value, row , index) {
                    return value + '<span class="rating rating-' + row["sonar_reliability_rating"] + '">' +
                        row["sonar_reliability_rating"] + '</span>'
                }
            }, {
                field: 'sonar_branch',
                title: '最新分支',
                align: 'left',

            }, {
                field: 'sonar_bugs',
                title: 'Bugs',
                align: 'center'
            }, {
                field: 'sonar_duplicated_blocks',
                title: '重复块',
                align: 'center'
            }, {
                field: 'sonar_vulnerabilities',
                title: '漏洞',
                align: 'center',
            }, {
                field: 'sonar_code_smells',
                title: '坏味道',
                align: 'center',
            }, {
                field: 'sonar_duplicated_lines_density',
                title: ' 重复度',
                align: 'center',
                formatter: function (value, row, index) {
                    if(value == "" || value == null){
                        return "0%";
                    }
                    else{
                        return value.toFixed(2) + "%";
                    }
                }
            },{
                field: 'sonar_branch_time',
                title: '最新更新时间',
                align: 'center',
            }],
        });
    };

    return oTableInit;
};


var GitCommitTableInit = function (item, data) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $(item).bootstrapTable({
            data: data,
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            paginationPreText:"上一页",
            paginationNextText:"下一页",
            pageSize: 50,                       //每页的记录行数（*）
            pageList: [50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: false,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: false,                //是否启用点击选中行
            //height: 700,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                field: 'source_branch',
                title: '分支名',
                align: 'left',
                visible: true,
            }, {
                field: 'git_commit_count',
                title: '提交次数',
                align: 'left',

            }, {
                field: 'git_add_lines',
                title: '新增行数',
                align: 'center'
            }, {
                field: 'git_remove_lines',
                title: '删除行数',
                align: 'center',
            }, {
                field: 'git_changed_file',
                title: '修改文件数',
                align: 'center',
            }],
        });
    };

    return oTableInit;
};
