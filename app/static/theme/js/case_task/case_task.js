$(function () {
    var oTable = new TableInit();
    oTable.Init();
    //2.初始化Button的点击事件
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();

    $('#myTab a:first').tab('show');

    $("#btn_create_list").click(function () {
        $("#bootstrap-duallistbox-nonselected-list_duallistbox_case_all").addClass("duallistbox_height");
        $("#bootstrap-duallistbox-selected-list_duallistbox_case_all").addClass("duallistbox_height");
    })

    get_task_env();

    $('#myTab a:first').tab('show');

    var href = get_cache("auto_exec"),
        program = get_cache("auto_exec_program");

    $("#tab_task_list").on("shown.bs.tab", function (e) {
        $("#tb_task_list").bootstrapTable("refresh");
    });

    $(".case_task_header_ul.dropdown-menu a").click(function () {
        var sel_str = $("#dropdownMenu1").html(),
            display_str = $(this).html();
        if(sel_str.indexOf(display_str) <= -1){
            $("#dropdownMenu1").html('<i class="case_task_header_i fa fa-link"></i>' + display_str +
                '                <span class="caret"></span>');
            setTimeout(function () {
            $("#tb_task_list").bootstrapTable("refresh");
        }, 100);
        }
    });

    $(".case_task_program li").click(function () {
        $(".case_task_program li").removeClass("active");
        $(this).addClass("active");
        var pro_list = $(this).find("a").attr("id").split("_"),
                pro = pro_list[pro_list.length - 1];
        save_cache("auto_exec_program", pro);
        setTimeout(function () {
            $("#tb_task_list").bootstrapTable("refresh");
        }, 100);

    });

    if (!$.isEmptyObject(program)){
        $.each($(".case_task_program li"), function () {
            var pro_list = $(this).find("a").attr("id").split("_"),
                pro = pro_list[pro_list.length - 1];
            if(pro == program){
                $(this).addClass("active")
                $("#tb_task_list").bootstrapTable("refresh");
            }
            else{
                $(this).removeClass("active")
            }
        });
    }

    if (!$.isEmptyObject(href)){
        setTimeout(function () {
        $.ajax({
            type: "GET",
            url: "/api/task/detail/" + href,
            contentType: "application/json; charset=UTF-8",
            success: function (data) {
                if (data.code != 0) {
                    toastr.error("error", "程序发生异常，请求联系管理员");
                    return;
                }
                else{
                    $("#tab_task_detail").click(function () {
                        $("#input_task_id").val(href);
                        $("#task_id_number").val(href);
                        getRunList(1);
                        refresh_task_detail(data);
                        $(this).tab('show').unbind('click');
                    }).click();
                    setTimeout(function () {
                        $("#btn_exec").click();
                        // window.location.search = ""
                    }, 100);
                }
            }
        });
    }, 100);
        save_cache("auto_exec", "")
    }

    $(window).resize(function (){
        var page_height = $(window).height();
        $('#tb_task_list').bootstrapTable('resetView',{ height: page_height - 150 } );
        $('.log_div').css('height', page_height - 510);
        $.each($("#myTabContent table"), function (i, item) {
            if($(item).attr("id") != "tb_task_list"){
                if($(item).bootstrapTable("getOptions").totalRows == 0){
                    $(item).bootstrapTable('resetView',{ height: page_height - 540 } );
                }else{
                    $(item).bootstrapTable('resetView',{ height: page_height - 540 } );
                }
            }
        });

    });

    //初始化
    // initListBox('', '', 'case_all');
    //setTimeout(function () {
    //    var after = $("#sel_system_test").parent("div");
    //     $(after).parent().after(after).remove();
    //},1000);

    $("#sel_system_test").on("changed.bs.select", function (e) {
        refresh_business();
    });

    function refresh_business(){
        var system = $("#sel_system_test").val();
        var program_business = eval();
        $("#sel_belong_business").empty();
        var options = "<option value=''>全部</option>";
        $.each(program_business, function (key, val) {
           if(val.hasOwnProperty(system)){
               if(!$.isEmptyObject(val[system])){
                   for(var index in val[system]){
                       options += "<option value='" + val[system][index]["business_name"] + "'>" +
                       val[system][index]["business_cname"] + "</option>";
                   }
               }else{

               }
           }
        });
        $("#sel_belong_business").append(options);
        $("#sel_belong_business").selectpicker("refresh");
    }

    $("#btn_create_task").click(function () {
        var case_ids = $('[name="duallistbox_case_all"]').val();
        var task_title = $("#modal_txt_task_title").val();
        var task_system = $("#sel_system_test").val();
        var task_business = $("#sel_belong_business").val();
        if (! case_ids){
            toastr.error("用例不能为空", "error");
            return
        }

        if (! task_title){
            toastr.error("任务名称不能为空", "error");
            return
        }
        $(this).attr("disabled", "disabled");
        var paramData = {
            "task_title": task_title,
            "task_ids": case_ids,
            "task_system": task_system,
            "task_business": task_business,
            "task_create_user": current_user
        };

        $.ajax({
            url: '/api/task/create',
            headers: {"X-CSRFToken": csrf_token},
            contentType: "application/json; charset=UTF-8",
            type: 'post',
            data: JSON.stringify(paramData),
            async: true,
            success: function (data) {
                if (data["code"] == 1) {
                    toastr.error("error", data["msg"]);
                }
                else {
                    toastr.success("success", "创建成功");
                    $("#btn_create_task_cancel").click();
                    $("#tb_task_list").bootstrapTable("refresh");
                }
                $("#btn_create_task").removeAttr("disabled");
            },
            error: function (e) {
                toastr.warning("warning", e.msg);
                $("#btn_create_task").removeAttr("disabled");
            }
    });
    });

    $("#sel_system_test").on("changed.bs.select", function (e) {
        var parent = $("#duallistbox_case").parent();
        parent.html("").append('<select id="duallistbox_case" multiple="multiple" size="10" name="duallistbox_case_all" class="case_all">\n' +
            '                    </select>');
        initListBox($(this).val(), $("#sel_belong_business").val(), "case_all");

    });

    $("#sel_belong_business").on("changed.bs.select", function (e) {
        var parent = $("#duallistbox_case").parent();
        parent.html("").append('<select id="duallistbox_case" multiple="multiple" size="10" name="duallistbox_case_all" class="case_all">\n' +
            '                    </select>');
        initListBox($("#sel_system_test").val(), $(this).val(), "case_all");

    })

    $("#sel_system_test").val(get_cache("search_case_from_system"));
    $("#sel_system_test").selectpicker("refresh");
    refresh_business();
    setTimeout(function () {
        var parent = $("#duallistbox_case").parent();
        parent.html("").append('<select id="duallistbox_case" multiple="multiple" size="10" name="duallistbox_case_all" class="case_all">\n' +
            '                    </select>');
        initListBox($("#sel_system_test").val(), "", "case_all");
    },100);
});

