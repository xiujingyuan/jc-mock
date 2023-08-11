$(function () {

    //主分支构建绑定事件
    $("#div_master_build button").bind("click", do_master_build);

    //修改
    $.each($("#div_master_env select"), function (i, sel) {
       $(sel).selectpicker({"width": 80})
    });

    var task_table = AssumptTableInit();
    task_table.Init();



    $("#sel_quality_info_level").selectpicker({"width": 80});
    $("#sel_quality_info_level").selectpicker('refresh');

    $("#master_div_edit_new a").click(function () {
        var program_id_list = $(this).attr("id").split("_");
        var program_id = program_id_list[program_id_list.length - 1];
        var env_id = $("#master_build_env_" + program_id).val();
        var jenkins_job = $("#master_jenkin_id_" + program_id).val();
        $("#tb_case_branch_commit").bootstrapTable("destroy");
        var branch_commit_table = BranchCommitTableInit("master", jenkins_job, program_id, env_id);
        branch_commit_table.Init();
        $("#showBranchCommit").modal("show");
    });

    $("#taskTab li").click(function () {
        $.each($("#taskTab li"), function (index, item) {
            $(this).removeClass("active")
        });
        $(this).addClass("active");

        $('#tb_assumpt_task').bootstrapTable('refresh');
        //refresh_task_table();
    });

    $(window).resize(function (){
        var page_height = $(window).height();
        $( '#tb_assumpt_task' ).bootstrapTable('resetView',{ height: page_height - 100 } );
    });

    bind_sel_env_jacoco();
    //master的jenkins

    //qnn的master分支的覆盖率
    var jenkins_job = $("#master_jenkin_id_10").val();
    var test_env = $("#master_build_env_10").val();

    change_qnn_jacoco_url(jenkins_job, test_env);

    $("#btn_uploadimg").click(function () {
           var fileObj = document.getElementById("FileUpload").files[0]; // js 获取文件对象
           if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
               alert("请选择图片");
               return;
           }
           var formFile = new FormData();
           formFile.append("action", "UploadVMKImagePath");
           formFile.append("file", fileObj); //加入文件对象
           //第二种 ajax 提交

           var data = formFile;
           $.ajax({
               url: "/api/upload/" + fileObj.name + "/" + $("#story_id").val() + "/" + $("#task_index").val(),
               data: data,
               headers: {
                    "X-CSRFToken": pt_csrf_token,
                    "content-type": "application/json"
                },
               type: "Post",
               dataType: "json",
               cache: false,//上传文件无需缓存
               processData: false,//用于对data参数进行序列化处理 这里必须false
               contentType: false, //必须
               success: function (data) {
                   if(data.code == 0){
                       toastr.success("success", data.message);
                       $("#modal_upload_file").modal("hide");
                       $("#tb_assumpt_task").bootstrapTable("updateCell", {index:data.index, field:"case_name",
                           value:data.file_name});
                       bind_click();
                       $("#FileUpload").val("");
                   }else{
                       toastr.error("error", data.message);
                   }

               },
           })
       });

    function change_qnn_jacoco_url(jenkins_job, test_env) {
        $.ajax({
            url: "/api/build_task/program_service_name",
            type: "GET",
            dataType: "json",
            data:{
                "jenkins_job": jenkins_job,
                "program_id": 10,
                "env": test_env
            },
            success: function (data) {
              if(data.code == 0){
                  var new_href = data.data.jacoco_url + "/master_new/summary_report.html";
                  $("#master_build_jacoco_10").attr("href", new_href);
              }
            },
            error:function () {

            }
        });

    }

    $("#master_build_env_10").on("changed.bs.select", function (e){
        var test_env = $(this).val();
        var jenkins_job = $("#master_jenkin_id_10").val();
        change_qnn_jacoco_url(jenkins_job, test_env);
    });
    $("#master_jenkin_id_10").on("changed.bs.select", function (e){
        var jenkins_job = $(this).val();
        var test_env = $("#master_build_env_10").val();
        change_qnn_jacoco_url(jenkins_job, test_env);
    });

    //在客户端记录选择tab页
    $("#myTab a").bind("click", save_click);

    $("#div_email button").bind("click", show_email);

    var mytab = get_click();

    $.each($("#myTab a"), function (i, item) {
        if ($(item).attr("href") == mytab){
            $(item).click();
        }
    });

    //禁止记录页构建日志单独可点击
    $('#buildRecordTab a').click(function (e) {
        e.preventDefault();
        if($(this).attr("href") == "#tab_detail_0"){
            $(this).tab('show');
        }
    });

    // 绑定分支可编辑事件
    $.each($("#lab_branch label"), function (i, item) {
        $(item).editable({
            validate: function (value) { //字段验证
                if (!$.trim(value)) {
                    return '不能为空';
                }
            },
            url: function (params) {
                var id_list = params.name.split("_");
                var id = id_list[id_list.length - 1];
                var branch = params.value;
                $.ajax({
                    url: "/api/build_task/update",
                    type: "POST",
                    sync:true,
                    headers: {
                        "X-CSRFToken": pt_csrf_token,
                        "content-type": "application/json"
                    },
                    data: JSON.stringify({
                        "task_id": id,
                        "branch": branch
                    }),
                    dataType: "json",
                    success: function (data) {
                        if (data.code == 0) {
                            $("#build_jacoco_" + id).prop("href", data.jacoco + "_new/summary_report.html");
                            toastr.success("success", data.message);
                            // refresh_env_by_branch(branch, id);

                        }
                        else {
                            toastr.warning("warning", "更新失败");
                            $(item).text(data.data)
                        }
                    },
                    error: function () {
                        toastr.error("error", "更新异常");
                        $(item).text(data.data)
                    }
                });
            }
        });
    });

    // refresh_task_table();

});

function refresh_task_table() {
    $("#tb_assumpt_task").bootstrapTable("destroy");
    var task_type = $("#taskTab li.active a").attr("id");
    var assumpt_table = AssumptTableInit(task_type);
    assumpt_table.Init();
}
var options = {
    mode: "code"
};

var json = {
};
var json_dict = {};
var json_list = ['json_filter_file_value'];

for(var json_name in json_list){
    var container = document.getElementById(json_list[json_name]);
    var json_edit = new JSONEditor(container, options, json);
    json_dict[json_list[json_name]] = json_edit;
}

function bind_click() {
    $("a.case_upload").unbind("click").click(function () {
        var id_list = $(this).attr("id").split("_");
        console.log(id_list);
        $("#story_id").val(id_list[1]);
        $("#task_index").val(id_list[2]);
        $("#modal_upload_file").modal("show");
      }
  );
}

