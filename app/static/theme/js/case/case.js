
$(function () {
    init_search();
    setTimeout(function () {
        //1.初始化Table
        //if(is_first_init()==true) {
        //    search_summary_data(bind_summary_data);
        //    $('#modal_case_summary').click();
        //};
        var oTable = new TableInit();
        oTable.Init();

        $(window).resize(function (){
            var page_height = $(window).height();
            $( '#tb_case' ).bootstrapTable('resetView',{ height: page_height - 50 } );
    });

    }, 100);

    var program = get_cache("case_sel_program");
    if (!$.isEmptyObject(program)){
        $.each($(".case_program li"), function () {
            var pro_list = $(this).find("a").attr("id").split("_"),
                pro = pro_list[pro_list.length - 1];
            if(pro == program){
                $(this).addClass("active");
                $("#tb_case").bootstrapTable("refresh");
            }
            else{
                $(this).removeClass("active")
            }
        });
    }

    $(".case_header_ul.dropdown-menu a").click(function () {
        var sel_str = $("#dropdownMenu1").html(),
            display_str = $(this).html();
        if(sel_str.indexOf(display_str) <= -1){
            $("#dropdownMenu1").html('<i class="case_header_i fa fa-link"></i>' + display_str +
                '                <span class="caret"></span>');
            setTimeout(function () {
            $("#tb_case").bootstrapTable("refresh");
        }, 100);
        }

    });

    $(".case_program li").click(function () {
        $(".case_program li").removeClass("active");
        $(this).addClass("active");
        var pro_list = $(this).find("a").attr("id").split("_"),
                pro = pro_list[pro_list.length - 1];
        save_cache("case_sel_program", pro);
        setTimeout(function () {
            $("#tb_case").bootstrapTable("refresh");
        }, 100);
    });

    $("#txt_case_from_system").on("changed.bs.select", function (e) {
        save_cache("search_case_from_system", $(this).val());
        refresh_business();
    });

    $("#txt_case_device").on("changed.bs.select", function (e) {
        save_cache("search_case_device", $(this).val());
    });

    $("#sel_case_belong_business").on("changed.bs.select", function (e) {
        save_cache("search_case_belong_business", $(this).val());
    });

    $("#btn_copy_all").click("bind", copy_selected_cases);

});

function save_cache(key, value) {
    localStorage.setItem(key, value);
}

function get_cache(key) {
    return localStorage.getItem(key);
}

function init_search() {
    var case_from_system = get_cache("search_case_from_system");
    var case_device = get_cache("search_case_device");
    var case_belong_business = get_cache("search_case_belong_business");
    if (case_from_system != ""){
        $("#txt_case_from_system").val(case_from_system);
        $("#txt_case_from_system").selectpicker("refresh");
    }
    if (case_device != ""){
        $("#txt_case_device").val(case_device);
        $("#txt_case_device").selectpicker("refresh");
    }
    if (case_belong_business != ""){

        //while ()
        refresh_business();
        setTimeout(function () {
            $("#sel_case_belong_business").val(case_belong_business);
            $("#sel_case_belong_business").selectpicker("refresh");
        }, 100);
    }


}

function refresh_business(){
    var system = $("#txt_case_from_system").val();
    var program_business = eval("{{ program_business }}");
    $("#sel_case_belong_business").empty();
    var options = "<option value=''>全部</option>";
    console.log(program_business);
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
    $("#sel_case_belong_business").append(options);
    $("#sel_case_belong_business").selectpicker("refresh");

}