/*初始化duallistbox*/
//queryParam1：参数
//selectClass：select元素class属性
//selectedDataStr：选中数据，多个以,隔开
function initListBox(program_id, business, selectClass, selectedDataStr) {
    var paramData = {
        'program_id': program_id,
        'business': business
    };
    if(program_id == ""){
        paramData["program_id"] = get_cache("search_case_from_system")
    }
    if(business == ""){
        business = get_cache("search_case_belong_business")
    }
    if(business == ""){
        paramData["business"] = $($("#sel_belong_business option")[1]).val()
    }
    else{
        paramData["business"] = business
    }
    $.ajax({
        url: '/api/case/all',
        type: 'get',
        async:false,
        data: paramData,
        success: function (returnData) {
            $(returnData["data"]).each(function () {
                var o = document.createElement("option");
                o.value = this['case_id'];
                o.text = this['case_name'];
                if ("undefined" != typeof (selectedDataStr) && selectedDataStr != "") {
                    var selectedDataArray = selectedDataStr.split(',');
                    $.each(selectedDataArray, function (i, val) {
                        if (o.value == val) {
                            o.selected = 'selected';
                            return false;
                        }
                    });
                }
                $("." + selectClass + "")[0].options.add(o);
            });
            //渲染dualListbox
            $('.' + selectClass + '').bootstrapDualListbox({
                nonSelectedListLabel: '待选择用例',
                infoText: "",
                filterPlaceHolder: "过滤",
                selectedListLabel: '已选择用例',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: true//,
                //nonSelectedFilter: 'ion ([7-9]|[1][0-2])'
            });
            $("#bootstrap-duallistbox-nonselected-list_duallistbox_case_all").addClass("duallistbox_height");
            $("#bootstrap-duallistbox-selected-list_duallistbox_case_all").addClass("duallistbox_height");
        },
        error: function (e) {
            console.log(e.msg);
        }
    });
}

function get_task_env(){
    var program_id = $("#task_system").val();
    $.ajax({
        url: "/api/build_task/get_env",
        type: "GET",
        data: {
            "branch": "",
            "program": program_id
        },
        dataType: "json",
        success: function (data) {
            if (data.code == 0) {
                $("#task_run_env").empty();
                for (var opt in data.data) {
                    $("#task_run_env").append('<option value="' + data.data[opt]["env_id"] + '">' + data.data[opt]["env_id"] + '</option>');
                }
                if ($("#task_run_env").find("option").length  == 0) {
                    $("#task_run_env").append('<option></option>');
                }
                $("#task_run_env").selectpicker("refresh");
                $("#task_run_env").selectpicker("render");
            }
        },
        error: function (data) {
            console.log("error", data);
        }
    });
}

function save_cache(key, value) {
    localStorage.setItem(key, value);
}

function get_cache(key) {
    return localStorage.getItem(key);
}

function getRunList(page) {
   var task_id = $("#task_id_number").val();
   //console.log("task_id", task_id);
   $.ajax({
       url: "/api/task/run/detail",
       type: "GET",
       data: {
           "page": page,
           "task_id": task_id
       },
       dataType: "json",
       success: function (data) {
           var totalPages;
           if (data.code == 0) {
            totalPages = data.total;
            var htm = "";
            var tab_htm = "";
            $.each(data.data, function(i, item) {
                htm += "<a href='#run_detail_" + i + "' class='list-group-item' data-toggle='tab'>";
                htm += item.run_begin + "</a>";
                if (i == 0){
                    tab_htm += '<div class="tab-pane active" id="run_detail_' + i +'" style="border: 1px solid #dddddd">\n' ;
                }
                else{
                    tab_htm += '<div class="tab-pane" id="run_detail_' + i +'" style="border: 1px solid #dddddd">\n';

                }

                tab_htm += '                <div id="progress_' + item.run_id + '">\n';

                if (item.run_status == 1){
                    //console.log("run_status", item, item.run_status);
                }
                else{
                    tab_htm +=    '                    <div class="my_progress"><div>\n' +
                    '                    <div class="nanobar" style="position: relative;">\n' +
                    '                        <div class="bar" style="width: 100%;"></div>\n' +
                    '                    </div>\n' +
                    '                </div>\n';
                    tab_htm +=
                    '                <div class="my_percent">100%</div>\n' +
                    '                <div class="log_div" style="overflow-y: auto;margin-top:10px;text-align:left">' +
                    '<pre style="text-align: left;background:white;border:0px;margin:0px;">' +
                    '' + item.run_result +'</div></pre>\n' ;
                }
                tab_htm +=
                    '            </div>\n' +
                    '            </div>\n' +
                    '            </div>'
            });
            $('#run_list').html(htm);
            $('#myTabContent').html(tab_htm);

            var page_height = $(window).height();
            set_log_height();


            var my_element = $('#pageLimit');
            var options = {
                bootstrapMajorVersion : 3,
                currentPage : page, // 当前页数
                numberOfPages : 5, // 显示按钮的数量
                totalPages : totalPages, // 总页数
                itemTexts : function(type, page, current) {
                    switch (type) {
                    case "first":
                        return "首页";
                    case "prev":
                        return "上一页";
                    case "next":
                        return "下一页";
                    case "last":
                        return "末页";
                    case "page":
                        return page;
                    }
                },
                // 点击事件，用于通过Ajax来刷新整个list列表
                onPageClicked : function(event, originalEvent, type, page) {
                    getRunList(page);
                }
            };
            my_element.bootstrapPaginator(options);
        }
           else{
               reset_run_log();
           }
    },
       error:function () {
        console.log("error");
    }
   });
}

