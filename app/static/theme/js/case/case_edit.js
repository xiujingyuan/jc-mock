$(function () {
    var case_belong_business = "",
        options = {
        mode: "code",
        sortObjectKeys: false
    },
        reg_marks = new RegExp("&#39;", "g"),//g,表示全部替换。
        reg_rmarks = new RegExp("&#34;", 'g'),
        reg_none = new RegExp("None", "g"),//g,表示全部替换。
        reg_enter = new RegExp("&lt;&gt;", "g"),//g,表示全部替换。
        reg_boolean_true = new RegExp("True", "g"),
        reg_boolean_false = new RegExp("False", "g"),
        json = {},
        json_list = ['json_case_expect', 'json_case_replace', 'json_case_request_args',
        'json_init_request_args', 'json_init_replace', 'json_pre_request_args',
        'json_pre_http_replace', 'json_pre_replace', 'json_pre_sql_args', 'json_pre_expect', 'json_init_sql_args',
        'json_sql_mock_expect', 'json_sql_mock_replace', 'json_http_mock_expect', 'json_http_mock_replace',
        'json_init_sql_replace', 'json_pre_sql_replace', 'json_public_replace', 'json_user_args',
        'json_case_sql_args', 'json_case_sql_replace', 'json_init_edit_request_args', 'json_init_edit_replace',
        'json_init_edit_sql_args', 'json_init_edit_sql_replace', 'json_edit_pre_request_args',
        'json_edit_pre_http_replace', 'json_edit_pre_sql_args', 'json_edit_pre_sql_replace',
        'json_edit_pre_user_args', 'json_edit_pre_replace', 'json_edit_pre_expect', 'json_edit_public_replace', 'sel_request_header'];
    for (var json_name in json_list) {
        var container = document.getElementById(json_list[json_name]);
        var json_edit = new JSONEditor(container, options, json);
        json_dict[json_list[json_name]] = json_edit;
    }
    $("[data-toggle='tooltip']").tooltip();
    load_case(case_id, bind_data_control, init_select);
    var pre_table = new PreTableInit();
    pre_table.Init();

    var init_table = new AddTableInit();
    init_table.Init();

    $(".content-edit-show").css("height", $(window).height() - 180);

    $(window).resize(function (){
            $( '#tb_edit_init' ).bootstrapTable('resetView',{ height: $(window).height() - 250 } );
            $( '#tb_edit_pre' ).bootstrapTable('resetView',{ height: $(window).height() - 250 } );
            $(".content-edit-show").css("height", $(window).height() - 180);
    });

});

window.operateEvents = {
        'click .update_prev_delete': function (e, value, row, index) {
            $.ajax({
                type: "DELETE",
                headers: {"X-CSRFToken": csrf_token},
                url: "/api/case/case_prev_edit/delete/" + row['prev_id'],
                contentType: "application/json; charset=UTF-8",
                success: function (data) {
                    if (data.code != 0) {
                        toastr.error("error", "程序发生异常，请求联系管理员");
                        return;
                    }
                    toastr.success("success", "删除成功");

                    $("#tb_edit_pre").bootstrapTable('remove', {
                        field: 'prev_id',
                        values: [row['prev_id']]
                    });

                }
            });

        },
        'click .update_prev_update': function (e, value, row, index) {
            $.ajax({
                type: "GET",
                headers: {"X-CSRFToken": csrf_token},
                url: "/api/case/case_prev_edit/" + row['prev_id'],
                contentType: "application/json; charset=UTF-8",
                success: function (data) {
                    if (data.code != 0) {
                        toastr.info("info", data.message);
                        return;
                    }
                    bind_pre_data(data.data, index, 'update', $("#txt_case_description").val());
                    $("#btn_edit_prev").click()

                }
            });

        },
        'click .update_prev_copy': function (e, value, row, index) {
            var copy_data = {};
            for (var key in row) {
                if (typeof row[key] == "object") {
                    copy_data[key] = JSON.stringify(row[key]);
                } else {
                    copy_data[key] = row[key];
                }

            }
            var copy_data_str = JSON.stringify(copy_data);
            $.ajax({
                type: "POST",
                headers: {"X-CSRFToken": csrf_token},
                url: "/api/case/prev/add",
                contentType: "application/json; charset=UTF-8",
                data: copy_data_str,
                success: function (data) {
                    if (data.code != 0) {
                        toastr.info("info", data.message);
                        return;
                    }
                    toastr.success("success", '复制成功');
                    $("#tb_edit_pre").bootstrapTable('insertRow', {
                        index: 0,
                        row: data.origin_data
                    });

                }
            });
        },
        'click .update_init_delete': function (e, value, row, index) {
            $.ajax({
                type: "DELETE",
                headers: {"X-CSRFToken": csrf_token},
                url: "/api/case/case_init_edit/delete/" + row['case_init_id'],
                contentType: "application/json; charset=UTF-8",
                success: function (data) {
                    if (data.code != 0) {
                        toastr.error("error", "程序发生异常，请求联系管理员");
                        return;
                    }
                    toastr.success("success", "删除成功");

                    $("#tb_edit_init").bootstrapTable('remove', {
                        field: 'case_init_id',
                        values: [row['case_init_id']]
                    });

                }
            });
        },
        'click .update_init_update': function (e, value, row, index) {
            $.ajax({
                type: "GET",
                headers: {"X-CSRFToken": csrf_token},
                url: "/api/case/case_init_edit/" + row['case_init_id'],
                contentType: "application/json; charset=UTF-8",
                success: function (data) {
                    $("#btn_edit_init").click();

                    bind_init_data(data.data, index, "update", $("#txt_case_description").val());

                }
            });

            return false;
        },
        'click .update_init_copy': function (e, value, row, index) {
            var copy_data = {};
            for (var key in row) {
                if (typeof row[key] == "object") {
                    copy_data[key] = JSON.stringify(row[key]);
                } else {
                    copy_data[key] = row[key];
                }

            }
            var copy_data_str = JSON.stringify(copy_data);

            $.ajax({
                type: "POST",
                headers: {"X-CSRFToken": csrf_token},
                url: "/api/case/init/add",
                contentType: "application/json; charset=UTF-8",
                data: copy_data_str,
                success: function (data) {
                    if (data.code != 0) {
                        toastr.info("info", data.message);
                        return;
                    }

                    toastr.success("success", '复制成功');
                    $("#tb_edit_init").bootstrapTable('insertRow', {
                        index: 0,
                        row: data.origin_data
                    });

                }
            });
        }
    };