function copy_selected_cases() {
    var allcases = $("#tb_case").bootstrapTable("getAllSelections");
    var cases = new Array();
    for(var index in allcases){
        cases.push(allcases[index]["case_id"]);
    }
    if(cases.length  == 0)
    {
        toastr.warning("warning", "至少勾选一个用例！");
    }
    else {
        $(this).text('批量复制中，请稍等！');
        $(this).attr("disabled", "disabled");
        $("#copying").removeClass("hidden");
        $(this).addClass("copy_cases");

        $.ajax({
            type: "POST",
            url: "/api/case/case/copy_all",
            data: JSON.stringify({
                "cases": cases,
                "author":current_user
            }),
            headers: {
                "X-CSRFToken": csrf_token,
                "content-type": "application/json"
            },
            dataType: 'JSON',
            success: function (data) {
                if (data["code"] == 1) {
                    toastr.warning("warning", "批量复制用例失败");
                }
                else {
                    toastr.success("success", "批量复制用例成功");
                    $("#tb_case").bootstrapTable("refresh");
                }
            },
            error: function () {
                toastr.error("error", "批量复制用例异常");
            },
            complete: function () {
                $("#btn_copy_all").text("批量复制");
                $("#btn_copy_all").attr("disabled", false);
                $("#btn_copy_all").removeClass("copy_cases");
                $("#copying").addClass("hidden");
            }
        })
    }
}