$('#myTab a').click(function (e) {
    e.preventDefault();
    if($(this).attr("href") == "#task_list"){
        $(this).tab('show');
    }
});


function set_log_height() {
    $('.log_div').css('height', $(window).height() - 515);
}

var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    var page_scroll = $(window).height();
    oTableInit.Init = function () {
        $('#tb_task_list').bootstrapTable({
            url: '/api/task/all',         //请求后台的URL（*）
            method: 'GET',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            paginationPreText:"上一页",
            paginationNextText:"下一页",
            height: page_scroll - 150,
            pageSize: 20,                       //每页的记录行数（*）
            pageList: [20, 50, 100],        //可供选择的每页的行数（*）
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
                field: 'task_title',
                title: '任务名称',
                class: 'task_name_col',
                formatter: showNameFormatter,
                align: 'left'
            }, {
                field: 'task_last_user',
                title: '最后修改人',
                class: 'task_col_80',
                align: "center"
            }, {
                field: 'task_update_time',
                title: '更新时间',
                class: 'task_col_120',
                align: 'center'
            }, {
                field: 'task_last_run_time',
                title: '上次运行时间',
                class: 'task_col_120',
                formatter: change_run_time,
                align: 'center'
            },{
                field: 'task_last_result',
                title: '上次运行结果',
                class: 'task_col_80',
                formatter: change_last_status,
                align: 'center'
            },
                {
                field: 'task_status',
                title: '当前运行状态',
                class: 'task_col_80',
                formatter: change_status,
                align: 'center'
            },
                {
                field: 'task_run_time',
                title: '运行次数',
                class: 'task_col_80',
                align: 'center'
            },{
                field: 'operate',
                title: '操作',
                align:"center",
                class: 'task_col_80',
                events: operateEvents,
                formatter:OpFormatter,
                class: 'W120',
            }]
        });
    };
    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var program_id = $(".case_task_program_item.active a").attr("id").split("_"),
            id = program_id[program_id.length - 1],
            actor = current_user;
        console.log($("#dropdownMenu1").html().indexOf("所有的") > -1);
        if($("#dropdownMenu1").html().indexOf("所有的") > -1) {
            actor = "";
        }
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            txt_from_system: id,
            txt_actor: actor,
            //case_exec_group_priority: "main",
            page_index: (params.offset / params.limit) + 1,
            page_size: params.limit,
        };
        return temp;
    };
    return oTableInit;
};

function change_status(value, row, index) {
    var ret = "";
    if (value == "0"){
        ret = '空闲';
    }
    else if (value == "1" ){
        ret = "运行中";
    }
    else {
        ret = "未知状态";
    }
    return ret
}

function change_run_time(value, row, index) {
    var ret = "未运行";
    if(value){
        ret = value;
    }
    return ret
}

function change_last_status(value, row, index) {
    var ret = "未运行";
    if (parseInt(value) == 0){
        ret = '失败'
    }
    else if (parseInt(value)  == 1){
        ret = "成功"
    }
    else if (value) {
        ret = "未知状态"
    }
    return ret
}

function OpFormatter(value, row, index) {
            return [
                '<a class="task_detail" style="cursor: pointer" href="javascript:void(0)" id=' + row.task_id + ' title="详情">',
                '<span>详情</span>',
                '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
            ].join('');
        };

$("#btn_query").click(function () {
    $("#tb_task_list").bootstrapTable('selectPage', 1);
});

$(document).keydown(function (event) {
    if (event.keyCode == 13) {
        $('#btn_query').triggerHandler('click');
    }
});

$("#btn_reset").click(function () {
    $("#txt_task_title").val("");
    $("#txt_task_run_status").val("");
    $("#txt_task_des").val("");
    //$("#tb_case").bootstrapTable('refresh');
});

var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        //初始化页面上面的按钮事件
    };

    return oInit;
};
$("#btn_del").click(function () {
    var row = $.map($('#tb_task_list').bootstrapTable('getSelections'),function (row) {
                return row;
    });
    var case_ids = new Array();
    for(var i in row){
        case_ids.push(row[i]['case_id'])
    }

    var run_case=JSON.stringify({
        "case_ids":case_ids,
        "email":"{{ current_user.email }}"
    });

    $.ajax({
        type: "POST",
        headers: {"X-CSRFToken": "{{ csrf_token() }}"},

        url: "/api/case/run/case",
        contentType: "application/json; charset=UTF-8",
        data: run_case,
        success: function (data) {
            if (data.code != 0) {
                toastr.error("error", data.msg);
                return;
            }
            toastr.success("success", "执行请求已经发给后台任务执行，请检查邮箱"+"{{ current_user.email }}");
            $("#tb_task_list").bootstrapTable('remove', {
                field: 'case_id',
                values: [row['case_id']]
            });
        }
    });
});