var AssumptTableInit = function () {
    var oTableInit = new Object();
    var id_lists = window.location.pathname.split("/");
    var program_id = id_lists[id_lists.length - 2];
    var env;
    var gitreport_name;
    var theight = $(window).height();
    oTableInit.Init = function () {
        $("#tb_assumpt_task").bootstrapTable({
            url: '/api/build_task/run/detail',         //请求后台的URL（*）
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
            height: theight - 100,
            paginationPreText:"上一页",
            paginationNextText:"下一页",
            pageSize: 20,                       //每页的记录行数（*）
            pageList: [20, 50],        //可供选择的每页的行数（*）
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
                title: 'ID',
                formatter:function (value, row, index) {
                    return index + 1
                },
                class: 'col-text'
            },{
                field: 'id',
                title: 'ID',
                visible: false,
            },{
                field: 'auto_url',
                title: 'auto_url',
                visible: false,
            },{
                field: 'mail_receive_time',
                title: '提测时间',
                class: "col-receive-time"
            }, {
                field: 'publish_time',
                title: "发布时间",
                class: "col-publish-time",
                formatter: function (value, row, index) {
                    if(row["build_task_status"] == 0){
                        return value
                    }
                    else{
                        return "未发布"
                    }
                }
            },
                {
                field: 'gitlab_program_name',
                title: '项目名称',
                class: 'col-text'
            },
                {
                field: 'build_branch',
                title: '构建分支',
                class: 'col-text'
            }, {
                field: 'story_name',
                title: '需求名',
                class: 'col-task-name',
                formatter:function (value, row, index) {
                    var new_value = '<a href="' + row["story_url"] + '" target="_blank">' + value + '</a>';
                    return "<div style='width:240px;text-overflow: ellipsis;overflow: hidden;'>" + new_value + "</div>"
                }
            }, {
                field: 'build_jenkins_jobs',
                title: 'Jenkins任务',
                formatter:JenkinsFormat,
            }, {
                field: 'build_task_status',
                title: '任务状态',
                visible: false,
            }, {
                field: 'last_build_env',
                title: '构建环境',
                formatter:EnvFormat,
                class: "col-env"
            }, {
                field: 'last_build_status',
                title: '构建状态',
                formatter: ShowLastBuildStatus,
                class: 'col-text'
            }, {
                field: 'build_coverage',
                title: '覆盖率',
                visible: false,
            }, {
                field: 'case_name',
                title: '用例',
                formatter: ShowCase,
                class: 'col-text'
            }, {
                field: 'operate',
                title: '操作',
                events: operateEvents,
                formatter: ShowOperate,
                class: "opclass"

            },],
            onEditableSave: function (field, row, oldValue, $el) {
                $.ajax({
                    url: "/api/build_task/update",
                    type: "POST",
                    headers: {
                        "X-CSRFToken": pt_csrf_token,
                        "content-type": "application/json"
                    },
                    data: JSON.stringify({
                        "task_id": row["id"],
                        "branch": row[field]
                    }),
                    dataType: 'JSON',
                    success: function (data) {
                        if (data.code == 0) {
                            toastr.success("success", data.message);
                            $("#tb_assumpt_task").bootstrapTable("refresh");
                        }
                        else {
                            toastr.warning("warning", "更新失败");
                            //$(item).text(data.data)
                        }
                    },
                    error: function () {
                        toastr.error("error", "更新失败");
                    },
                    complete: function () {

                    }

                });
            },
            onPostBody: function(){
                $(".col-env select").selectpicker({"width": 100});
                $(".col-compare-type select").selectpicker({"width": 80});
                $("#tb_assumpt_task select").selectpicker("refresh");
            },
            onLoadSuccess: function(data) {
                  $.each($("#tb_assumpt_task").bootstrapTable('getData'), function(index, item){
                    if(item["last_build_status"] == 3 || item["last_build_status"] == 5){
                        refresh_row("#tb_assumpt_task", item["last_run_id"],item["id"],index)
                    }
                });

                  bind_click();
                  // $.each($("a.case_upload"), function (index, item) {
                  //     $(item).click(function () {
                  //       var id_list = $(this).attr("id").split("_");
                  //       console.log(index, id_list);
                  //       $("#story_id").val(id_list[1]);
                  //       $("#task_index").val(id_list[2]);
                  //       $("#modal_upload_file").modal("show");
                  //     })
                  //
                  // });
            },
            responseHandler: function (result) {
                env = result.test_env;
                gitreport_name = result.program;
                //如果没有错误则返回数据，渲染表格
                return result
                },
        });

    };


    function ShowCase(value, row, index) {
        return '<a class="case_upload" id="upload_' + row["story_id"] + '_' + index + '"><i class="fa fa-upload" aria-hidden="true" ></i></a> | ' +
            '<a href="' + row["case_name"] + '" target="_blank"><i class="fa fa-download" aria-hidden="true" ></i></a>'
    }
    function ShowOperate(value, row, index) {
        var coverage = "覆盖" + row["last_coverage"] + "%";
        var ret = '<a class="jenkines_build" style="cursor: pointer;" href="javascript:void(0)" title="构建">';
        ret += '<span>构建</span>';
        ret += '</a>&nbsp;&nbsp;';
        ret += '<a class="jenkines_master_build" style="cursor: pointer;" href="javascript:void(0)" title="master构建">';
        ret += '<span>master构建</span>';
        ret += '</a>&nbsp;&nbsp;';
        ret += '<a class="jenkines_build_cancel" style="cursor: pointer;" href="javascript:void(0)" title="终止构建">';
        ret += '<span>终止</span>';
        ret += '</a>&nbsp;&nbsp;';
        ret += '<a class="show_log" style="cursor: pointer;" href="javascript:void(0)" title="日志">';
        ret += '<span>日志</span></a>&nbsp;&nbsp;';
        ret += '<a class="exec_auto" style="cursor: pointer;" href="javascript:void(0)" title="执行自动化">';
        ret += '<span>自动化</span></a>&nbsp;&nbsp;';
        ret += '<br /><a class="show_jacoco_new" style="cursor: pointer;" href="javascript:void(0)" title="';
        ret += coverage;
        ret += '">'
        ret += '<span>';
        ret += coverage;
        ret += '</span>';

        // ret += '<a class="show_merge_jacoco" style="cursor: pointer;" href="javascript:void(0)" title="合并覆盖率">';
        // ret += '<span>合并覆盖率</span>';
//        ret += '<a class="show_quality_info" style="cursor: pointer;" href="javascript:void(0)" title="提测质量">';
//        ret += '<span>提测质量</span>';
        ret += '</a>&nbsp;&nbsp;';
        ret += '<a class="modify_branch_info" style="cursor: pointer;" href="javascript:void(0)" title="修改分支">';
        ret += '<span>修改分支</span>';
        ret += '</a>&nbsp;&nbsp;';
        if(row["build_task_status"] == 0){
            ret += '<a style="cursor: pointer;color:red;" href="javascript:void(0)"   title="已发布">';
            ret += '<span>已发布</span>&nbsp;&nbsp;';
            ret += '</a>';
        }else{
            ret += '<a class="story_complete"  style="cursor: pointer;" href="javascript:void(0)"   title="发布需求">';
            ret += '<span>发布需求</span>&nbsp;&nbsp;';
            ret += '</a>';
        }
        // ret += '<a class="show_auto_report" style="cursor: pointer;" href="javascript:void(0)" title="自动化报告">';
        // ret += '<span>报告</span></a>&nbsp;&nbsp;';
        ret += '<a class="filter_file" style="cursor: pointer;" href="javascript:void(0)" title="过滤">';
        ret += '<span>过滤</span></a>&nbsp;&nbsp;';
//        ret += '</a>&nbsp;&nbsp;';
//        ret += '</a><a class="show_totest" style="cursor: pointer;" href="javascript:void(0)" title="提测邮件">';
//        ret += '<span>提测邮件</span>';
//         ret += '</a>&nbsp;&nbsp;';
//         ret += '</a><a class="show_jacoco_new" style="cursor: pointer;" href="javascript:void(0)" title="新覆盖率">';
//         ret += '<span>新覆盖率</span>';
        return ret;
    };

    function ShowLastBuildStatus(value, row, index) {
        var last_build_status = "空闲";
        if(value == 1){
            last_build_status = "成功"
        }
        else if(value == 2){
            last_build_status = "失败"
        }
        else if(value == 3){
            last_build_status = "构建中"
        }
        else if(value == 4){
            last_build_status = "已取消"
        }
        else if(value == 5){
            last_build_status = "准备中"
        }
        else if(value == 6){
            last_build_status = "排队中"
        }
        return last_build_status
    }

    function JenkinsFormat(value, row, index){
        var ret = '<select id="jenkin_id_' + row["id"] + '" class="selectpicker " data-style="btn-primary">';
        if(value.length == 0){
            ret += '<option>not_found</option>';
        }
        else{
            for(var index in value){
                ret += '<option>' + value[index]["name"] + '</option>'
            }
        }
        ret += '</select>';
        return ret
    }

    function EnvFormat(value, row, index){
        var ret = '<select id="build_env_' + row["id"] + '" class="selectpicker " data-style="btn-primary">';
        var has_opt = false;
        if(env.length == 0){
            ret += '<option>not_found</option>';
        }
        else{
            for(var env_index in env){
                for(var jenkins_index  in row["build_jenkins_jobs"]){
                    if(row["build_jenkins_jobs"][jenkins_index]["name"] == env[env_index]["jenkins_job_name"]){
                        has_opt = true;
                        if(value == env[env_index]["env_id"]){
                            ret += '<option selected>' + env[env_index]["env_id"] + '</option>'
                        }
                        else{
                            ret += '<option>' + env[env_index]["env_id"] + '</option>'
                        }
                    }
                }
            }
            if(!has_opt && env.length != 0){
                ret += '<option>not_found</option>';
            }
        }
        ret += '</select>';
        return ret
    }

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            program_id: program_id,
            task_type: $("#taskTab li.active a").attr("id"),
            page_index: (params.offset / params.limit) + 1,
            page_size: params.limit
        };

        if(!$.isEmptyObject(temp["case_id"])){
            temp["case_from_system"] = "";
            temp["case_belong_business"] = "";
            temp["case_executor"] = "";
            temp["case_is_exec"] = "";
        }
        console.log(temp);
        return temp;
    };

    return oTableInit;
};