var TableInit = function () {
    var oTableInit = new Object();

    // 初始化子表格
    oTableInit.InitSubTable = function (index, row, $detail) {
        var case_exec_group = row.case_exec_group;
        if($.isEmptyObject(case_exec_group)==true){
            return
        }
        var case_from_system = row.case_from_system

        var case_exec_group_priority = "sub";
        var cur_table = $detail.html('<table id="tb_' + row.case_exec_group +  '"></table>').find('table');
        $(cur_table).bootstrapTable({
            url: '/api/case/search/',
            method: 'get',
            striped: true,
            queryParams: {  case_exec_group: case_exec_group ,
                            case_exec_group_priority: case_exec_group_priority,
                            case_from_system :case_from_system,
                            page_index: 1,
                            page_size: 2000},
            clickToSelect: true,
            detailView: false,//父子表
            pageSize: 20,
            classes: "table-no-bordered table table-hover table-striped",
            columns: [{
            //    checkbox: true
            //}, {
                field: 'operate',
                title: '操作',
                events: operateEvents,
                formatter: casesubFormatter,
                class: 'W90',
            }, {
                field: 'case_id',
                title: 'ID',
                align:'left'
            }, {
                field: 'case_name',
                title: '用例名称',
                align:'left'
            }, {
                field: 'case_description',
                title: '用例描述',
                align:'left'
            }, {
                field: 'case_from_system_name',
                title: '用例系统',
                align: 'left'
            }, {
                field: 'case_executor',
                title: '用例类型',
                align: 'left',
                formatter: caseexecutorFormatter,
            }, {
                field: 'case_exec_priority',
                title: '优先级',
                align: 'left',
                editable: {
                type: 'text',
                title: '优先级',
                validate: function (v) {
                    if (!v) {
                        return '优先级不能为空';
                    }
                }
            }
            }, {
                field: 'case_exec_count',
                title: '循环次数',
                align: "center",
                editable: {
                type: 'text',
                title: '循环次数',
                validate: function (v) {
                    if (!v) {
                        return '循环次数不能为空';
                    }
                }
            }
            }, {
                field: 'case_is_exec',
                title: '是否执行',
                align: "center",
                editable: {
                type: 'select',
                title: '是否执行',
                source:[
                    {value:"1",text:"是"},
                    {value:"0",text:"否"}
                ]
            }
            }, {
                field: 'case_exec_group',
                title: '复杂分组',
                align: 'left'
            },],
            onEditableSave: function (field, row, oldValue, $el) {

                var last_edit_user = current_user;
                var case_data = JSON.stringify({
                    "case":{
                        "basicInfo":{
                            "case_id":row['case_id'],
                            "case_exec_priority": row['case_exec_priority'],
                            "case_from_system":row['case_from_system'],
                            "case_name": row['case_name'],
                            "case_description": row['case_description'],
                            "case_category": row['case_category'],
                            "case_executor": row['case_executor'],
                            "case_exec_group": row['case_exec_group'],
                            "case_exec_group_priority": row['case_run_group_property'],
                            "case_api_address": row['case_api_address'],
                            "case_api_method": row['case_api_method'],
                            "case_api_params": get_reverse_json_value(row['case_api_params']),
                            "case_api_header": get_reverse_json_value(row['case_api_header']),
                            "case_check_method": row['case_check_method'],
                            "case_except_value": get_reverse_json_value(row['case_except_value']),
                            "case_sql_actual_statement": row['case_sql_actual_statement'],
                            "case_sql_actual_database": row['case_sql_actual_database'],
                            "case_sql_params": get_reverse_json_value(row['case_sql_params']),
                            "case_ref_tapd_id": row['case_ref_tapd_id'],
                            "case_is_exec": row['case_is_exec'],
                            "case_mock_flag":row['case_mock_flag'],
                            "case_next_msg":row['case_next_msg'],
                            "case_next_task":row['case_next_task'],
                            "case_replace_expression":get_reverse_json_value(row['case_replace_expression']),
                            "case_wait_time":row['case_wait_time'],
                            "case_vars_name":row['case_vars_name'],
                            "case_last_user":last_edit_user,
                            "case_exec_count":row["case_exec_count"]
                        }
                    }
                });

                $.ajax({
                    type: "PUT",
                    url: "/api/case/case/",
                    headers: {"X-CSRFToken":csrf_token,
                            "content-type": "application/json"},
                    data: case_data,
                    dataType: 'JSON',
                    success: function (data) {
                        if (data["code"] == 1) {
                            toastr.warning("warning", "更新数据失败，请求联系管理员");
                        }

                        else {
                            toastr.success("success", "更新数据成功");
                        }
                    },
                    error: function () {
                        $("#update_warning").text("网络异常，请求失败");
                        $("#update_warning").show()
                    },
                    complete: function () {

                    }

                });
            }
        });
    };

    //初始化Table
    oTableInit.Init = function () {
        var page_scroll = $(window).height();
        $('#tb_case').bootstrapTable({
            url: '/api/case/search/',         //请求后台的URL（*）
            method: 'GET',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            toolbarAlign: "right",
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
            pageSize: 20,                       //每页的记录行数（*）
            pageList: [20, 50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            height: page_scroll - 50,
            strictSearch: true,
            showColumns: false,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: false,                //是否启用点击选中行
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: true,                   //是否显示父子表
            onExpandRow:  function (index, row, $detail) {
                oTableInit.InitSubTable(index, row, $detail);
            },
            columns: [{
                checkbox: true
            },{
                field: 'operate',
                title: '操作',
                events: operateEvents,
                formatter: caseFormatter,
                class: 'W120',
            }, {
                field: 'case_id',
                title: 'ID',
                visible: true,
            }, {
                field: 'case_ref_tapd_id',
                title: 'TAPD_ID',
                align:'left'
            }, {
                field: 'case_name',
                title: '用例名称',
                align:'left',
                class: 'col_name',
                formatter: showNameFormatter,
            }, {
                field: 'case_description',
                title: '用例描述',
                align:'left',
                class: 'col_name',
                formatter: showNameFormatter,
            }, {
                field: 'case_from_system_name',
                title: '用例系统',
                align: 'left'
            }, {
                field: 'case_executor',
                //title: '执行器',
                title: '用例类型',
                align: 'left',
                formatter: caseexecutorFormatter,

            }, {
                field: 'case_belong_business_name',
                title: '所属业务',
                align: 'left',
                class: 'W140',
            }, {
                field: 'case_exec_count',
                title: '循环次数',
                align: "center",
                editable: {
                type: 'text',
                title: '循环次数',
                validate: function (v) {
                    if (!v) {
                        return '循环次数不能为空';
                    }
                }
            }
            }, {
                field: 'case_is_exec',
                title: '是否执行',
                align: "center",
                editable: {
                type: 'select',
                title: '是否执行',
                source:[
                    {value:"1",text:"是"},
                    {value:"0",text:"否"}
                ]
            }

            }, {
                field: 'case_exec_group',
                title: '复杂用例名称',
                align: 'left',
                class: 'col_name',
                editable: {
                type: 'text',
                emptytext:"",
                tpl:'<textarea cols="30"></textarea>',
                title: '修改复杂用例名称',
                validate: function (v) {
                    if (!v) {
                        return '复杂用例名称不能为空';
                    }
                    else {
                        var ret = "";
                        $.ajax({
                            type: "GET",
                            url: "/api/case/check_group",
                            data: {
                              "group_name": v
                            },
                            async: false,
                            success:function (data) {
                                console.log(data);
                                if (data.code == 1){
                                    ret = '该复杂用例名称已存在';
                                }
                            },
                            error:function () {
                                ret = '程序异常';
                            }
                        });
                        console.log("finisded");
                        if(ret != ""){
                            return ret;
                        }
                    }
                }
            },
                formatter: showNameByEdit
            },], onEditableSave: function (field, row, oldValue, $el) {
                var last_edit_user = current_user;
                var case_data = JSON.stringify({
                    "last_edit_user": last_edit_user,
                    "case_exec_group": row["case_exec_group"],
                    "case_is_exec": row["case_is_exec"],
                    "case_id": row["case_id"],
                    "case_exec_count": row["case_exec_count"],
                    "flag": field
                });
                $.ajax({
                        type: "PUT",
                        url: "/api/case/case/",
                        headers: {"X-CSRFToken": csrf_token,
                                "content-type": "application/json"},
                        data: case_data,
                        dataType: 'JSON',
                        success: function (data) {
                            if (data["code"] == 1) {
                                if(field == "case_exec_group"){
                                    $el.text(oldValue);

                                }
                                toastr.warning(data["msg"], "warning");
                            }
                            else {
                                toastr.success("更新成功", "success");
                            }
                        },
                        error: function () {
                            toastr.error("网络异常，请求失败", "error");
                        },
                        complete: function () {

                        }

                    });
                }

        });
    };

    oTableInit.subqueryParams = function(params){
      var temp = {

      }
      return temp;
    };
    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var program_id = $(".case_program_item.active a").attr("id").split("_"),
            id = program_id[program_id.length - 1],
            actor = current_user;
        if($("#dropdownMenu1").html().indexOf("所有的") > -1) {
            actor = "";
        }
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            case_from_system: id,
            case_description: $("#txt_case_description").val().trim(),
            case_name: $("#txt_case_name").val().trim(),
            case_id: $("#txt_case_id").val().trim(),
            case_is_exec: $("#is_run").val(),
            case_executor: $("#txt_case_device").val().trim(),
            case_exec_group:$("#txt_case_exec_group").val().trim(),
            case_actor: actor,
            case_belong_business: $("#sel_case_belong_business").val(),
            //case_exec_priority:$("#txt_case_exce_priority").val().trim(),
            //case_exec_group_priority: "main",
            page_index: (params.offset / params.limit) + 1,
            page_size: params.limit,
        };

        if(!$.isEmptyObject(temp["case_id"])){
            temp["case_from_system"] = "";
            temp["case_belong_business"] = "";
            temp["case_executor"] = "";
            temp["case_is_exec"] = "";
        }

        return temp;
    };

    function caseexecutorFormatter(value, row, index) {
        var ret;
        if (value == "common"){
            ret = "简单场景";
        }
        else if (value == "group"){
            ret = "复杂场景";
        }
        return ret
    };

    function showNameByEdit(value, row, index) {
        return value
    };

    function showNameFormatter(value, row, index) {
        return "<div style='width:300px;text-overflow: ellipsis;overflow: hidden;'>" + value + "</div>"
    }
    return oTableInit;
};