$("#btn_business_add").click(function () {
    var program_id = $("#txt_edit_case_from_system").val();
    var program_name = $("#txt_edit_case_from_system").find("option:selected").text();
    $("#program_id").text(program_id);
    $("#program_name").text(program_name);
    $("#addBusiness").modal("show");
});

function getNow(s) {
    return s < 10 ? '0' + s : s;
}

function change_to_empty(data) {
    if (typeof data == 'object') {
        for (var k in data) {
            return data;
        }
        return '';
    }
    return data;

};

function get_date() {
    var myDate = new Date();
    //获取当前年
    var year = myDate.getFullYear();
    //获取当前月
    var month = myDate.getMonth() + 1;
    //获取当前日
    var date = myDate.getDate();
    var h = myDate.getHours();       //获取当前小时数(0-23)
    var m = myDate.getMinutes();     //获取当前分钟数(0-59)
    var s = myDate.getSeconds();

    var now = year + '-' + getNow(month) + "-" + getNow(date) + " " + getNow(h) + ':' + getNow(m) + ":" + getNow(s);
    return now
}

function jsonFormatter(value, row, index) {
    return "<pre style='white-space: pre-wrap;border:0px;background-color: transparent;'>" + JSON.stringify(value, null, 2) + "</pre>"
};
var PreTableInit = function () {

    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_edit_pre').bootstrapTable({
            // url: '/api/tb_case/',         //请求后台的URL（*）
            data: prevInfo,
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            height: $(window).height() - 300,
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: false,
            showColumns: true,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: false,                //是否启用点击选中行
            //height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle: false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: false,
                visible: false
            }, {
                field: 'prev_id',
                visible: true,
                title: 'ID',
            }, {
                field: 'operate',
                align: 'center',
                width: "150px",
                events: operateEvents,
                formatter: operateFormatter,
                colspan: 1,
                title: '操作'
            }, {
                field: 'prev_name',
                title: '前置名称',
                align: 'center'
            }, {
                field: 'prev_description',
                title: '前置描述',
                align: 'center'
            }, {
                field: 'prev_flag',
                visible: false
            }, {
                field: 'prev_setup_type',
                visible: false
            }, {
                field: 'prev_api_address',
                title: '请求URL',
                align: 'center'
            }, {
                field: 'prev_api_method',
                title: '请求方式',
                align: 'center',
                visible: false
            }, {
                field: 'prev_api_params',
                title: '请求参数',
                formatter: jsonFormatter,
                visible: false
            }, {
                field: 'prev_api_header',
                title: '请求头信息',
                align: 'center',
                visible: false

            }, {
                field: 'prev_api_expression',
                title: '替换表达式',
                formatter: jsonFormatter,
                visible: false
            }, {
                field: 'prev_sql_statement',
                title: 'sql语句',
                align: 'center',
                visible: false
            }, {
                field: 'prev_sql_params',
                title: 'sql参数',
                formatter: jsonFormatter,
                visible: false
            }, {
                field: 'prev_sql_database',
                title: 'sql执行数据库',
                align: 'center',
                visible: false
            }, {
                field: 'prev_sql_expression',
                title: 'sql替换表达式',
                formatter: jsonFormatter,
                visible: false
            }, {
                field: 'prev_expression',
                title: '替换表达式',
                formatter: jsonFormatter,
                visible: false
            }, {
                field: 'prev_params',
                title: '用户变量定义参数',
                formatter: jsonFormatter,
                visible: false
            }, {
                field: 'prev_except_expression',
                title: '公共替换表达式',
                formatter: jsonFormatter,
                visible: false
            }, {
                field: 'prev_except_value',
                title: '预期值替换表达式',
                formatter: jsonFormatter,
                visible: false
            }, {
                field: 'prev_in_user',
                visible: false
            }, {
                field: 'prev_last_user',
                visible: false
            }, {
                field: 'prev_in_date',
                visible: false
            }, {
                field: 'prev_last_date',
                visible: false
            }, {
                field: 'prev_priority',
                title: '优先级',
                editable: {
                    type: 'text',
                    title: '优先级',
                    validate: function (v) {
                        if (!v) {
                            return '优先级不能为空';
                        }
                    }
                }
            }],

            onEditableSave: function (field, row, oldValue, $el) {
                var pre_data = JSON.stringify({
                    "prev_id": row['prev_id'],
                    "prev_priority": parseInt(row[field]),
                    "prev_last_user": current_user
                });
                $.ajax({
                    type: "PUT",
                    url: "/api/case/prev_priority",
                    headers: {
                        "X-CSRFToken": csrf_token,
                        "content-type": "application/json"
                    },
                    data: pre_data,
                    dataType: 'JSON',
                    success: function (data) {
                        if (data["code"] == 1) {
                            toastr.warning("warning", "更新数据失败，请求联系管理员");
                        } else {
                            toastr.success("success", "更新优先级成功");
                        }
                    },
                    error: function () {
                        toastr.error("error", "网络异常");
                    }

                });
            }
        });

        function operateFormatter(value, row, index) {
            return [
                '<a class="update_prev_copy" href="javascript:void(0)" title="Copy">',
                '<span>复制</span>',
                '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
                '<a class="update_prev_update" style="cursor: pointer" href="javascript:void(0)" title="Update">',
                '<span>编辑</span>',
                '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
                '<a class="update_prev_delete" href="javascript:void(0)" title="Delete">',
                '<span>删除</span>',
                '</a>',
            ].join('');
        }
    };

    return oTableInit;
}

var AddTableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_edit_init').bootstrapTable({
            //url: '/api/tb_case/',         //请求后台的URL（*）
            data: initInfo,
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            height: $(window).height() - 300,
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: false,
            showColumns: true,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            //height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle: false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: false,
                visible: false
            }, {
                field: 'case_init_id',
                title: 'ID'
            }, {
                field: 'operate',
                align: 'center',
                width: "150px",
                events: operateEvents,
                formatter: operateFormatter,
                title: '操作'
            }, {
                field: 'case_init_name',
                title: '初始化名称',
                align: 'center'
            }, {
                field: 'case_init_description',
                title: '初始化描述',
                align: 'center'
            }, {
                field: 'case_init_type',
                title: '初始化类型',
                align: 'center'
            }, {
                field: 'case_init_api_address',
                title: '请求URL',
                align: 'center',
                visible: false
            }, {
                field: 'case_init_api_method',
                title: '请求方式',
                align: 'center',
                visible: false
            }, {
                field: 'case_init_api_params',
                title: '请求参数',
                formatter: jsonFormatter,
                visible: false
            }, {
                field: 'case_init_api_header',
                title: '请求头信息',
                align: 'center',
                visible: false
            }, {
                field: 'case_init_api_expression',
                title: '替换表达式',
                formatter: jsonFormatter,
                visible: false
            }, {
                field: 'case_init_sql',
                title: 'sql语句',
                align: 'center',
                visible: false
            }, {
                field: 'case_init_sql_params',
                title: 'sql参数',
                formatter: jsonFormatter,
                visible: false
            }, {
                field: 'case_init_sql_expression',
                title: 'sql替换表达式',
                formatter: jsonFormatter,
                visible: false
            }, {
                field: 'case_init_sql_database',
                title: '执行数据库',
                align: 'center',
                visible: false
            }, {
                field: 'case_init_indate',
                visible: false
            }, {
                field: 'case_init_inuser',
                visible: false
            }, {
                field: 'case_init_lastuser',
                visible: false
            }, {
                field: 'case_init_lastdate',
                visible: false
            }, {
                field: 'case_priority',
                title: '优先级',
                editable: {
                    type: 'text',
                    title: '优先级',
                    validate: function (v) {
                        if (!v) {
                            return '优先级不能为空';
                        }
                    }
                }
            }],
            onEditableSave: function (field, row, oldValue, $el) {
                var init_data = JSON.stringify({
                    "init_id": row['case_init_id'],
                    "case_priority": parseInt(row[field]),
                    "case_init_lastuser": current_user
                });
                $.ajax({
                    type: "PUT",
                    url: "/api/case/init_priority",
                    headers: {
                        "X-CSRFToken": csrf_token,
                        "content-type": "application/json"
                    },
                    data: init_data,
                    dataType: 'JSON',
                    success: function (data) {
                        if (data["code"] == 1) {
                            toastr.warning("warning", "更新数据失败，请求联系管理员");
                        } else {
                            toastr.success("success", "更新优先级成功");
                        }
                    },
                    error: function () {
                        toastr.error("error", "网络异常");
                    }

                });
            }
        });

        function operateFormatter(value, row, index) {
            return [
                '<a class="update_init_copy" href="javascript:void(0)" title="Copy">',
                '<span>复制</span>',
                '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
                '<a class="update_init_update" style="cursor: pointer" href="javascript:void(0)" title="Update">',
                '<span>编辑</span>',
                '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
                '<a class="update_init_delete" href="javascript:void(0)" title="Delete">',
                '<span>删除</span>',
                '</a>',

            ].join('');
        }
    };

    return oTableInit;
}