var BranchCommitTableInit = function (branch, jenkins, program_id, env) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $("#tb_case_branch_commit").bootstrapTable({
            url: '/api/coverage/' + branch + "/" + jenkins + "/" + program_id + "/" + env,   //请求后台的URL（*）
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
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10],        //可供选择的每页的行数（*）
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
                field: 'id',
                title: '提交ID',
            }, {
                field: 'name',
                title: '提交信息',
                align: 'left',
            }, {
                field: 'author',
                title: '提交人',
                align: 'center',
            }, {
                field: 'time',
                title: '提交时间',
                align: 'left',
                align: 'center',
                formatter: function (value, row, index) {
                    return value.replace("T", " ").replace(".000Z", "")
                }
            }, ],
        });

    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            program_id: program_id,
            page_index: (params.offset / params.limit) + 1,
            page_size: params.limit,
            task_type: params.task_type
        };
        return temp;
    };

    return oTableInit;
};

$('#tb_case_branch_commit').on('click-row.bs.table', function (e,row,$element) {
    //$('.changeColor').removeClass('changeColor');
    //$($element).addClass('changeColor');
    // /coverage/514/testing/1/3599
    var url = "/coverage/" + row["gitlab_id"] + "/" + row["branch"] + "/" + row["env"] + "/" + row["id"];
    window.open(url);

});

function bind_sel_env_jacoco(){
    $.each($("#build_env_sel select"), function (i, item) {
        if($(item).find("option").length == 0){
            $(item).append('<option></option>');
        }
        $(item).on("changed.bs.select", function (e) {
            var old_env = "1/";
            var new_env = "2/";
            var item_list = $(item).attr("id").split("_");
            var item_id = item_list[item_list.length - 1];
            if($(item).val() == "1"){
                old_env = "2/";
                new_env = "1/";
            }
            var new_url = $("#build_jacoco_" + item_id).attr("href").replace(old_env, new_env);

            $("#build_jacoco_" + item_id).attr("href", new_url);

        })
    });
}
// 绑定构建详情记录的按钮事件
$.each($("#div_build_record button"), function (i, item) {
    $(item).bind("click", get_record);
});

var buildRcordTable = function (program_id, test_env) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_build_record').bootstrapTable({
            url: '/api/build_task/env/list',         //请求后台的URL（*）
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
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 20],        //可供选择的每页的行数（*）
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
            detailView: false,                   //是否显示父子表,
            columns: [{
                field: 'id',
                title: 'ID',
                visible: true,
            }, {
                field: 'build_user',
                title: '构建人',
                align:'left'
            }, {
                field: 'build_time',
                title: '构建时间',
                align:'left'
            }, {
                field: 'build_branch',
                title: '构建分支',
                align:'left'
            }, {
                field: 'build_result',
                title: '构建结果',
                formatter: buildFormatter,
                align: 'left'
            }, {
                field: 'build_jenkins',
                title: 'jenkins任务',
                align: 'left'

            }, {
                field: 'build_jenkins_task_id',
                title: 'jenkins任务ID',
                formatter: jenkinjobFormatter,
                align: 'left'

            }, {
                field: 'build_message',
                title: '日志',
                events: operateEvents,
                formatter: logFormatter,
                align: 'left'
            },]
        });
    };

    function jenkinjobFormatter(value, row, index) {
        return '<a href="https://jenkins-test.kuainiujinke.com/jenkins/job/' + row.build_jenkins + "/" + value +
            '/console" target="_blank">' + value + '</a>'
    }


    function buildFormatter(value, row, index) {
        //构建结果，0:构建中；2:构建成功；3构建失败
        var ret;
        if(value == 2){
            ret = "成功"
        }
        else if (value == 0){
            if(row.build_jenkins_task_id > 0){
                ret = "构建中"
            }
            else{
                ret = "准备中"
            }
        }
        else if (value == 3){
            ret = "失败"
        }
        else if (value == 4){
            ret = "已取消"
        }
        else{
            ret = "未知"
        }
        return ret
    }

    function logFormatter(value, row, index) {
            return [
                '<a id="' + row["id"] + '" class="log_detail" style="cursor: pointer" href="javascript:void(0)" title="详情">',
                '<span>详情</span>',
                '</a>',

            ].join('');
        };


    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            program_id: program_id,
            env: test_env,
            page_index: (params.offset / params.limit) + 1,
            page_size: params.limit,
        };
        return temp;
    };
    return oTableInit;
};