function refresh_task_detail(data) {
    $("#task_detail input:text").each(function () {
        if ($(this).attr("id") == "task_status")
        {
            if (data["data"]["task_status"] == "0")
            {
                $(this).val("空闲");
            }
            else{
                $(this).val("运行中");
            }
        }
        else if ($(this).attr("id") =="task_last_result"){
            if (data["data"][$(this).attr("id")] == "0")
            {
                $(this).val("失败");
            }
            else{
                $(this).val("成功");
            }
        }
        else
        {
            $(this).val(data["data"][$(this).attr("id")]);
        }
    });

    $("#task_system").val(data["data"]["task_system"]);
    $("#task_system").selectpicker("refresh");

    refresh_business();

    setTimeout(function () {
        $("#task_business").val(data["data"]["task_business"]);
        $("#task_business").selectpicker("refresh");
        get_task_env();
        setTimeout(function () {
            var run_env = data["data"]["task_last_run_env"];
            if(run_env != "null"){
                $("#task_run_env").val(run_env);
                $("#task_run_env").selectpicker("refresh");
            }
        }, 200)

    }, 100);
}

function refresh_business(){
    console.log("task_system", $("#task_system").val(), get_cache("auto_exec_program"));
    $.ajax({
        url: "/api/case/program_business/" + $("#task_system").val(),
        type: "GET",
        success:function (data) {
            if(data.code == 0){
                $("#task_business").empty();
                var options = "<option value=''>全部</option>";
                for(var index in data.data){
                    options += "<option value='" + data.data[index]["business_name"] + "'>" +
                        data.data[index]["business_cname"] + "</option>";
                    }
                $("#task_business").append(options);
                $("#task_business").selectpicker("refresh");
            }
            else{
                $("#task_business").empty();
                $("#task_business").append("<option value=''>全部</option>");
                $("#task_business").selectpicker("refresh");
                toastr.warning("获取业务失败", 'warning');
            }
        },
        error:function () {
          toastr.error("获取业务异常", 'error');
          $("#task_business").empty();
          $("#task_business").append("<option value=''>全部</option>");
          $("#task_business").selectpicker("refresh");
        }
    })
}

function getRunList(page) {
   var task_id = $("#task_id_number").val();
   //console.log("task_id", task_id);
   $.ajax({
       url: "/api/task/run/detail",
       type: "GET",
       data: {
           "page": page,
           "task_id": task_id
       },
       dataType: "json",
       success: function (data) {
           var totalPages;
           if (data.code == 0) {
            totalPages = data.total;
            var htm = "";
            var tab_htm = "";
            var url = "";
            var run_id = 0;
            $.each(data.data, function(i, item) {
                if (i == 0){
                    htm += "<a href='#run_detail_" + i + "' class='list-group-item active'><input " +
                        "type='hidden' id='run_task_id_" + i + "' value='" + item.run_task_id + "'>";
                    htm += item.run_begin + "</a>";
                    tab_htm += '<div class="tab-pane active" id="run_detail_' + i +'">\n' ;
                }
                else{
                    htm += "<a href='#run_detail_" + i + "' class='list-group-item'><input " +
                        "type='hidden' id='run_task_id_" + i + "' value='" + item.run_task_id + "'>";
                    htm += "<input " +
                        "type='hidden' id='run_env_num" + i + "' value='" + item.run_env_num + "'>";
                    htm += item.run_begin + "</a>";

                    tab_htm += '<div class="tab-pane" id="run_detail_' + i +'">\n';

                }
                tab_htm += '<ul class="nav nav-tabs" id="runCaseTab'+ i + '" style="text-align: center;padding-left: 10px;">\n' +
                    '    <li class="active col-sm-1" style="padding: 0px;">\n' +
                    '        <a href="#case_content' + i + '">Case</a>\n' +
                    '    </li>\n' +
                    '    <li class="col-sm-1" style="padding: 0px;">\n' +
                    '        <a href="#myTabContent' + i + '">Log</a></li>\n' +
                    '</ul>\n' +
                    '<div class="tab-content" style="padding: 0px;">\n' +
                    '    <div class="tab-pane active" id="case_content' + i + '"><table id="tb_run_case'+ i + '"></table></div>\n' +
                    '    <div class="tab-pane" id="myTabContent' + i + '"  style="padding: 0px">';

                tab_htm += '                <div id="progress_' + item.run_id + '">\n';

                if (i == 0 && item.run_status == 1){
                    //console.log("run_status", item, item.run_status);
                    run_id = item.run_id;
                    url = ["/tasks/case_task_status/status/", item.run_task_id].join("");
                }
                else{
                    tab_htm +=    '                    <div class="my_progress"><div>\n' +
                    '                    <div class="nanobar" style="position: relative;">\n' +
                    '                        <div class="bar" style="width: 100%;"></div>\n' +
                    '                    </div>\n' +
                    '                </div>\n';
                    tab_htm +=
                    '                <div class="my_percent">100%</div>\n' +
                    '                <div class="log_div" style="overflow-y: auto;margin-top:10px;text-align:left">' +
                    '<pre style="text-align: left;background:white;border:0px;margin:0px;">' +
                    '' + item.run_result +'</div></pre>\n' ;
                }

                tab_htm += '</div>\n' +
                    '    </div>\n' +
                    '</div>';

                tab_htm +=
                    '            </div>\n' +
                    '            </div>\n' +
                    '            </div>'
            });

            $('#run_list').html(htm);
            $('#myTabContent').html(tab_htm);
            set_log_height();
            setTimeout(function () {

                $('#myTabContent a').click(function (e) {
                    $(this).tab('show');
                    set_log_height();
                });

                $.each($("#myTabContent table"), function (i, item) {
                    if (i == 0) {
                        var oTable = new RunCaseTableInit(item, data.data[i].task_id,
                            data.data[i].run_task_id, data.data[i].run_env_num);
                        oTable.Init();
                    }
                });

                // 启动查询
                if (run_id != 0){
                    get_run_logger(url, run_id);
                }

                $("#run_list a").on("click",function(){
                    $("#run_list a").removeClass("active");
                    $(this).addClass('active');

                    $("#myTabContent > div").removeClass("active");

                    var click_id = $(this).attr("href").replace("#", "");
                    $("#" + click_id).addClass("active");
                    var index = click_id.replace("run_detail_", "");
                    var item = $("#tb_run_case" + index);
                    var run_task_id = $("#run_task_id_" + index).val();
                    var run_env_num = $("#run_env_num" + index).val();
                    var task_id = $("#task_id_number").val();
                    var oTable = new RunCaseTableInit(item,
                        task_id,
                        run_task_id,
                        run_env_num);
                        oTable.Init();
                        set_log_height();

                });

            }, 100);

            var my_element = $('#pageLimit');
            var options = {
                bootstrapMajorVersion : 3,
                currentPage : page, // 当前页数
                numberOfPages : 5, // 显示按钮的数量
                totalPages : totalPages, // 总页数
                itemTexts : function(type, page, current) {
                    switch (type) {
                    case "first":
                        return "首页";
                    case "prev":
                        return "上一页";
                    case "next":
                        return "下一页";
                    case "last":
                        return "末页";
                    case "page":
                        return page;
                    }
                },
                // 点击事件，用于通过Ajax来刷新整个list列表
                onPageClicked : function(event, originalEvent, type, page) {
                    getRunList(page);
                }
            };
            my_element.bootstrapPaginator(options);
        }
           else{
               reset_run_log();
           }
    },
       error:function () {
        console.log("error");
    }
   });
}
function reset_run_log(){
    $("#pageLimit li").remove();
    $("#run_list a").remove();
    $("#myTabContent div").remove();
}