function reponseFormatter(value, row, index) {
    return "<pre class='repsonse_pre'>" + value + "</pre>"
};

var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        //初始化页面上面的按钮事件
    };

    return oInit;
};

//获取httpmock信息
function get_http_mock() {
    var is_http_mock = $("#is_http_mock").prop('checked');

    if (is_http_mock) {
        var mock_info = {
            "mock_name": "",
            "mock_api_path": "",
            "mock_response": "",
            "mock_expression": "",
            "mock_status": "",
            "mock_memo": "",
            "mock_create_at": "",
            "mock_create_user": "",
            "mock_update_at": "",
            "mock_case_step_id": "",
            "mock_update_user": ""
        };
        var mock_response = $.isEmptyObject(json_dict['json_http_mock_expect'].get()) == true ? "" : json_dict['json_http_mock_expect'].get();
        var mock_expression = $.isEmptyObject(json_dict['json_http_mock_replace'].get()) == true ? "" : json_dict['json_http_mock_replace'].get();
        var mock_name = $("#txt_http_mock_name").val();
        var mock_path = $("#txt_http_mock_path").val();
        var mock_status = is_http_mock ? "active" : "deactive";
        mock_info["mock_name"] = mock_name;
        mock_info["mock_api_path"] = mock_path;
        mock_info["mock_response"] = mock_response;
        mock_info["mock_expression"] = mock_expression;
        mock_info["mock_status"] = mock_status;
        mock_info["mock_memo"] = "";
        mock_info["mock_case_step_id"] = 1;
        mock_info["mock_create_at"] = get_date();
        mock_info["mock_create_user"] = current_user;
        mock_info["mock_update_at"] = get_date();
        mock_info["mock_update_user"] = current_user;
        return mock_info;
    }

}

//获取数据库mock信息
function get_db_mock() {
    var is_mock = $("#is_mock").prop('checked');

    if (is_mock) {
        var mock_sql_info = {
            "mock_name": "",
            "mock_api_path": "",
            "mock_response": "",
            "mock_expression": "",
            "mock_status": "",
            "mock_memo": "",
            "mock_create_at": "",
            "mock_create_user": "",
            "mock_update_at": "",
            "mock_case_step_id": "",
            "mock_update_user": ""
        };
        var mock_sql_response = $.isEmptyObject(json_dict['json_sql_mock_expect'].get()) == true ? "" : json_dict['json_sql_mock_expect'].get();
        var mock_sql_expression = $.isEmptyObject(json_dict['json_sql_mock_replace'].get()) == true ? "" : json_dict['json_sql_mock_replace'].get();
        var mock_name = $("#txt_sql_mock_name").val();
        var mock_path = $("#txt_sql_mock_path").val();
        var mock_status = is_mock ? "active" : "deactive";
        mock_sql_info["mock_name"] = mock_name;
        mock_sql_info["mock_api_path"] = mock_path;
        mock_sql_info["mock_response"] = mock_sql_response;
        mock_sql_info["mock_expression"] = mock_sql_expression;
        mock_sql_info["mock_status"] = mock_status;
        mock_sql_info["mock_memo"] = "";
        mock_sql_info["mock_case_step_id"] = 1;
        mock_sql_info["mock_create_at"] = get_date();
        mock_sql_info["mock_create_user"] = current_user;
        mock_sql_info["mock_update_at"] = get_date();
        mock_sql_info["mock_update_user"] = current_user;
        return mock_sql_info;
    }

}

//mock所有情况
function get_mocks() {
    var mocks = new Array();
    var is_http_db = $('#accordion input:radio:checked').val();
    if ("2" == is_http_db) {
        var db_mock = get_db_mock();
        if ($.isEmptyObject(db_mock) == false) {
            mocks.push(db_mock);
        }

    } else if ("1" == is_http_db) {
        //获取实际值请求-数据库请求
        var http_mock = get_http_mock();
        if ($.isEmptyObject(http_mock) == false) {
            mocks.push(http_mock);
        }
    }
    return mocks;
}