function jsonFormatter(value, row, index) {
        return "<pre style='white-space: pre-wrap;border:0px;background-color: transparent;'>"+JSON.stringify(value, null, 2)+"</pre>"
    };

function casesubFormatter(value, row, index) {
    return [
        '<a class="case_update" style="cursor: pointer" href="case/' + row.case_id + '/" target="_blank" title="编辑">',
        '<span class=\'glyphicon glyphicon-pencil\'></span>',
        '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
        '<a class="case_delete"  style="cursor: pointer" href="javascript:void(0)"   title="删除">',
        '<span class=\'glyphicon glyphicon-remove\'></span>',
        '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
        '<a class="case_sub_copy"  style="cursor: pointer" href="javascript:void(0)"   title="复制">',
        '<span class=\'glyphicon glyphicon-file\'></span>',
        '</a>',

    ].join('');
};

function caseFormatter(value, row, index) {
    return [
        '<a class="case_exec" href="javascript:void(0)" title="执行">',
        '<span class=\'glyphicon glyphicon-play\'></span>',
        '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
        '<a class="case_update" style="cursor: pointer" href="case/' + row.case_id + '/" target="_blank" title="编辑">',
        '<span class=\'glyphicon glyphicon-pencil\'></span>',
        '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
        '<a class="case_delete"  style="cursor: pointer" href="javascript:void(0)"   title="删除">',
        '<span class=\'glyphicon glyphicon-remove\'></span>',
        '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
        '<a class="case_group_copy"  style="cursor: pointer" href="javascript:void(0)"   title="复制">',
        '<span class=\'glyphicon glyphicon-file\'></span>',
        '</a>',
    ].join('');
};