function get_record() {
    var bt_id = $(this).attr("id").split("_");
    var program_id = bt_id[bt_id.length - 1];
    var env = $("#master_build_env_" + program_id).val() || 1;
    $("#tb_build_record").remove();
    $("#div_table").html('<table id="tb_build_record"></table>');

    $("#record_title").text(program_name + "-环境" + env.toString() + "-构建记录");

    var oTable = new buildRcordTable(program_id, env);

    oTable.Init();

    $("#showBuildRecord").modal("show");

}

function get_click() {
    var save_key = get_href_name();
    return localStorage.getItem(save_key)
}

function save_click() {

    var save_key = get_href_name();
    localStorage.setItem(save_key, $(this).attr("href"));
}

function get_href_name() {
    var href_list = window.location.href.split("/");
    var save_key;
    if (href_list[href_list.length - 1] == "")
    {
        save_key = href_list[href_list.length - 2];
    }
    else{
        save_key = href_list[href_list.length - 1];
    }
    return save_key
}

/*var mdm_url = $("#mdm_url").val();
console.log(mdm_url);
var socket = io(mdm_url + 'websocket/receive_email');

socket.on('connect', function() { // 发送到服务器的通信内容
    socket.emit('connect_event', {data: '我已连接上服务端！'});
});


socket.on('server_response', function(msg) {
    //显示接受到的通信内容，包括服务器端直接发送的内容和反馈给客户端的内容
    console.log(msg);
});
socket.on('user_response', function(msg) {
    // 获取后端传过来的业务数据
    console.log(msg);
    if (msg.data == "new_data"){
        $.each(msg.program_id, function (i, item) {
            // getRunList(item, 1);
            $("#tb_assumpt_task_" + msg.program_id).bootstrapTable("refresh");
        })

    }
});*/

function show_email() {
        var email_id_list = $(this).attr("id").split("_");
        var email_id = email_id_list[email_id_list.length - 1];
        $.ajax({
            url: "/api/build_task/email_content/" + email_id,
            type:'GET',
            dataType: "json",
            success:function (data) {
                if(data.code == 0){
                    // $("#email_content").attr("src", "{{ url_for('static', filename='email/35001.html') }}");
                    var my_url = "{{ url_for('static', filename='') }}" + 'email/' + email_id + '.html';
                    $("#email_content").attr("src", my_url);
                    // $("#record_title").val("提测时间：" + "-" + "" + "提测邮件内容");
                    $("#showEmailContent").modal("show");

                    toastr.success("success", "显示邮件成功");
                }
                else {
                    toastr.warning("warning", "显示邮件错误");
                }
            },
            error:function () {
                toastr.error("error", "显示邮件异常");
            }
        })
    }

function do_master_build() {
    var click_id = $(this).attr("id");
    var id_list = click_id.split("_");
    var build_task_id = id_list[id_list.length - 1];

    $.ajax({
        type: "POST",
        url: "/tasks/build_task_create/" + build_task_id,
        contentType: "application/json; charset=UTF-8",
        headers: {"X-CSRFToken": pt_csrf_token},
        data: JSON.stringify({
           "job_name": $("#master_jenkin_id_" + build_task_id).val(),
           "program": build_task_id,
           "is_master": "1",
           "build_branch": "master",
           "env": {"Branch": "master", "num": $("#master_build_env_" + build_task_id).val()}
       }),
        dataType: "json",
        success: function (data) {
            if (data.code != 202) {
                toastr.warning("创建任务异常，" + data.message,"Error");
                $("#master_status_" + build_task_id).text("构建状态:失败");
            }
            else {
                $.ajax({
                    url: data["url"],
                    type: "GET",
                    success: function (ret){
                        toastr.success("任务运行成功", "Success");
                        var data_list = data["url"].split("/");
                        var build_task_run_id = data_list[data_list.length - 1];
                        $("#master_status_" + build_task_id).text("构建状态:构建中");
                        setTimeout(function() {
                              update_progress(build_task_run_id, build_task_id, $("#master_status_" + build_task_id))
                          }, 100);
                    },
                    error: function (ret) {
                        toastr.warning("创建任务失败，" + ret.code,"Error");
                        $("#master_status_" + build_task_id).text("构建状态:失败");
                }
                });
            }
        },
        error:function (data) {
            //$("#btn_exec").removeAttr("disabled");
            toastr.error("error", "登录失效，请刷新页面重新登录！");
            $("#master_status_" + build_task_id).text("构建状态:失败");
        }
    });
}

function get_program_id() {
    var program_id;
    var tab_list = $("#myTab li");
    for(var item in tab_list){
        if($(tab_list[item]).hasClass("active")){
            var active_a = $(tab_list[item]).find("a")[0];
            program_id = parseInt($(active_a).attr("href").replace("#tab", ""));
            return program_id
        }
    }
}

function create_build_task(table, build_task_id, build_branch, program_id, id, index, extend) {
    console.log(table, build_task_id, build_branch, program_id, id, index, extend);
    var req_data;
    req_data = {
           "job_name": $("#jenkin_id_" + build_task_id).val(),
           "build_branch": build_branch,
           "program": program_id,
           "env": {"Branch": build_branch, "num": $("#build_env_" + build_task_id).val()}
       };
    if(extend != 1){
        req_data["env"]["capital_num"] = extend["captinal"];
        req_data["env"]["biz_num"] = extend["biz"];
        $.each(extend, function (modal, branch) {
            req_data["env"][modal] = branch;
        });
        req_data["env"]["extend"] = extend;
    }
    console.log("req_data", req_data);
    $.ajax({
        type: "POST",
        url: "/tasks/build_task_create/" + build_task_id,
        contentType: "application/json; charset=UTF-8",
        headers: {"X-CSRFToken": pt_csrf_token},
        data: JSON.stringify(req_data),
        dataType: "json",
        success: function (data) {
            console.log("data", data);
            if (data.code != 202) {
                toastr.warning("创建任务异常，" + data.message, "Error");
                console.log(data.message);
            }
            else {
                $(table).bootstrapTable("updateCell", {index:index, field:"last_build_status", value:5});
                var data_list = data["url"].split("/");
                var build_task_run_id = data_list[data_list.length - 1];
                refresh_row(table, build_task_run_id, id, index);
            }
        },
        error:function () {
            toastr.error("登录失效，请刷新页面重新登录！", "error");
        }
    });
}

function refresh_row(table, build_task_run_id, id, index) {
    console.log(table, build_task_run_id, id, index);
    var status_url = "/api/build_task/status/" + build_task_run_id;
        $.ajax({
            url: status_url,
            dataType:"json",
            type:"GET",
            success: function(data) {
                // update UI
                console.log("refresh", data, index, data.data, id, table);
                if (data.code == 0) {
                    if(data.data){
                    var last_build_status = 0,
                        env = data.data["env"];
                    if(data.data["result"] == "ERROR" || data.data["result"] == "FAILURE"){
                        last_build_status = 2;
                    }else if (data.data["result"] == "SUCCESS"){
                        last_build_status = 1;
                    }else if (data.data["result"] == "PENDING"){
                        last_build_status = 5;
                    }else if (data.data["result"] == "QUEUE"){
                        last_build_status = 6;
                    }else if (data.data["result"] == "BUILDING"){
                        last_build_status = 3;
                    } else if (data.data["result"] == "ABORTED"){
                        last_build_status = 4;
                    }
                    //$(table).bootstrapTable("updateRow", {index:index, row:data.data});
                    $(table).bootstrapTable("updateCell", {index:index, field:"last_build_status", value:last_build_status});
                    $("#build_env_" + id).val(env);
                    $("#build_env_" + id).selectpicker("refresh");
                    if (data.data["result"] == "ERROR" || data.data["result"]  == "SUCCESS" ||
                        data.data["result"]  == "ABORTED" || data.data["result"] == "FAILURE") {

                    }
                    else {
                        setTimeout(function () {
                            refresh_row(table, build_task_run_id, id, index);
                        }, 5000)
                }}else{
                        setTimeout(function () {
                            refresh_row(table, build_task_run_id, id, index);
                        }, 5000)
                    }
                }

            }
        });
}