$('#myTab a').click(function (e) {
    e.preventDefault();
    if($(this).attr("href") == "#task_list"){
        $(this).tab('show');
    }
});

function showNameFormatter(value, row, index) {
    return "<div style='width:300px;text-overflow: ellipsis;overflow: hidden;'>" + value + "</div>"
}

function OpFormatter(value, row, index) {
            return [
                '<a class="task_detail" style="cursor: pointer" href="javascript:void(0)" id=' + row.task_id + ' title="详情">',
                '<span>详情</span>',

            ].join('');
        };

$("#btn_query").click(function () {
    $("#tb_task_list").bootstrapTable('selectPage', 1);
});

$(document).keydown(function (event) {
    if (event.keyCode == 13) {
        $('#btn_query').triggerHandler('click');
    }
});

$("#btn_reset").click(function () {
    $("#txt_task_title").val("");
    $("#txt_task_run_status").val("");
    $("#txt_task_des").val("");
    //$("#tb_case").bootstrapTable('refresh');
});

var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        //初始化页面上面的按钮事件
    };

    return oInit;
};
$("#btn_del").click(function () {
    var row = $.map($('#tb_task_list').bootstrapTable('getSelections'),function (row) {
                return row;
    });
    var case_ids = new Array();
    for(var i in row){
        case_ids.push(row[i]['case_id'])
    }

    var run_case = JSON.stringify({
        "case_ids":case_ids,
        "email":"{{ current_user.email }}"
    });

    $.ajax({
        type: "POST",
        headers: {"X-CSRFToken": "{{ csrf_token() }}"},
        url: "/api/case/run/case",
        contentType: "application/json; charset=UTF-8",
        data: run_case,
        success: function (data) {
            if (data.code != 0) {
                toastr.error("error", data.msg);
                return;
            }
            toastr.success("success", "执行请求已经发给后台任务执行，请检查邮箱"+"{{ current_user.email }}");
            $("#tb_task_list").bootstrapTable('remove', {
                field: 'case_id',
                values: [row['case_id']]
            });
        }
    });
});

window.operateEvents = {
    'click .task_detail': function (e, value, row, index) {
        $.ajax({
            type: "GET",
            url: "/api/task/detail/" + row['task_id'],
            contentType: "application/json; charset=UTF-8",
            success: function (data) {
                if (data.code != 0) {
                    toastr.error("error", "程序发生异常，请求联系管理员");
                    return;
                }
                else{
                    $("#tab_task_detail").click(function () {
                        $("#input_task_id").val(row['task_id']);
                        $("#task_id_number").val(row['task_id']);

                        getRunList(1);
                        refresh_task_detail(data);
                        $(this).tab('show').unbind('click');
                    }).click();
                }
            }
        });
    },

    'click .task_run': function (e, value, row, index) {
        var case_ids = new Array();
        case_ids.push(row['case_id']);

        var run_case=JSON.stringify({
            "task_id":case_ids,
            "email": "{{ current_user.email }}"
        });
        $.ajax({
            type: "POST",
            headers: {"X-CSRFToken": "{{ csrf_token() }}"},
            url: "/api/case/run/case",
            contentType: "application/json; charset=UTF-8",
            data:run_case,
            success: function (data) {

                if (data.code != 0) {
                    toastr.error("error", data.msg);
                    return;
                }
                toastr.success("success", "执行请求已经发给后台任务执行，请检查邮箱"+"{{ current_user.email }}");

            }
        });
    },

    'click .case_detail_info': function (e, value, row, index) {
        $("#tb_case_detail").bootstrapTable("destroy");
        var ocaseTable = new CaseDetailTable([row]);
        ocaseTable.Init();
        $("#tb_case_detail").bootstrapTable("refresh");
        $("#case_detail_info").modal("show");
    },

    'click .init_task': function (e, value, row, index) {
        console.log("init_task");
        $("#tb_case_init_detail").bootstrapTable("destroy");
        var ocaseTable = new CaseInitDetailTable(row["history_case_id"], row["build_id"]);
        ocaseTable.Init();
        $("#tb_case_init_detail").bootstrapTable("refresh");
        $("#case_init_detail_info").modal("show");
    },

    'click .pre_task': function (e, value, row, index) {
        $("#tb_case_pre_detail").bootstrapTable("destroy");
        var ocaseTable = new CasePreDetailTable(row["history_case_id"], row["build_id"]);
        ocaseTable.Init();
        $("#tb_case_pre_detail").bootstrapTable("refresh");

        $("#case_pre_detail_info").modal("show");
    },

    'click .edit_case': function (e, value, row, index) {
        var url = "/case/" + row["history_case_id"] + "/";
        window.open(url);
    },

};