$("#btn_copy").click(function () {
        var case_data = JSON.stringify({
            "case_id": $("#txt_case_id").val(),
            "case_exec_group": $("#txt_case_exec_group").val(),
            "case_from_system": $("#txt_edit_case_from_system").val(),
            "case_author": current_user,
            "case_run_group_property": $("#sel_run_group_property").val()
        });
        $.ajax({
            url: "/api/case/case/copy",
            contentType: "application/json; charset=UTF-8",
            headers: {"X-CSRFToken": csrf_token},
            async: true,
            jsonp: "callback",
            type: "POST",
            data: case_data,
            // 成功后开启模态框
            success: function (data) {
                if (data["code"] == 1) {
                    toastr.warning("warning", data["msg"]);
                } else {
                    console.log(data.origin_data);
                    var address = "/case/" + data.origin_data;
                    $(location).attr('href', address);
                    toastr.success("success", "复制用例成功");
                }
            },
            error: function () {
                $("#update_warning").text("网络异常，请求失败");
                $("#update_warning").show()
            },
            dataType: "json"
        });
    });

function show_mock(index) {
    var myid = '#is_mock';
    var mycollose = '#collapse_case_mock';
    if (index == 1) {
        myid = '#is_http_mock';
        mycollose = '#collapse_case_http_mock';
    }
    if ($(myid).prop('checked')) {
        $(mycollose).collapse('show');
    } else {
        $(mycollose).collapse('hide');
    }
};

//添加初始化
$("#btn_edit_add_init").click(function () {
    var case_id = $("#txt_case_id").val();
    var case_name = $("#txt_case_description").val();
    bind_init_edit_addinit(case_id, "add", case_name);

});

//添加前置处理
$("#btn_edit_add_prev").click(function () {
    var case_id = $("#txt_case_id").val();
    var case_name = $("#txt_case_description").val();
    bind_prev_edit_addprev(case_id, "add", case_name);

});

//更新用例
$("#btn_update").click(function () {// 用例基础信息获取
    var case_data = fill_data("update");


    $.ajax({
        url: "/api/case/case/",
        contentType: "application/json; charset=UTF-8",
        headers: {"X-CSRFToken": csrf_token},
        async: true,
        jsonp: "callback",
        type: "PUT",
        data: case_data,
        // 成功后开启模态框
        success: function (data) {
            if (data["code"] == 1) {
                toastr.warning("warning", data["msg"]);
            } else {
                toastr.success("success", "更新用例成功");
            }
        },
        error: function () {
            $("#update_warning").text("网络异常，请求失败");
            $("#update_warning").show()
        },
        dataType: "json"
    });
});