function refresh_env_by_branch(branch, task_id) {
    $.ajax({
            url: "/api/build_task/get_env",
            type: "GET",
            data: {
                   "branch": branch,
                   "program": get_program_id()
            },
            dataType: "json",
            success: function (data){
                if($("#build_env_" + task_id).find("option").length > 0) {
                    $("#build_env_" + task_id).empty();
                    for (var opt in data.data) {
                        $("#build_env_" + task_id).append('<option>' + data.data[opt]["env_id"] + '</option>');
                    }
                    if ($("#build_env_" + task_id).find("option").length  == 0) {
                        $("#build_env_" + task_id).append('<option></option>')
                    }
                    $("#build_env_" + task_id).selectpicker("refresh");
                    $("#build_env_" + task_id).selectpicker("render");
                }
            },
            error: function (data) {
                console.log("error", data);
        }
        });
}

function update_progress(build_task_run_id, build_task_id, bt) {
    // send GET request to status URL
    var status_url = "/api/build_task/status/" + build_task_run_id;
    $.ajax({
        url: status_url,
        dataType:"json",
        type:"GET",
        success: function(data) {
            // update UI
            if (data.code == 0) {
                if (data.data == 1) {
                    bt.text("构建状态:成功")
                }
                else if (data.data == 2) {
                    bt.text("构建状态:失败")
                }
                else if (data.data == 4){
                    bt.text("构建状态: 已取消")
                }
                else if (data.data == 5){
                    bt.text("构建状态: 准备中")
                }

                else {
                // rerun in 2 seconds
                setTimeout(function () {
                    update_progress(build_task_run_id, build_task_id, bt);
                }, 5000);
            }
            }

        }
    });
}