$("#btn_query").click(function () {
    $("#tb_case").bootstrapTable('selectPage', 1);
    $("#tb_case").bootstrapTable("refresh");
});

$(document).keydown(function (event) {
    if (event.keyCode == 13) {
        $('#btn_query').triggerHandler('click');
    }
});

$("#btn_reset").click(function () {
    $("#txt_case_from_system").val("");
    $("#txt_case_description").val("");
    $("#txt_case_name").val("");
    $("#txt_case_id").val("");
    $("#txt_case_device").val("");
    $("#is_run").val("是");
    $("#txt_case_exec_group").val("");
    $("#sel_case_exce_group_priority").selectpicker('val','');
    //$("#tb_case").bootstrapTable('refresh');
});

function get_sel_program() {
    var pro = "";
    $(".case_program li").each(function () {
        if($(this).hasClass("active")){
            var pro_list = $(this).find("a").attr("id").split("_");
            pro = pro_list[pro_list.length - 1];
            return false
        }
    });
    return pro;
}
$("#btn_exec").click(function () {
    var row = $.map($('#tb_case').bootstrapTable('getSelections'), function (row) {
        return row;
    });
    var case_ids = new Array(),
        task_system = get_sel_program();
    for (var i in row) {
        case_ids.push(row[i]['case_id'])
    }

    var run_case = JSON.stringify({
        "task_ids": case_ids,
        "task_title": row[0]["case_name"] + "_group_debug_" + (Date.parse(new Date()) / 1000).toString(),
        "debug": true,
        "task_business": $("#sel_case_belong_business").val(),
        "task_system": task_system,
        "task_create_user": current_user
    });

    $.ajax({
        url: '/api/task/create',
        headers: {"X-CSRFToken": csrf_token},
        contentType: "application/json; charset=UTF-8",
        type: 'POST',
        data: run_case,
        success: function (data) {
            if (data["code"] == 1) {
                toastr.error("error", data["msg"]);
            }
            else {
                toastr.success("success", "创建并运行成功");
                save_cache("auto_exec", data.task_id);
                save_cache("auto_exec_program", task_system);
                $(location).attr('href', "/tasks/list");

            }
            $("#btn_create_task").removeAttr("disabled");
        },
        error: function (e) {
            toastr.warning("warning", e.msg);
            $("#btn_create_task").removeAttr("disabled");
        }
    });

});