function fill_data(action) {
    var case_id = $("#txt_case_id").val();
    var case_name = $("#txt_case_name").val();
    var case_description = $("#txt_case_description").val();
    var case_type = $("#txt_case_type").val();
    var case_run_device = $("#sel_run_device").val();
    var case_run_group_property = $("#sel_run_group_property").val();
    var case_run_priority = $("#txt_run_priority").val();
    var case_run_task = $("#txt_edit_case_next_task").val();
    var case_run_msg = $("#txt_edit_case_next_msg").val();
    var case_wait_time = $("#txt_edit_case_wait_time").val();
    var case_from_system = $("#txt_edit_case_from_system").val();
    var case_belong_business = $("#sel_case_belong_business").val();
    var case_vars_name = $("#txt_edit_case_vars_name").val();
    var case_is_exec = $('#sel_case_exec').val();
    var case_exec_group = $("#txt_case_exec_group").val();
    var case_ref_tapd_id = $("#txt_edit_case_ref_tapd_id").val();


    //获取实际值请求-http
    var is_http_db = $('input[name="groupCaseRadios"]:checked').val();

    var request_url = "";
    var request_method = "";
    var request_header = "";
    var request_args = "";
    var request_replace = "";
    var case_sql = "";
    var case_sql_args = "";
    var case_sql_replace = "";
    var case_sql_deveice = "";
    var case_author = "";
    var case_last_user = "";

    if ("1" == is_http_db) {
        request_url = $("#txt_case_request_url").val();
        request_method = $("#sel_request_method").val();
        request_header = get_reverse_json_value(json_dict['sel_request_header'].get());
        var case_check_method = "except";
        try {
            request_args = json_dict['json_case_request_args'].get();
        } catch (e) {
            request_args = ""
        }
        request_args = get_reverse_json_value(request_args);
        try {
            request_replace = json_dict['json_case_replace'].get();
        } catch (e) {
            request_replace = ""
        }
        case_sql_replace = get_reverse_json_value(request_replace);

    } else if ("2" == is_http_db) {
        //获取实际值请求-数据库请求
        case_sql = $("#txt_case_sql").val();
        try {
            case_sql_args = get_reverse_json_value(json_dict['json_case_sql_args'].get());
        } catch (e) {
            case_sql_args = ""
        }
        try {
            case_sql_replace = get_reverse_json_value(json_dict['json_case_sql_replace'].get());
        } catch (e) {
            case_sql_replace = ""
        }

        case_sql_deveice = $("#sel_run_sql_device").val();
        case_check_method = "database";

    }
    var case_mock_flag = "N";
    var case_mock_flag_http = $("input:checkbox[id='is_http_mock_edit']:checked").val();
    var case_mock_flag_db = $("input:checkbox[id='is_mock_edit']:checked").val();
    if (case_mock_flag_db == true || case_mock_flag_http == true) {
        case_mock_flag = 'Y'
    } else {
        case_mock_flag = 'N'
    }

    //预期相关
    var case_expect = "";
    try {
        case_expect = json_dict['json_case_expect'].get();
    } catch (e) {
        case_expect = ""
    }

    case_expect = get_reverse_json_value(case_expect);

    //添加前置处理
    var pre_table_data = $('#tb_edit_pre').bootstrapTable('getData');
    pre_table_data = change_to_empty(pre_table_data);

    //添加初始化
    var init_table_data = $('#tb_edit_init').bootstrapTable('getData');
    init_table_data = change_to_empty(init_table_data);
    if (action != "update") {
        case_author = current_user;
        case_last_user = current_user;
    }

    if (case_name == "" ||
        case_description == "" ||
        case_from_system == ""
    ) {
        toastr.warning("warning", '用例名称、用例描述、用户来源、参数不能为空');
        return
    } else if (case_run_device == "group") {
        if ($.isEmptyObject(case_exec_group) || $.isEmptyObject(case_run_group_property)) {
            toastr.warning("warning", '执行器为group 时，复杂用例属性和复杂用例分组都不能为空');
            return
        }
    } else if (case_run_device == "common") {
        case_exec_group = "";
        case_run_group_property = "";

    } else if ($.isEmptyObject(case_run_priority) || typeof case_run_priority !== "number") {
        case_run_priority = 0
    } else if ($.isEmptyObject(case_wait_time) || typeof case_wait_time !== "number") {
        case_wait_time = 0
    }

    var case_data = JSON.stringify({
        "case": {
            "basicInfo": {
                "case_id": case_id,
                "case_exec_priority": case_run_priority,
                "case_from_system": case_from_system,
                "case_belong_business": case_belong_business,
                "case_name": case_name,
                "case_description": case_description,
                "case_category": case_type,
                "case_executor": case_run_device,
                "case_exec_group": case_exec_group,
                "case_exec_group_priority": case_run_group_property,
                "case_api_address": request_url,
                "case_api_method": request_method,
                "case_api_params": request_args,
                "case_api_header": request_header,
                "case_check_method": case_check_method,
                "case_except_value": case_expect,
                "case_sql_actual_statement": case_sql,
                "case_sql_actual_database": case_sql_deveice,
                "case_sql_params": case_sql_args,
                "case_ref_tapd_id": case_ref_tapd_id,
                "case_is_exec": case_is_exec,
                "case_mock_flag": case_mock_flag,
                "case_next_msg": case_run_msg,
                "case_next_task": case_run_task,
                "case_replace_expression": case_sql_replace,
                "case_wait_time": case_wait_time,
                "case_vars_name": case_vars_name,
                "case_author": case_author,
                "case_last_user": case_last_user,
                "case_in_date": get_date(),
                "case_last_user": current_user,
                "case_last_date": get_date(),
            },
            "prevInfo": pre_table_data,
            "initInfo": init_table_data,
            "mockInfo": get_mocks(),
        }
    });
    return case_data
}

$("#btn_case_exec").click(function () {
        var case_ids = new Array(),
            task_id = $("#txt_case_id").val(),
            task_system = $("#txt_edit_case_from_system").val();
        case_ids.push(task_id);

        var run_case = JSON.stringify({
            "task_ids": case_ids,
            "task_title": $("#txt_case_name").val() + "_debug_" + (Date.parse(new Date()) / 1000).toString(),
            "debug": true,
            "task_business": $("#sel_case_belong_business").val(),
            "task_system": task_system,
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
                } else {
                    toastr.success("success", "创建并运行成功");
                    save_cache("auto_exec", data.task_id);
                    save_cache("auto_exec_program", task_system);
                    $(location).attr('href', "/tasks/list?" + data.task_id);
                }
                $("#btn_create_task").removeAttr("disabled");
            },
            error: function (e) {
                toastr.warning("warning", e.msg);
                $("#btn_create_task").removeAttr("disabled");
            }
        });
    });

function save_cache(key, value) {
    localStorage.setItem(key, value);
}

function get_cache(key) {
    return localStorage.getItem(key);
}

function change_value_mark(value) {
        if (value == "") {
            return {};
        }
        //alert(value)
        var result = JSON.parse(value.replace(reg_marks, '"').replace(reg_enter, '\n').replace(reg_rmarks, "'").replace(reg_none, "null").replace(reg_boolean_true, true).replace(reg_boolean_false, false));
        return result
    };

$("#txt_edit_case_from_system").on("changed.bs.select", function (e) {
    refresh_business();
});