window.operateEvents = {
    'click .log_detail': function (e, value, row, index) {
        $.ajax({
            type: "GET",
            url: "/api/build_task/env/log/" + row['id'],
            contentType: "application/json; charset=UTF-8",
            success: function (data) {
                console.log(data);
                if (data.code != 0) {
                    toastr.error("error", "程序发生异常，请求联系管理员");
                }
                else{

                    $("#tab_log").click(function () {
                        $(this).tab('show').unbind('click');
                        $("#log_detail").html('<pre style="text-align: left;background:white;border:0px;' +
                            'margin:0px;height: 522px;overflow-y: auto;">' + data.log + '</pre>');

                    }).click();
                }
            }
        });
    },

    'click .task_run': function (e, value, row, index) {
        var case_ids = new Array()
        case_ids.push(row['case_id']);

        var run_case=JSON.stringify({
            "task_id":case_ids,
            "email": current_user_email
        });
        $.ajax({
            type: "POST",
            headers: {"X-CSRFToken": pt_csrf_token},
            url: "/api/case/run/case",
            contentType: "application/json; charset=UTF-8",
            data:run_case,
            success: function (data) {

                if (data.code != 0) {
                    toastr.error("error", data.msg);
                    return;
                }
                toastr.success("success", "执行请求已经发给后台任务执行，请检查邮箱" + current_user_email);

            }
        });
    },

    'click .show_email': function (e, value, row, index) {
        var email_id = row["email_id"];
        $.ajax({
            url: "/api/build_task/email_content/" + email_id,
            type:'GET',
            dataType: "json",
            success:function (data) {
                if(data.code == 0){
                    var my_url = "{{ url_for('static', filename='') }}" + 'email/' + email_id + '.html';
                    $("#email_content").attr("src", my_url);
                    $("#showEmailContent").modal("show");

                    toastr.success("success", "显示邮件成功");
                }
                else {
                    toastr.warning("warning", "显示邮件错误");
                }
            },
            error:function () {
                toastr.error("error", "显示邮件异常");
            }
        })
    },

    'click .show_log': function (e, value, row, index) {
        $.ajax({
            url: "/api/build_task/get_log/" + row.id,
            type: "GET",
            success:function(data){
              if(data.code == 0){
                  window.open(data.url);
              }else{
                  toastr.warning(data.msg, "warning")
              }
            },
        });
    },

    //
    'click .show_auto_report': function (e, value, row, index) {
        window.open(row.auto_url);
    },

    'click .exec_auto': function (e, value, row, index) {
        var env = row["last_build_env"];
        // 部署前先判断该环境是否有分支
        $.ajax({
            type: "GET",
            url: "/tasks/exec_auto_task/" + row['id'] + "/" + env,
            contentType: "application/json; charset=UTF-8",
            dataType: "json",
            success: function (data) {
                console.log("data", data);
                if (data.code != 0) {
                    toastr.error("程序发生异常，请求联系管理员", "error");
                    console.log(data.message);
                }
                else {
                    toastr.success("开始执行自动化用例，请稍后，详情请查看日志", "success");
                }
            },
            error:function () {
                toastr.error("程序发生异常，请求联系管理员", "error");
            }
        });
     },

    'click .show_totest': function (e, value, row, index) {
      var url= "https://www.tapd.cn/" + row.work_id +"/report/workspace_reports/?report_type=totest";
      window.open(url);
    },

    'click .show_quality_info': function (e, value, row, index) {
        var build_task_id = row["id"];
        $("#build_task_id").val(build_task_id);
        $.ajax({
            url: "/api/quality_info/" + build_task_id,
            type: 'GET',
            dataType: "json",
            success:function (data) {
                if(data.code == 0){
                    $("#txt_story_change_count").val(data.data.story_change_count);
                    $("#txt_smoke_count").val(data.data.smoke_count);
                    $("#txt_reason").val(data.data.reason);
                    $("#sel_quality_info_level").val(data.data.level);
                    $('#modal_quality_info').modal('show');
                }
                else {
                    toastr.warning("warning", "获取信息失败");
                }
            },
            error:function () {
                toastr.error("error", "获取信息异常");
            }
        });
    },

    'click .jenkines_build': function (e, value, row, index) {

        var build_task_id = row["id"];
        var build_branch = row["build_branch"];

        var program_id = row["program_id"];
        $("#bt_build_" + build_task_id).attr("disabled", "disabled");
        var assumpt_table = "#tb_assumpt_task";
        var id = row["id"];
        var job_name = $("#jenkin_id_" + build_task_id).val();
        // 部署前先判断该环境是否有分支
        $.ajax({
            type: "GET",
            url: "/api/build_task/get_env_status",
            contentType: "application/json; charset=UTF-8",
            data: {
               "program": program_id,
               "env": $("#build_env_" + build_task_id).val(),
               "branch": build_branch,
               "job_name": job_name,
           },
            success:function (data) {
                console.log(data);
                if(data.code == 2){
                    BootstrapDialog.confirm({
                        title : '确认',
                        message : data.data,
                        type : BootstrapDialog.TYPE_WARNING, // <-- Default value is
                        // BootstrapDialog.TYPE_PRIMARY
                        closable : true, // <-- Default value is false，点击对话框以外的页面内容可关闭
                        draggable : true, // <-- Default value is false，可拖拽
                        btnCancelLabel : '取消', // <-- Default value is 'Cancel',
                        btnOKLabel : '确定', // <-- Default value is 'OK',
                        btnOKClass : 'btn-warning', // <-- If you didn't specify it, dialog type
                        size : BootstrapDialog.SIZE_SMALL,
                        // 对话框关闭的时候执行方法
                        callback : function(result) {
                            // 点击确定按钮时，result为true
                            if (result) {
                                // 执行方法
                                // funcok.call();
                                build_task_msg(job_name, assumpt_table, build_task_id, build_branch, program_id, id, index);
                            }
                        }
                    });
                }
                else{
                    if (data.code == 3){
                        toastr.warning("没有找到对应的构建信息", "warning");
                    }
                    build_task_msg(job_name, assumpt_table, build_task_id, build_branch, program_id, id, index);
                }
            },
            error:function (data) {
                toastr.error("程序发生异常，请求联系管理员", "error");
            }
        });
     },

    'click .jenkines_master_build': function (e, value, row, index) {

        var build_task_id = row["id"];
        var build_branch = "master";

        var program_id = row["program_id"];
        $("#bt_build_" + build_task_id).attr("disabled", "disabled");
        var assumpt_table = "#tb_assumpt_task";
        var id = row["id"];
        var job_name = $("#jenkin_id_" + build_task_id).val();
        // 部署前先判断该环境是否有分支
        $.ajax({
            type: "GET",
            url: "/api/build_task/get_env_status",
            contentType: "application/json; charset=UTF-8",
            data: {
               "program": program_id,
               "env": $("#build_env_" + build_task_id).val(),
               "branch": build_branch,
               "job_name": job_name,
           },
            success:function (data) {
                if(data.code == 2){
                    BootstrapDialog.confirm({
                        title : '确认',
                        message : data.data,
                        type : BootstrapDialog.TYPE_WARNING, // <-- Default value is
                        // BootstrapDialog.TYPE_PRIMARY
                        closable : true, // <-- Default value is false，点击对话框以外的页面内容可关闭
                        draggable : true, // <-- Default value is false，可拖拽
                        btnCancelLabel : '取消', // <-- Default value is 'Cancel',
                        btnOKLabel : '确定', // <-- Default value is 'OK',
                        btnOKClass : 'btn-warning', // <-- If you didn't specify it, dialog type
                        size : BootstrapDialog.SIZE_SMALL,
                        // 对话框关闭的时候执行方法
                        callback : function(result) {
                            // 点击确定按钮时，result为true
                            if (result) {
                                // 执行方法
                                // funcok.call();
                                build_task_msg(job_name, assumpt_table, build_task_id, build_branch, program_id, id, index);
                            }
                        }
                    });
                }
                else {
                    if (data.code == 3){
                        toastr.warning("没有找到对应的构建信息", "warning");
                    }
                    build_task_msg(job_name, assumpt_table, build_task_id, build_branch, program_id, id, index);
                }
            },
            error:function (data) {
                toastr.error("程序发生异常，请求联系管理员", "error");
            }
        });
     },

    'click .jenkines_build_cancel': function (e, value, row, index) {
        $.ajax({
            type: "GET",
            url: "/api/build_task/task_cancel/" + row["id"],
            contentType: "application/json; charset=UTF-8",
            success:function (data) {
                if(data.code == 0){
                    $("#tb_assumpt_task").bootstrapTable("updateCell", {index:index, field:"last_build_status", value: 4});
                    toastr.success(data.message, "success");
                }
                else {
                    toastr.warning(data.message, "warning");
                }
            },
            error:function (data) {
                toastr.error("程序发生异常，请求联系管理员", "error");
            }
        });
     },

    'click .story_complete': function (e, value, row, index) {
        BootstrapDialog.confirm({
            title : '确认',
            message : "确定要发布该需求吗？",
            type : BootstrapDialog.TYPE_WARNING, // <-- Default value is
            // BootstrapDialog.TYPE_PRIMARY
            closable : true, // <-- Default value is false，点击对话框以外的页面内容可关闭
            draggable : true, // <-- Default value is false，可拖拽
            btnCancelLabel : '取消', // <-- Default value is 'Cancel',
            btnOKLabel : '确定', // <-- Default value is 'OK',
            btnOKClass : 'btn-warning', // <-- If you didn't specify it, dialog type
            size : BootstrapDialog.SIZE_SMALL,
            // 对话框关闭的时候执行方法
            callback : function(result) {
                // 点击确定按钮时，result为true
                if (result) {
                    // 执行方法
                    // funcok.call();
                    $.ajax({
                        type: "POST",
                        url: "/api/tapd/publish_story",
                        contentType: "application/json; charset=UTF-8",
                        headers: {"X-CSRFToken": pt_csrf_token},
                        data: JSON.stringify({
                            "build_task_id": row.id,
                            "user_name": current_user
                       }),
                        success:function (data) {
                            if(data.code == 0) {
                                toastr.success("发布成功", "success");
                                $("#tb_assumpt_task").bootstrapTable("refresh");
                            }
                            else{
                                toastr.warning("发布失败!" + data.message, "warning");
                            }
                        },
                        error:function (data) {
                            toastr.error("程序发生异常，请求联系管理员", "error");
                        }
                    });
                }
            }
        });

    },

    'click .filter_file': function (e, value, row, index) {
        $("#id_build_task_id").val(row["id"]);
        $.ajax({
            type: "POST",
            url: "/api/build_task/assumpt_task/get_info/",
            contentType: "application/json; charset=UTF-8",
            dataType: 'JSON',
            headers: {"X-CSRFToken": pt_csrf_token,
                    "content-type": "application/json"},
            data: JSON.stringify({
                "attr": "filter_file_value",
                "task_id": row["id"],
           }),
            success:function (data) {
                console.log(data);
                if(data.code == 0){
                    json_dict['json_filter_file_value'].set(data.data);
                }
            },
            error:function (data) {
                toastr.error("程序发生异常，请求联系管理员", "error");
            }
        });

        $("#modify_filter_file").modal("show");

    },

    'click .show_jacoco':function (e, value, row, index) {
        var env = $("#build_env_" + row["id"]).val();
        var index = row["build_branch"].indexOf("/");
        if( index != -1){
            var branch = row["build_branch"].substr(index + 1)
        }
        else {
            branch = row["build_branch"]
        }

        if(row["program_id"] == 10){
            window.open(row["jacoco_url"] + env + "/" + branch + '_new/summary_report.html')
        }
        else{
            if(row["build_task_status"] == 0 || row["last_build_status"] == 1) {
                $.ajax({
                    type: "GET",
                    url: "/api/coverage/is_master_id/" + row["id"],
                    contentType: "application/json; charset=UTF-8",
                    success:function (data) {
                        if(data.code == 0) {
                            window.open('/coverage/' + row["gitlab_program_id"] + '/' + row["build_branch"] + '/' + env + '/' + row["id"])
                        }
                        else{
                            toastr.warning(data.message, "warning");
                        }
                    },
                    error:function (data) {
                        toastr.error("程序发生异常，请求联系管理员", "error");
                    }
                });
            }
            else{
                toastr.warning('未构建成功，暂时获取不到新覆盖率', 'warning');
            }
        }
    },

    'click .show_jacoco_new':function (e, value, row, index) {
        var system = row["gitlab_program_name"];
        var env = $("#build_env_" + row["id"]).val();
        var index = row["build_branch"].indexOf("/");
        if( index != -1){
            var branch = row["build_branch"].substr(index + 1)
        }
        else {
            branch = row["build_branch"]
        }

        if(row["program_id"] == 10){
            window.open(row["jacoco_url"] + env + "/" + branch + '_new/summary_report.html')
        }
        else{
            if(row["build_task_status"] == 0 || row["last_build_status"] == 1) {
                $.ajax({
                    type: "GET",
                    url: "/api/coverage/is_master_id/" + row["id"],
                    contentType: "application/json; charset=UTF-8",
                    success:function (data) {
                        if(data.code == 0) {
                            $.ajax({
                                type: "GET",
                                url: "/api/coverage/jacoco_new/" + row["id"],
                                contentType: "application/json; charset=UTF-8",
                                success:function (data) {
                                    if(data.code == 1) {
                                        window.open(data.data.reportUrl)
                                    }
                                    else{
                                        toastr.warning(data.message, "warning");
                                    }
                                },
                                error:function (data) {
                                    toastr.error(data.message, "error");
                                }

                            });
                        }
                        else{
                            toastr.warning(data.message, "warning");
                        }
                    },
                    error:function (data) {
                        toastr.error("程序发生异常，请求联系管理员", "error");
                    }
                });
            }
            else{
                toastr.warning('未构建成功，暂时获取不到新覆盖率', 'warning');
            }
        }
    },

    'click .show_merge_jacoco':function (e, value, row, index) {
            $("#env_table").bootstrapTable("destroy");
            var options = $("#build_env_" + row["id"] + " option"),
                data = [];
            $.each(options, function (index, item) {
                if(($.isEmptyObject($(item).val()) && index == 0) || $(item).val() == row["last_build_env"]){
                    data.push( {"env_id": $(item).val(), "base": 1})
                }
                else{
                    data.push( {"env_id": $(item).val(), "base": 0})
                }
            });
            if(data.length < 2){
                toastr.warning("the env's count not enough!")
            }
            else {
                $("#jenkins_job_name").val(row["build_jenkins_jobs"][0]["name"]);
                $("#jenkins_task_id").val(row["id"]);
                var env_table = envTable(data);
                env_table.Init();
                $('#merge_jacoco').modal('show');
            }
        },

    'click .modify_branch_info':function (e, value, row, index) {
            $("#modify_branch_index").val(index);
            $("#modify_branch_task_id").val(row.id);
            $("#modify_branch_name").val(row["build_branch"]);
            $.ajax({
                type: "GET",
                url: "/api/build_task/get_task_jenkins/" + row.id,
                contentType: "application/json; charset=UTF-8",
                success:function (data) {
                    if(data.code == 0) {
                        $("#sel_jenkins_job").empty();
                        $.each(data.data, function (index, item) {
                             $("#sel_jenkins_job").append('<option>' + item + '</option>');
                        });
                        $("#sel_jenkins_job").selectpicker('refresh');
                        $("#sel_jenkins_job").selectpicker('render');
                        $('#modify_branch_info').modal('show');
                    }
                    else{
                        toastr.warning("获取Jenkins任务异常" + data.message, "warning");
                    }
                },
                error:function (data) {
                    toastr.error("程序发生异常，请求联系管理员", "error");
                }
            });

        },

    'click .set_base_jacoco': function (e, value, row, index) {
            var all_data = $("#env_table").bootstrapTable("getData"),
                new_data = new Array();
            for (var item in all_data) {
                var base = 0;
                if(item == index){
                    base = 1;
                }
                new_data.push({
                    "base": base,
                    "env_id": all_data[item]["env_id"],
                    "build_branch": all_data[item]["build_branch"]
                })
            }
            $("#env_table").bootstrapTable("destroy");
            var env_table = envTable(new_data);
            env_table.Init();
            $("#env_table").bootstrapTable("refresh");
        },
};