var CaseDetailTable = function (row) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $("#tb_case_detail").bootstrapTable({
            data: row,
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
            pageSize: 1,                       //每页的记录行数（*）
            pageList: [1],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            rowStyle:rowStyle,
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
            columns: [
            {
                field: 'action',
                title: '执行动作',
                align:'left',
                class: 'json_style',
                formatter:showJson
            },
             {
                field: 'history_case_except_value',
                title: '期望结果',
                align:'left',
                class: 'json_style',
                formatter:showJson
            }, {
                field: 'history_case_actual_value',
                title: '实际结果',
                align:'left',
                class: 'json_style',
                formatter: showJson
            }, {
                field: 'history_case_result_info',
                title: '异常',
                align: "left",
                class: 'json_style',
                formatter: showJson
            }],
        });
    };

    function showJson(value, row, index, field) {
        var ret = '<div style="height:700px;overflow:auto;padding:0px;margin:0px;"><pre class="json_hover">' + JSON.stringify(value, null, 2) + "</pre></div>";
        //var ret = '<div style="padding:0px;margin:0px;"><pre class="json_hover">' + JSON.stringify(value, null, 2) + "</pre></div>";
        // var ret = JSON.stringify(value, null, 2);
        if (field == "history_case_vars" && row["history_case_result"] == 1){
            ret = "-"
        }
        return ret
    }

    function rowStyle(row, index) {
        if (row["history_case_result"] == 1) {
            return {
                classes: "success"
            };
        }
        else if(row["history_case_result"] == 0){
            return {
                classes: "danger"
            };
        }
        return {};
    }

    function changeResult(value) {
        var ret = "未执行";
        if(value == 1){
            ret = "通过"
        }
        else if (value == 0){
            ret = "失败"
        }
        return ret
    }

    return oTableInit;
};

var CaseInitDetailTable = function (case_id, build_id) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $("#tb_case_init_detail").bootstrapTable({
            url:"/api/case/history_init/" + case_id + "/" + build_id,
            method: 'GET',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            paginationPreText:"上一页",
            paginationNextText:"下一页",
            pageSize: 1,                       //每页的记录行数（*）
            pageList: [1],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            rowStyle:rowStyle,
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
            columns: [
             {
                field: 'case_init_id',
                title: '任务ID',
                align:'left',
            }, {
                field: 'case_init_name',
                title: '初始名',
                align: "left",
            }, {
                field: "action",
                title: '执行动作',
                align: "left",
                class: 'json_style',
                formatter: showJson
            }, {
                field: 'init_exec_result',
                title: '执行结果',
                align: "left",
                class: 'json_style',
                formatter: showJson
            }]
        });
    };

    function showJson(value, row, index, field) {
        var ret = '<div style="height:200px;overflow:auto;padding:0px;margin:0px;"><pre class="json_hover">' + JSON.stringify(value, null, 2) + "</pre></div>";
        //var ret = '<div style="padding:0px;margin:0px;"><pre class="json_hover">' + JSON.stringify(value, null, 2) + "</pre></div>";
        // var ret = JSON.stringify(value, null, 2);
        if (field == "history_case_vars" && row["history_case_result"] == 1){
            ret = "-"
        }
        return ret
    }

    function rowStyle(row, index) {
        if (row["history_case_result"] == 1) {
            return {
                classes: "success"
            };
        }
        else if(row["history_case_result"] == 0){
            return {
                classes: "danger"
            };
        }
        return {};
    }

    return oTableInit;
};

var CasePreDetailTable = function (case_id, build_id) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $("#tb_case_pre_detail").bootstrapTable({
            url: "/api/case/history_pre/" + case_id + "/" + build_id,
            method: 'GET',                      //请求方式（*）
            dataType: "json",
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
            pageSize: 100,                       //每页的记录行数（*）
            pageList: [100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            rowStyle:rowStyle,
            strictSearch: true,
            showColumns: false,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            queryParams: oTableInit.queryParams,//传递参数（*）
            clickToSelect: false,                //是否启用点击选中行
            //height: 700,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [
             {
                field: 'prev_id',
                title: '任务ID',
                align:'left',
            }, {
                field: 'prev_name',
                title: '前置名',
                align: "left",
            }, {
                field: 'prev_except_value',
                title: '期望值',
                align: "left",
                class: 'json_style',
                formatter: showJson
            },  {
                field: "action",
                title: '执行动作',
                align: "left",
                class: 'json_style',
                formatter: showJson
            }, {
                field: 'prev_exec_result',
                title: '执行结果',
                align: "left",
                class: 'json_style',
                formatter: showJson
            }],
        });
    };

    function showAction(value, row, index, field) {
        var ret = "";
        /*if(row["prev_api_address"] != ""){
            value = {
                "prev_api_address": row["prev_api_address"],
                "prev_api_method": row["prev_api_method"],
                "prev_api_params": row["prev_api_params"],
                "prev_api_header": row["prev_api_header"],
                "prev_api_expression": row["prev_api_expression"],
            };
            ret += '<div style="overflow:auto;padding:0px;margin:0px;"><pre class="json_hover">' + JSON.stringify(value, null, 2) + "</pre></div>"
        }
        else if (row["prev_sql_statement"] != ""){
            value = {
                "prev_sql_statement": row["prev_sql_statement"],
                "prev_sql_params": row["prev_sql_params"],
                "prev_sql_database": row["prev_sql_database"],
                "prev_sql_expression": row["prev_sql_expression"],
            };
            ret += '<div style="overflow:auto;padding:0px;margin:0px;"><pre class="json_hover">' + JSON.stringify(value, null, 2) + "</pre></div>"
        }
        else if (row["prev_expression"] != ""){
            value = {
                "prev_expression": row["prev_expression"],
                "prev_params": row["prev_params"],
                "prev_except_expression": row["prev_except_expression"],
            };
            ret += '<div style="overflow:auto;padding:0px;margin:0px;"><pre class="json_hover">' + JSON.stringify(value, null, 2) + "</pre></div>"
        }*/
        return '<div style="height:120px;overflow:auto;padding:0px;margin:0px;"><pre class="json_hover">' + JSON.stringify(value, null, 2) + "</pre></div>"
    }

    function showJson(value, row, index, field) {
        var ret = '<div style="height:200px;overflow:auto;padding:0px;margin:0px;"><pre class="json_hover">' + JSON.stringify(value, null, 2) + "</pre></div>";
        //var ret = '<div style="padding:0px;margin:0px;"><pre class="json_hover">' + JSON.stringify(value, null, 2) + "</pre></div>";
        // var ret = JSON.stringify(value, null, 2);
        if (field == "history_case_vars" && row["history_case_result"] == 1){
            ret = "-"
        }
        return ret
    }

    function rowStyle(row, index) {
        if (row["history_case_result"] == 1) {
            return {
                classes: "success"
            };
        }
        else if(row["history_case_result"] == 0){
            return {
                classes: "danger"
            };
        }
        return {};
    }

    function changeResult(value) {
        var ret = "未执行";
        if(value == 1){
            ret = "通过"
        }
        else if (value == 0){
            ret = "失败"
        }
        return ret
    }

    return oTableInit;
};