function refresh_business() {
    $.ajax({
        url: "/api/case/program_business/" + $("#txt_edit_case_from_system").val(),
        type: "GET",
        success: function (data) {
            if (data.code == 0) {
                $("#sel_case_belong_business").empty();
                var options = "";
                for (var index in data.data) {
                    options += "<option value='" + data.data[index]["business_name"] + "'>" +
                        data.data[index]["business_cname"] + "</option>";
                }
                $("#sel_case_belong_business").append(options);
                $("#sel_case_belong_business").selectpicker("refresh");
                setTimeout(function () {
                    var case_belong_business = $("#sel_case_belong_business").val();
                    $("#sel_case_belong_business").selectpicker('val', case_belong_business);
                    $('#sel_case_belong_business').selectpicker("refresh");
                }, 100);
            } else {
                $("#sel_case_belong_business").empty();
                $("#sel_case_belong_business").append("<option></option>");
                $("#sel_case_belong_business").selectpicker("refresh");
                toastr.warning("获取业务失败", 'warning');
            }
        },
        error: function () {
            toastr.error("获取业务异常", 'error');
            $("#sel_case_belong_business").empty();
            $("#sel_case_belong_business").append("<option></option>");
            $("#sel_case_belong_business").selectpicker("refresh");
        }
    })
}

$("#sel_run_device").on("changed.bs.select", function (e) {
    if ($(this).val() == "common") {
        $("#sel_run_group_property").empty();
        $("#div_group_property").addClass("hidden");
        $("#div_exec_group").addClass("hidden");
        var options = "<option value=''></option>";
        $("#sel_run_group_property").append(options);
        $("#sel_run_group_property").selectpicker("refresh");
    } else if ($(this).val() == "group") {

        $("#div_group_property").removeClass("hidden");
        $("#div_exec_group").removeClass("hidden");
        $("#sel_run_group_property").empty();
        var options = "<option value='main'>父用例</option>";
        options += "<option value='sub'>子用例</option>";
        $("#sel_run_group_property").append(options);
        $("#sel_run_group_property").selectpicker("refresh");
    }
});

function load_case(case_id, bind_data_control, init_select) {
    var result = "";
    $.ajax({
        type: "GET",
        headers: {"X-CSRFToken": csrf_token},
        url: "/api/case/load/case/" + case_id,
        contentType: "application/json; charset=UTF-8",
        success: function (data) {
            if (data.code != 0) {
                toastr.error("error", "程序发生异常，请求联系管理员");
                return;
            }
            var case_belong_business = data.result["basicInfo"]["case_belong_business"];
            bind_data_control(data.result);
            init_select(data.result);
        }
    });
}

function bind_data_control(case_entity) {

    $('#txt_case_name').val(case_entity['basicInfo']['case_name']);
    $('#txt_case_id').val(case_entity['basicInfo']['case_id']);
    $('#txt_case_description').val(case_entity['basicInfo']['case_description']);
    $('#txt_case_type').val(case_entity['basicInfo']['case_category']);
    $('#sel_run_device').selectpicker('val', (case_entity['basicInfo']['case_executor']));
    $('#sel_run_group_property').selectpicker('val', (case_entity['basicInfo']['case_exec_group_priority']));
    $('#txt_case_exec_group').val(case_entity['basicInfo']['case_exec_group']);
    $('#txt_run_priority').val(case_entity['basicInfo']['case_exec_priority']);
    $('#txt_edit_case_vars_name').val(case_entity['basicInfo']['case_vars_name']);
    $('#txt_edit_case_wait_time').val(case_entity['basicInfo']['case_wait_time']);
    $('#txt_edit_case_from_system').val(case_entity['basicInfo']['case_from_system']);
    $('#txt_edit_case_ref_tapd_id').val(case_entity['basicInfo']['case_ref_tapd_id']);
    $('#txt_edit_case_next_task').val(case_entity['basicInfo']['case_next_task']);
    $('#txt_edit_case_next_msg').val(case_entity['basicInfo']['case_next_msg']);
    $('#txt_case_request_url').val(case_entity['basicInfo']['case_api_address']);
    $('#sel_request_method').selectpicker('val', (case_entity['basicInfo']['case_api_method']).toUpperCase());
    $('#txt_http_mock_path').val(case_entity['basicInfo']['mock_api_path']);
    $('#txt_case_sql').val(case_entity['basicInfo']['txt_case_sql']);
    $('#sel_run_sql_device').val(case_entity['basicInfo']['case_sql_actual_database']);
    $('#txt_sql_mock_name').val(case_entity['basicInfo']['mock_name']);
    $('#txt_sql_mock_path').val(case_entity['basicInfo']['mock_api_path']);
    $('#txt_http_mock_path').val(case_entity['basicInfo']['mock_api_path']);

}