function build_task_msg(job_name, assumpt_table, build_task_id, build_branch, program_id, id, index) {
    if (job_name == "cd_biz_dcs_jacoco"){
        show_dcs_modal(assumpt_table, build_task_id, build_branch, program_id, id, index);
    }
    else if (job_name.indexOf("FS_OA") > 0) {
        show_oa_modal(assumpt_table, build_task_id, build_branch, program_id, id, index);
    }
    // else if (job_name == "cd_biz_central_jacoco") {
    //     show_central_modal(assumpt_table, build_task_id, build_branch, program_id, id, index)
    // }
    else {
        create_build_task(assumpt_table, build_task_id, build_branch, program_id, id, index, extend=1);
    }
}

function set_modal_data(assumpt_table, build_task_id, build_branch, program_id, id, index) {
    $("#id_assumpt_table").val(assumpt_table);
    $("#id_build_task_id").val(build_task_id);
    $("#id_build_branch").val(build_branch);
    $("#id_program_id").val(program_id);
    $("#id_id").val(id);
    $("#id_index").val(index);
}


function show_central_modal(assumpt_table, build_task_id, build_branch, program_id, id, index) {
     set_modal_data(assumpt_table, build_task_id, build_branch, program_id, id, index);
    $("#merge_central_sel").modal("show");
}


function show_dcs_modal(assumpt_table, build_task_id, build_branch, program_id, id, index) {
    set_modal_data(assumpt_table, build_task_id, build_branch, program_id, id, index);
    $("#merge_dcs_sel").modal("show");
}


function show_oa_modal(assumpt_table, build_task_id, build_branch, program_id, id, index) {
    set_modal_data(assumpt_table, build_task_id, build_branch, program_id, id, index);
    var build_branch_list = build_branch.split(",");
    $.each($(".oa-sel-list select"), function (index, item) {
        if($(item).find("option").length > 1){
            var can_change = true;

            $.each($(item).find("option"), function (index, opt) {
                $.each(build_branch_list, function (branch_index, each_build_branch) {
                    if(each_build_branch == $(opt).val()){
                       can_change = false;
                    }
                });
            });
            if(can_change){
                 $(item).find("option").last().remove();
                 $.each(build_branch_list, function (branch_index, each_build_branch) {
                    $(item).append('<option value="' + each_build_branch + '">' + each_build_branch + '</option>');
                });
            }
        }else{
            $.each(build_branch_list, function (branch_index, each_build_branch) {
                $(item).append('<option value="' + each_build_branch + '">' + each_build_branch + '</option>');
            });
        }
        $(item).selectpicker('refresh');
    });
    $("#merge_oa_sel").modal("show");
}