var RunCaseTableInit = function (item, task_id, build_id, env) {
    var oTableInit = new Object();
    //初始化Table
    var page_height = $(window).height();
    oTableInit.Init = function () {
        $(item).bootstrapTable({
            url: '/api/task/run_case/result/' + task_id + '/' + build_id,         //请求后台的URL（*）
            //url: '/api/task/run_case/result/' + build_id + '/' + 'grant_baiji_jinjian_3q',
            method: 'GET',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            paginationPreText:"上一页",
            paginationNextText:"下一页",
            height: page_height - 470,
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            rowStyle:rowStyle,
            strictSearch: true,
            showColumns: false,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: false,                //是否启用点击选中行
            //height: 700,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: true,                   //是否显示父子表
            onLoadSuccess: function(data){
                if(data.rows.length == 0) {
                    $(item).bootstrapTable('resetView',{ height: $(window).height() - 470 + 54 } );
                }
            },
            onExpandRow:  function (index, row, $detail) {
                oTableInit.InitSubTable(index, row, $detail);
            },
            columns: [
             {
                field: 'history_case_id',
                title: 'ID',
                visible: true,
                 class:"id_class"
            }, {
                field: 'history_case_name',
                title: '用例名称',
                align:'left',
                class: 'W90'
            }, {
                field: 'history_case_description',
                title: '用例描述',
                align:'left',
                class: 'W90'
            }, {
                field: 'history_case_from_system',
                title: '运行环境',
                align: 'left',
                class: 'W90',
                formatter:function () {
                    return env
                },
            }, {
                field: 'history_case_except_value',
                title: '期望结果',
                align:'left',
                class: 'json_style',
                formatter:showJson
            }, {
                field: 'history_case_actual_value',
                title: '实际结果',
                align:'left',
                class: 'json_style',
                formatter: showJson
            }, {
                field: 'history_case_result',
                title: '执行结果',
                align: "left",
                class:"W90",
                formatter:changeResult,
            }, {
                align: "left",
                class: 'W90',
                field: 'operate',
                title: '详情',
                events: operateEvents,
                formatter:casedetailInfo
            }],
        });
    };

    function rowStyle(row, index) {
        if (row["history_case_result"] == 1) {
            return {
                classes: "success"
            };
        }
        else if(row["history_case_result"] == 0){
            return {
                classes: "danger"
            };
        }
        return {};
    }

    function changeCaseType(value) {
        var ret = value;
        if(value == "common"){
            ret = "简单场景";
        }
        else if(value == "group"){
            ret = "复杂场景";
        }
        return ret
    }
    // 初始化子表格
    oTableInit.InitSubTable = function (index, row, $detail) {
        var case_exec_group = row.history_case_exec_group;

        if($.isEmptyObject(case_exec_group)==true){
            return
        }
        var cur_table = $detail.html('<table id="tb_' + row.history_case_id +  '"></table>').find('table');

        $(cur_table).bootstrapTable({
            url: '/api/task/run_case/result/' + build_id + '/' + case_exec_group,
            method: 'get',
            striped: true,
            rowStyle:rowStyle,
            queryParams: {
                page_index: 1,
                page_size: 2
            },
            clickToSelect: true,
            detailView: false,//父子表
            pageSize: 20,
            columns: [{
                field: 'history_case_id',
                title: 'ID',
                align: 'left',
                class: 'id_class',
            }, {
                field: 'history_case_name',
                title: '用例名称',
                align: 'left',
                class: 'W90',
            }, {
                field: 'history_case_description',
                title: '用例描述',
                align: 'left',
                class: 'W90',
            }, {
                field: 'history_case_except_value',
                title: '期望结果',
                align: "left",
                class: 'json_style',
                formatter: showJson
            }, {
                field: 'history_case_actual_value',
                title: '实际结果',
                align: "left",
                class: 'json_style',
                formatter: showJson
            },{
                field: 'history_case_result',
                title: '执行结果',
                align: "left",
                class: "W90",
                formatter: changeResult
            },{
                align: "left",
                class: 'W90',
                field: 'operate',
                title: '详情',
                events: operateEvents,
                formatter:casedetailInfo
            }],
        });
    };

    function casedetailInfo(value, row, index) {
            return [
                '<a class="case_detail_info" style="cursor: pointer" href="javascript:void(0)" title="详情">',
                '<span>详情</span>',
                '</a><br />',
                '<a class="init_task" style="cursor: pointer" href="javascript:void(0)" title="初始化">',
                '<span>初始化</span>',
                '</a><br />',
                '<a class="pre_task" style="cursor: pointer" href="javascript:void(0)" title="前置任务">',
                '<span>前置任务</span>',
                '</a><br />',
                '<a class="edit_case" style="cursor: pointer" href="javascript:void(0)" title="前置任务">',
                '<span>编辑用例</span>',
                '</a>',
            ].join('');
        };

    function changeResult(value) {
        var ret = "未执行";
        if(value == 1){
            ret = "通过"
        }
        else if (value == 0){
            ret = "失败"
        }
        return ret
    }

    function showJson(value, row, index, field) {
        var ret = '<div style="height:100px;overflow:auto;padding:0px;margin:0px;"><pre class="json_hover">' + JSON.stringify(value, null, 2) + "</pre></div>";
        // var ret = JSON.stringify(value, null, 2);
        if (field == "history_case_vars" && row["history_case_result"] == 1){
            ret = "-"
        }
        return ret
    }

    function casesubFormatter(value, row, index) {
        return [
            '<a class="case_update" style="cursor: pointer" href="case/' + row.case_id + '/" title="编辑">',
            '<span class=\'glyphicon glyphicon-pencil\'></span>',
            '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
            '<a class="case_delete"  style="cursor: pointer" href="javascript:void(0)"   title="删除">',
            '<span class=\'glyphicon glyphicon-remove\'></span>',
            '</a>',

        ].join('');
    };

    oTableInit.subqueryParams = function(params){
      var temp = {

      };
      return temp;
    };
    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            page_index: (params.offset / params.limit) + 1,
            page_size: params.limit,
        };
        return temp;
    };

    return oTableInit;
};