function init_select(case_entity) {
    json_dict['sel_request_header'].set(case_entity['basicInfo']['case_api_header']);

    var radio_case_is_exec = case_entity['basicInfo']['case_is_exec'];

    $('#sel_case_exec').val(radio_case_is_exec.toString());
    $('#sel_case_exec').selectpicker("refresh");

    $("#txt_edit_case_from_system").selectpicker("val", case_entity['basicInfo']['case_from_system']);
    $('#txt_edit_case_from_system').selectpicker("refresh");
    refresh_business();
    if ((case_entity['basicInfo']['case_check_method']).toLowerCase() == "except") {

        json_dict['json_case_request_args'].set(case_entity['basicInfo']['case_api_params']);
        json_dict['json_case_replace'].set(case_entity['basicInfo']['case_replace_expression']);
    } else {

        $('#is_case_db_reqeust').click();
        json_dict['json_case_sql_args'].set(case_entity['basicInfo']['case_sql_params']);
        json_dict['json_case_sql_replace'].set(case_entity['basicInfo']['case_replace_expression']);
        $("#txt_case_sql").val(case_entity['basicInfo']['case_sql_actual_statement']);
    }

    json_dict['json_case_expect'].set(case_entity['basicInfo']['case_except_value']);

    var mockInfo_binding = case_entity['mockInfo'][0];
    if ($.isEmptyObject(mockInfo_binding) == false) {
        $('#is_edit_http_mock').click();
        $('#is_edit_mock').click();
        $('#txt_http_mock_name').val(mockInfo_binding.mock_name);
        $('#txt_http_mock_path').val(mockInfo_binding.mock_api_path);
        $('#txt_sql_mock_name').val(mockInfo_binding.mock_name);
        $('#txt_sql_mock_path').val(mockInfo_binding.mock_api_path);
        json_dict['json_http_mock_replace'].set(mockInfo_binding.mock_expression);
        json_dict['json_http_mock_expect'].set(mockInfo_binding.mock_response);
        json_dict['json_sql_mock_expect'].set(mockInfo_binding.mock_response);
        json_dict['json_sql_mock_replace'].set(mockInfo_binding.mock_expression);

    }

}

// create the editor

function getMaxId(table_id, id_name) {
    var init_datas = $(table_id).bootstrapTable('getData');
    var ids = new Array();

    if (init_datas.length > 0) {
        init_datas.forEach(function (item) {
            ids.push(item[id_name]);
        });
    }
    /*for(var index in init_datas){
        console.log(index);
        ids.push(init_datas[index]["init_id"]);
    }*/
    var max = 1;
    if (ids.length > 0) {
        max = Math.max.apply(null, ids) + 1;
    }
    return max;
}

$('#myTab a').click(function (e) {
    if (!$(this).parent('li').hasClass('active')) {
        var that = this;
        showConfirm('切换后该页面的内容会重置，是否继续切换？', function () {
            e.preventDefault();
            $(that).tab('show');
            if ("tab0" == $('#that').attr("href")) {
                $('#is_http').html("1");
            } else if ("tab1" == $('#that').attr("href")) {
                $('#is_http').html("2");
            }
            // 不清除
        })

    }
});

$("#accordion input").click(function () {

   if(  $("#collapseOne").hasClass('in') ){
       $(".collapseRow").eq(0).click();
   }
   if(  $("#collapseTwo").hasClass('in') ){
       $(".collapseRow").eq(1).click();
   }
   $(this).next().click();

}).eq(0).click();

$("#myInit input").click(function () {

   if(  $("#collapseInitOne").hasClass('in') ){
       $(".collapseInitRow").eq(0).click();
   }
   if(  $("#collapseInitTwo").hasClass('in') ){
       $(".collapseInitRow").eq(1).click();
   }
   $(this).next().click();

}).eq(0).click();

$("#myPre input").click(function () {

   if(  $("#collapsePreOne").hasClass('in') ){
       $(".collapsePreRow").eq(0).click();
   }
   if(  $("#collapsePreTwo").hasClass('in') ){
       $(".collapsePreRow").eq(1).click();
   }
   if(  $("#collapsePreThree").hasClass('in') ){
       $(".collapsePreRow").eq(2).click();
   }
   $(this).next().click();

}).eq(0).click();

$("#myInitContent input").click(function () {

   if(  $("#collapseInitContentOne").hasClass('in') ){
       $(".collapseInitContentRow").eq(0).click();
   }
   if(  $("#collapseInitContentTwo").hasClass('in') ){
       $(".collapseInitContentRow").eq(1).click();
   }
   $(this).next().click();

}).eq(0).click();

$("#myPreContent input").click(function () {

   if(  $("#collapsePreContentOne").hasClass('in') ){
       $(".collapsePreContentRow").eq(0).click();
   }

   if(  $("#collapsePreContentTwo").hasClass('in') ){
       $(".collapsePreContentRow").eq(1).click();
   }

   if(  $("#collapsePreContentThree").hasClass('in') ){
       $(".collapsePreContentRow").eq(2).click();
   }

   $(this).next().click();

}).eq(0).click();