window.operateEvents = {
    'click .case_delete': function (e, value, row, index) {
        $.ajax({
            type: "DELETE",
            headers: {"X-CSRFToken": csrf_token},
            url: "/api/case/case/delete/" + row['case_id'],
            contentType: "application/json; charset=UTF-8",
            success: function (data) {

                if (data.code != 0) {
                    toastr.error("error", "程序发生异常，请求联系管理员");
                    return;
                }
                if ($("#tb_" + row['case_exec_group']).length > 0) {
                    $("#tb_" + row['case_exec_group']).bootstrapTable('remove', {
                        field: 'case_id',
                        values: [row['case_id']]
                    });
                    $("#tb_" + row['case_exec_group']).bootstrapTable('refresh');
                }
                else {
                    $("#tb_case").bootstrapTable('remove', {
                        field: 'case_id',
                        values: [row['case_id']]
                    });
                    $("#tb_case").bootstrapTable('refresh');
                }
                toastr.success("success", "删除成功");
            }
        });
    },

    'click .case_exec': function (e, value, row, index) {
        var case_ids = new Array();
        case_ids.push(row['case_id']);

        var run_case = JSON.stringify({
            "task_ids": case_ids,
            "task_title": row["case_name"] + "_debug_" + (Date.parse(new Date()) / 1000).toString(),
            "debug": true,
            "task_business": row["case_belong_business"],
            "task_system": row["case_from_system"],
            "task_create_user": current_user,
        });
        $.ajax({
            url: '/api/task/create',
            headers: {"X-CSRFToken": csrf_token},
            contentType: "application/json; charset=UTF-8",
            type: 'POST',
            data: run_case,
            success: function (data) {
                if (data["code"] == 1) {
                    toastr.error("error", data["msg"]);
                }
                else {
                    toastr.success("success", "创建并运行成功");
                    save_cache("auto_exec", data.task_id);
                    save_cache("auto_exec_program", row["case_from_system"]);
                    $(location).attr('href', "/tasks/list");

                }
                $("#btn_create_task").removeAttr("disabled");
            },
            error: function (e) {
                toastr.warning("warning", e.msg);
                $("#btn_create_task").removeAttr("disabled");
            }
        });
    },
    'click .case_group_copy': function (e, value, row, index) {
        var copy_group = {
            "case_id": row['case_id'],
            "case_from_system": row['case_from_system'],
            "case_exec_group": row['case_exec_group'],
            "case_author": current_user
        }
        $.ajax({
            type: "POST",
            headers: {"X-CSRFToken": csrf_token},
            url: "/api/case/copy/group",
            contentType: "application/json; charset=UTF-8",
            data: JSON.stringify(copy_group),
            success: function (data) {
                if (data.code != 0) {
                    toastr.error("error", data.message);
                    return;
                }
                $("#tb_case").bootstrapTable('selectPage', 1);
                toastr.success("success", "复制成功");

            }
        });

    },

    'click .case_sub_copy': function (e, value, row, index) {
        var copy_group = {
            "case_id": row['case_id'],
            "case_from_system": row['case_from_system'],
            "case_exec_group": row['case_exec_group'],
            "case_author": current_user,
            "case_run_group_property": row["case_exec_group_priority"]
        };
        $.ajax({
            type: "POST",
            headers: {"X-CSRFToken": csrf_token},
            url: "/api/case/copy/group",
            contentType: "application/json; charset=UTF-8",
            data: JSON.stringify(copy_group),
            success: function (data) {
                if (data.code != 0) {
                    toastr.error("error", data.message);
                    return;
                }
                $("#tb_case").bootstrapTable('selectPage', 1);
                toastr.success("success", "复制成功");

            }
        });


    }
};