function update_progress(status_url, nanobar, status_div, last_log) {
    // send GET request to status URL
    $.getJSON(status_url, function(data) {
        // update UI
        var task_id = $("#task_id_number").val();
        var percent = parseInt(data['current'] * 100 / data['total']);
        nanobar.go(percent);
        $(status_div.childNodes[1]).text(percent + '%');
        if(data['status'] != "" && data['status'] != last_log){
                $(status_div.childNodes[2]).html("<pre style='text-align:left;background:white;border:0px;margin:0px;'>" + data['status'] + "</pre>");
            }
        last_log = data['status'];
        // console.log(data['state'] == 'PENDING' || data['state'] == 'PROGRESS', data);
        if (data['state'] == 'PENDING' || data['state'] == 'PROGRESS') {
               // rerun in 2 seconds
            setTimeout(function() {
              update_progress(status_url, nanobar, status_div, last_log);
            }, 2000);
        }
        set_log_height();
    });
}

$("#btn_exec").click(function () {
    var task_id = $("#task_id").val();
    $.ajax({
        type: "GET",
        url: "/tasks/case_task_create/" + task_id,
        data: {
            "task_run_env": $("#task_run_env").val(),
            "user": "{{ current_user.username }}"
        },
        contentType: "application/json; charset=UTF-8",
        success: function (data) {
            if (data.code != 202) {
                toastr.error("error", "程序发生异常，请求联系管理员");
                //$("#btn_exec").removeAttr("disabled");
            }
            else {
                toastr.success("success", "任务运行成功");
                getRunList(1);
                setTimeout(function () {
                    get_run_case(task_id, data.build_id);
                }, 100);
                exect_refresh_task();
            }
        },
        error:function (data) {
            //$("#btn_exec").removeAttr("disabled");
        }
    });
});

function get_run_case(task_id, build_id) {
   $.ajax({
       url: "/api/task/run_case/result/" + task_id + "/" + build_id,
       type:"GET",
       success: function (data) {
           var row_count = $("#tb_run_case0").bootstrapTable("getData").length;
           if(data.rows.length > 0 && data.rows.length != row_count) {
               $("#tb_run_case0").bootstrapTable("destroy");
               var item = $("#tb_run_case0");
               var oTable = new RunCaseTableInit(item, task_id, build_id, data.env);
               oTable.Init();
               $("#tb_run_case0").bootstrapTable("refresh");
           }

           if(data.code == 0){
               if(data.finish == 1){
                    $.ajax({
                        type: "GET",
                        url: "/api/task/detail/" + task_id,
                        contentType: "application/json; charset=UTF-8",
                        success: function (info) {
                            if (info.code == 0){
                                refresh_task_detail(info);
                            }
                        }
                    });
               }
               else {
                   console.log("获取运行用例情况未完成！");
                   setTimeout(function(){
                       get_run_case(task_id, build_id);
                   }, 4000);
               }

           }
           else{
                console.log("获取运行用例情况失败");
           }
       },
       error:function () {
            console.log("获取运行用例情况异常");
       }
   })
}

function exect_refresh_task() {
   $.ajax({
        type: "GET",
        url: "/api/task/detail/" + $("#task_id").val(),
        contentType: "application/json; charset=UTF-8",
        success: function (data) {
            if (data.code != 0) {
                return;
            }
            else{
                refresh_task_detail(data);
            }
        }
    });
}

function get_run_logger(url, run_id) {
    $("#progress_" + run_id).html("");
    var div = $('<div class="my_progress"><div></div><div class="my_percent">0%</div><div class="log_div" style="' +
        'overflow-y: auto;margin-top:10px;text-align:left"></div></div>');
    $("#myTabContent  #progress_" + run_id).append(div);
    var nanobar = new Nanobar({
        bg: '#38f',
        sh: 1,
        target:div[0].childNodes[0]
    });
    set_log_height();
    update_progress(url, nanobar, div[0], "");
}

function change_status(value, row, index) {
    var ret = "";
    if (value == 0){
        ret = '空闲';
    }
    else if (value == 1 ){
        ret = "运行中";
    }
    else {
        ret = "未知状态";
    }
    return ret
}

function change_run_time(value, row, index) {
    var ret = "未运行";
    if(value){
        ret = value;
    }
    return ret
}

$("#btn_query").click(function () {
    $("#tb_task_list").bootstrapTable('selectPage', 1);
});

$(document).keydown(function (event) {
    if (event.keyCode == 13) {
        $('#btn_query').triggerHandler('click');
    }
});