var envTable = function (data) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#env_table').bootstrapTable({
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
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 20],        //可供选择的每页的行数（*）
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
            detailView: false,                   //是否显示父子表,
            columns: [{
                checkbox: true,
            }, {
                field: 'env_id',
                title: '环境',
                align:'left'
            }, {
                title: '基准环境',
                formatter: function(value, row, index){
                    if(row["base"] == 1){
                        return "是"
                    }
                    else {
                        return "否"
                    }
                },
                align:'left'
            },{
                field: 'operate',
                title: '操作',
                events: operateEvents,
                formatter: setBaseJacoco,
                align:'left'
            }]
        });
    };

    function setBaseJacoco(value, row, index) {
        if(row["base"] == 1){
            return ""
        }
        else{
            return [
                    '<a class="set_base_jacoco" style="cursor: pointer" href="javascript:void(0)" title="设置为基准环境">',
                    '<span>设置为基准环境</span>',
                    '</a>',

                ].join('');
        }
    }
    return oTableInit;
};
$("#btn_merge_jacoco_save").click(function () {
    var check_data = $("#env_table").bootstrapTable("getSelections");
    if(check_data.length < 2 ){
        toastr.warning("合并jacoco至少两个环境", "warning")
    }else{
        var test_env = new Array(),
            has_base = false;
        for(var index in check_data){
            if(check_data[index]["base"] == 1){
                has_base = true;
                test_env.unshift(check_data[index]["env_id"]);
            }else {
                test_env.push(check_data[index]["env_id"])
            }
        }
        if(!has_base){
            toastr.warning("合并的环境中没有基准环境", "warning");
        }else {
            $("#btn_merge_jacoco_save").attr("disabled","disabled");
            $.ajax({
                url: "/api/coverage/merge/coverage",
                type: "POST",
                dataType: 'JSON',
                headers: {"X-CSRFToken": pt_csrf_token,
                            "content-type": "application/json"},
                data: JSON.stringify({
                    "jenkins_job": $("#jenkins_job_name").val(),
                    "env": test_env,
                    "task": $("#jenkins_task_id").val()
                }),
                success: function (data) {
                    if (data.code == 0) {
                        $("#btn_merge_jacoco_cancel").click();
                        window.open(data.url);
                    } else {
                        toastr.warning(data.msg, "warning")
                    }
                    $("#btn_merge_jacoco_save").removeAttr("disabled");
                },
                error: function () {
                    $("#btn_merge_jacoco_save").removeAttr("disabled");
                }
            });
        }
    }

});


$("#btn_assumput_task_build").click(function () {
    var assumpt_table = $("#id_assumpt_table").val(),
        build_task_id = $("#id_build_task_id").val(),
        build_branch = $("#id_build_branch").val(),
        program_id = $("#id_program_id").val(),
        id = $("#id_id").val(),
        index = $("#id_index").val();
    var extend = {"captinal" : $("#txt_dcs_capital").val(),
                "biz" : $("#txt_dcs_biz").val()
                    };
    create_build_task(assumpt_table, build_task_id, build_branch, program_id, id, index,extend=extend);
    $("#btn_assumput_task_cancel").click();
});
function get_reverse_json_value(data) {
            if ($.isEmptyObject(data)) {
                return "";
            } else {
                return JSON.stringify(data);
            }
        }

$("#btn_modify_filter").click(function () {
    var build_task_id = $("#id_build_task_id").val(),
        index = $("#id_index").val(),
        filter_file_value = json_dict['json_filter_file_value'].get(),
        task_param = JSON.stringify({
            "task_id": build_task_id,
            "filter_file_value": filter_file_value
        });
    console.log("task_param", task_param);
    $.ajax({
        url: "/api/build_task/assumpt_task/update/",
        type: "POST",
        dataType: 'JSON',
        headers: {"X-CSRFToken": pt_csrf_token,
                    "content-type": "application/json"},
        data: task_param,
        success: function (data) {
            if (data.code == 0) {
                $("#btn_branch_info_cancel").click();
            } else {
                toastr.warning(data.msg, "warning")
            }
        }
    });
    $("#btn_modify_filter_cancel").click();
});

$("#btn_central_assumput_task_build").click(function () {
    var assumpt_table = $("#id_assumpt_table").val(),
        build_task_id = $("#id_build_task_id").val(),
        build_branch = $("#id_build_branch").val(),
        program_id = $("#id_program_id").val(),
        id = $("#id_id").val(),
        index = $("#id_index").val();
    var extend = {"biz_database" : $("#txt_central_biz").val()};
    create_build_task(assumpt_table, build_task_id, build_branch, program_id, id, index,extend=extend);
    $("#btn_central_assumput_task_cancel").click();
});

$("#btn_oa_assumput_task_build").click(function () {
    var assumpt_table = $("#id_assumpt_table").val(),
        build_task_id = $("#id_build_task_id").val(),
        build_branch = $("#id_build_branch").val(),
        program_id = $("#id_program_id").val(),
        id = $("#id_id").val(),
        index = $("#id_index").val();
    var extend = {};
    $.each(oa_modals.split("&#39;"), function (index, item) {
        if(item.indexOf("oa") == 0){
            extend[item.replace("-v2", "").replace("app-", "").replace("oa-", "")] = $("#txt_" + item).val();
        }
    });
    console.log("extend", extend);
    create_build_task(assumpt_table, build_task_id, build_branch, program_id, id, index,extend=extend);
    $("#btn_oa_assumput_task_cancel").click();
});


$("#btn_branch_info_save").click(function () {
    var index = $("#modify_branch_index").val(),
        task_id = $("#modify_branch_task_id").val();
    $.ajax({
        url: "/api/build_task/update",
        type: "POST",
        dataType: 'JSON',
        headers: {"X-CSRFToken": pt_csrf_token,
                    "content-type": "application/json"},
        data: JSON.stringify({
            "task_id": task_id,
            "branch": $("#modify_branch_name").val(),
            "jenkins_job": $("#sel_jenkins_job").val()
        }),
        success: function (data) {
            if (data.code == 0) {
                $("#tb_assumpt_task").bootstrapTable("updateRow", {index:index, row:data.data});
                $("#btn_branch_info_cancel").click();
            } else {
                toastr.warning(data.msg, "warning")
            }
        }
    });

});

$("#btn_qualty_info_save").click(function () {
    $.ajax({
        url: "/api/quality_info/update/",
        type: 'POST',
        headers: {"X-CSRFToken": pt_csrf_token,
                    "content-type": "application/json"},
        data: JSON.stringify({
            "task_id": $("#build_task_id").val(),
            "story_change_count": $("#txt_story_change_count").val(),
            "smoke_count": $("#txt_smoke_count").val(),
            "reason": $("#txt_reason").val(),
            "level": $("#sel_quality_info_level").val(),
            "operator": current_user
        }),
        dataType: "json",
        success:function (data) {
            if(data.code == 0){
                toastr.success("success", "更新成功");
                $("#btn_qualty_info_cancel").click();
            }
            else {
                toastr.warning("warning", "更新失败");
            }
        },
        error:function () {
            toastr.error("error", "更新异常");
        }
    });
});


