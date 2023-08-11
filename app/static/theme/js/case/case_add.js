$(function () {

    //1.初始化Add Init Table
    var oInitTable = new AddTableInit();
    oInitTable.Init();

    //2.初始化Add Pre Table
    var oPreTable = new PreTableInit();
    oPreTable.Init();

    //2.初始化Button的点击事件
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();

    init_page_default_value();

    $(".content-show").css("height", $(window).height() - 180);

    $(window).resize(function (){
            var page_height = $(window).height();
            $( '#tb_add_init' ).bootstrapTable('resetView',{ height: $(window).height() - 220 } );
            $( '#tb_add_pre' ).bootstrapTable('resetView',{ height: $(window).height() - 220 } );
            $(".content-show").css("height", $(window).height() - 180)
    });

    //所属系统和所属业务的联动
    $("#sel_case_from_system").on("changed.bs.select", function (e) {

        save_add_case_program($(this).val());

        refresh_business();
    });

    function refresh_business(){
        $.ajax({
            url: "/api/case/program_business/" + $("#sel_case_from_system").val(),
            type: "GET",
            success:function (data) {
                if(data.code == 0){
                    $("#sel_case_belong_business").empty();
                    var options = "";
                    for(var index in data.data){
                        options += "<option value='" + data.data[index]["business_name"] + "'>" +
                            data.data[index]["business_cname"] + "</option>";
                        }
                    $("#sel_case_belong_business").append(options);
                    $("#sel_case_belong_business").selectpicker("refresh");
                }
                else{
                    $("#sel_case_belong_business").empty();
                    $("#sel_case_belong_business").append("<option></option>");
                    $("#sel_case_belong_business").selectpicker("refresh");
                    toastr.warning("获取业务失败", 'warning');
                }
            },
            error:function () {
              toastr.error("获取业务异常", 'error');
              $("#sel_case_belong_business").empty();
              $("#sel_case_belong_business").append("<option></option>");
              $("#sel_case_belong_business").selectpicker("refresh");
            }
        })
    }

    $("#btn_business_save").click(function () {
            $.ajax({
                url: "/api/case/add_business",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify({
                    "project_id": $("#program_id").text(),
                    "business_name": $("#txt_business_name").val(),
                    "business_cname": $("#txt_business_cname").val(),
                    "autor": current_user
                }),
                dataType:"json",
                type:"POST",
                headers: {"X-CSRFToken": csrf_token},

                success:function (data) {
                    if(data.code == 0){
                        $("#btn_business_cancel").click();
                        toastr.success("success", "添加业务成功");
                        setTimeout(function () {
                            refresh_business();
                        }, 100);

                    }
                    else {
                        toastr.warning("warning", "添加业务失败");
                    }
                },
                error:function () {
                    toastr.error("error", "添加业务异常");
                }
            });


        });
    change_select_system();

    function change_select_system(){

        var select_program = localStorage.getItem("add_case_program");

        if(select_program){
            $("#sel_case_from_system").val(select_program).trigger("changed");
            $("#sel_case_from_system").selectpicker("refresh");
        }

    };

    function save_add_case_program(program_id) {
        localStorage.setItem("add_case_program", program_id);
    }

    // 用例类型和复杂用例属性联动
    $("#sel_run_device").on("changed.bs.select", function (e) {
        if($(this).val() == "common"){
            $("#sel_run_group_property").empty();
            $("#div_group_property").addClass("hidden");
            $("#div_exec_group").addClass("hidden");
            var options = "<option value=''></option>";
            $("#sel_run_group_property").append(options);
            $("#sel_run_group_property").selectpicker("refresh");
        }
        else if($(this).val() == "group") {

            $("#div_group_property").removeClass("hidden");
            $("#div_exec_group").removeClass("hidden");
            $("#sel_run_group_property").empty();
            var options = "<option value='main'>父用例</option>";
            options += "<option value='sub'>子用例</option>";
            $("#sel_run_group_property").append(options);
            $("#sel_run_group_property").selectpicker("refresh");
        }
    });

});
function init_page_default_value(){
    json_dict['sel_request_header'].set({
        "Content-type": "application/json"
    })
}
// create the editor

$("#btn_business_add").click(function () {
    var program_id = $("#sel_case_from_system").val();
    var program_name = $("#sel_case_from_system").find("option:selected").text();
    $("#program_id").text(program_id);
    $("#program_name").text(program_name);
    $("#addBusiness").modal("show");
});

var options = {
    mode: "code"
};

var json = {
};

var json_dict = {};

var json_list = ['json_case_expect', 'json_case_replace', 'json_case_request_args',
    'json_init_request_args', 'json_init_replace', 'json_pre_request_args',
    'json_pre_http_replace', 'json_pre_replace', 'json_pre_sql_args', 'json_pre_expect', 'json_init_sql_args',
    'json_sql_mock_expect', 'json_sql_mock_replace', 'json_http_mock_expect', 'json_http_mock_replace',
    'json_init_sql_replace', 'json_pre_sql_replace', 'json_public_replace', 'json_user_args',
    'json_case_sql_args', 'json_case_sql_replace','sel_request_header'];

for(var json_name in json_list){
    var container = document.getElementById(json_list[json_name]);
    var json_edit = new JSONEditor(container, options, json);
    json_dict[json_list[json_name]] = json_edit;
}

function getMaxId(table_id, id_name){
    var init_datas = $(table_id).bootstrapTable('getData');
    var ids = new Array();

    if(init_datas.length > 0) {
        init_datas.forEach(function (item) {
            ids.push(item[id_name]);
        });
    }
    /*for(var index in init_datas){
        console.log(index);
        ids.push(init_datas[index]["init_id"]);
    }*/
    var max = 1;
    if(ids.length > 0)
    {
        max = Math.max.apply(null, ids) + 1;
    }
    return max;
}

$('#myTab a').click(function (e) {
    if( !$(this).parent('li').hasClass('active') ){
        var that = this;
        showConfirm('切换后该页面的内容会重置，是否继续切换？', function (){
            e.preventDefault();
            $(that).tab('show');
            if("tab0" == $('#that').attr("href"))
            {
                $('#is_http').html("1");
            }
            else if ("tab1" == $('#that').attr("href"))
            {
                $('#is_http').html("2");
            }
            // 不清除
        })

    }
});

// set json
// editor.set(json)
// get json editor.get();

window.operateEvents = {
    'click .delete': function (e, value, row, index) {
        toastr.success("success", '删除成功');
        $("#tb_add_pre").bootstrapTable('remove', {
            field: 'prev_id',
            values: [row['prev_id']]
        });

        return false;
    },
    'click .update': function (e, value, row, index) {
        $.ajax({
            type : "PUT",
            headers:{"X-CSRFToken":csrf_token},
            url : "/api/mock/pre",
            data : JSON.stringify({
                "prev_id" : row['prev_id']
            }),
            contentType: "application/json; charset=UTF-8",
            success : function (data) {
                if (data.result != 0) {
                    toastr.info("info", data.message);
                    return ;
                }
                toastr.success("success", '更新成功');
                $("#tb_add_pre").bootstrapTable('refresh');
            }
        });

        return false;
    },
    'click .copy': function (e, value, row, index) {
        var copy_data = {};
        for(var key in row){
            copy_data[key]=row[key]
        }

        $("#tb_add_pre").bootstrapTable('insertRow', {
            index: 0,
            row: copy_data
        });
        toastr.success("success", '复制成功');

    },
    'click .init_delete': function (e, value, row, index) {
        toastr.success("success", '删除成功');
        $("#tb_add_init").bootstrapTable('remove', {
            field: 'init_id',
            values: [row['init_id']]
        });
        return false;
    },
    'click .init_update': function (e, value, row, index) {
        $.ajax({
            type : "PUT",
            headers: {"X-CSRFToken":csrf_token},
            url : "/api/mock/init",
            data : JSON.stringify({
                "init_id" : row['init_id']
            }),
            contentType: "application/json; charset=UTF-8",
            success : function (data) {
                if (data.result != 0) {
                    toastr.info("info", data.message);
                    return ;
                }
                toastr.success("success", '更新成功');
                $("#tb_add_init").bootstrapTable('refresh');
            }
        });

        return false;
    },
    'click .init_copy': function (e, value, row, index) {
        var copy_data = {};
        for(var key in row){
            copy_data[key]=row[key]
        }

        toastr.success("success", '复制成功');
        $("#tb_add_init").bootstrapTable('insertRow', {
            index: 0,
            row: copy_data
        });

        return false;
    }
};



function getNow(s) {
    return s < 10 ? '0' + s: s;
}

function get_date() {
    var myDate = new Date();
    //获取当前年
    var year=myDate.getFullYear();
    //获取当前月
    var month=myDate.getMonth()+1;
    //获取当前日
    var date=myDate.getDate();
    var h=myDate.getHours();       //获取当前小时数(0-23)
    var m=myDate.getMinutes();     //获取当前分钟数(0-59)
    var s=myDate.getSeconds();

    var now=year+'-'+getNow(month)+"-"+getNow(date)+" "+getNow(h)+':'+getNow(m)+":"+getNow(s);
    return now
}

function jsonFormatter(value, row, index) {
    return "<pre style='white-space: pre-wrap;border:0px;background-color: transparent;'>"+JSON.stringify(value, null, 2)+"</pre>"
};

var PreTableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_add_pre').bootstrapTable({
            // url: '/api/tb_case/',         //请求后台的URL（*）
            data : [],
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            height: $(window).height() - 280,
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
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
            showToggle:false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: false,
                visible:false
            }, {
                field: 'prev_id',
                visible: true,
                title: 'ID',
            },{
                field: 'operate',
                align:'center',
                width: "150px",
                events: operateEvents,
                formatter: operateFormatter,
                colspan: 1,
                title: '操作'}
                , {
                    field: 'prev_name',
                    title: '前置名称',
                    align: 'center'
                },  {
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
                    formatter:jsonFormatter
                }, {
                    field: 'prev_api_header',
                    title: '请求头信息',
                    align: 'center',
                    visible: false

                }, {
                    field: 'prev_api_expression',
                    title: '替换表达式',
                    formatter:jsonFormatter,
                    visible: false
                }, {
                    field: 'prev_sql_statement',
                    title: 'sql语句',
                    align: 'center',
                    visible: false
                }, {
                    field: 'prev_sql_params',
                    title: 'sql参数',
                    formatter:jsonFormatter,
                    visible: false
                }, {
                    field: 'prev_sql_database',
                    title: 'sql执行数据库',
                    align: 'center',
                    visible: false
                }, {
                    field: 'prev_sql_expression',
                    title: 'sql替换表达式',
                    formatter:jsonFormatter,
                    visible: false
                }, {
                    field: 'prev_expression',
                    title: '替换表达式',
                    formatter:jsonFormatter,
                    visible: false
                }, {
                    field: 'prev_params',
                    title: '用户变量定义参数',
                    formatter:jsonFormatter,
                    visible: false
                }, {
                    field: 'prev_except_expression',
                    title: '公共替换表达式',
                    formatter:jsonFormatter,
                    visible: false
                }, {
                    field: 'prev_except_value',
                    title: '预期值替换表达式',
                    //formatter:jsonFormatter,
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
                }]
        });



        function operateFormatter(value, row, index) {
            return [
                '<a class="copy" href="javascript:void(0)" title="Copy">',
                '<span>复制</span>',
                '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
                '<a class="update" style="cursor: pointer" href="case_pre_edit/'+row.prev_id+'/" title="Update">',
                '<span>编辑</span>',
                '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
                '<a class="delete" href="javascript:void(0)" title="Delete">',
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
        $('#tb_add_init').bootstrapTable({
            //url: '/api/tb_case/',         //请求后台的URL（*）
            data: [],
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            height: $(window).height() - 280,
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
                field: 'init_id',
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
                formatter:jsonFormatter,
            }, {
                field: 'case_init_api_header',
                title: '请求头信息',
                align: 'center',
                visible: false
            }, {
                field: 'case_init_api_expression',
                title: '替换表达式',
                formatter:jsonFormatter,
                visible: false
            }, {
                field: 'case_init_sql',
                title: 'sql表达式',
                align: 'center',
                visible: false
            }, {
                field: 'case_init_sql_params',
                title: 'sql参数',
                formatter:jsonFormatter,
                visible: false
            }, {
                field: 'case_init_sql_expression',
                title: 'sql替换表达式',
                formatter:jsonFormatter,
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
            }]
        });

        function operateFormatter(value, row, index) {
            return [
                '<a class="init_copy" href="javascript:void(0)" title="Copy">',
                '<span>复制</span>',
                '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
                '<a class="init_update" style="cursor: pointer" href="case_init_edit/' + row.init_id + '/" title="Update">',
                '<span>编辑</span>',
                '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
                '<a class="init_delete" href="javascript:void(0)" title="Delete">',
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

    if(is_http_mock) {
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
            "mock_update_user": ""};
        var mock_response = $.isEmptyObject(json_dict['json_http_mock_expect'].get()) ==true ? "": json_dict['json_http_mock_expect'].get();
        var mock_expression = $.isEmptyObject(json_dict['json_http_mock_replace'].get())==true ? "": json_dict['json_http_mock_replace'].get();
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

    if(is_mock){
        var mock_sql_info = {
            "mock_name": "",
            "mock_api_path":"",
            "mock_response": "",
            "mock_expression": "",
            "mock_status": "",
            "mock_memo": "",
            "mock_create_at":"",
            "mock_create_user": "",
            "mock_update_at":"",
            "mock_case_step_id": "",
            "mock_update_user":""};
        var mock_sql_response = $.isEmptyObject(json_dict['json_sql_mock_expect'].get()) == true ? "" : json_dict['json_sql_mock_expect'].get();
        var mock_sql_expression = $.isEmptyObject(json_dict['json_sql_mock_replace'].get()) == true ? "" :json_dict['json_sql_mock_replace'].get();
        var mock_name = $("#txt_sql_mock_name").val();
        var mock_path = $("#txt_sql_mock_path").val();
        var mock_status = is_mock ? "active" : "deactive";
        mock_sql_info["mock_name"] = mock_name;
        mock_sql_info["mock_api_path"] = mock_path;
        mock_sql_info["mock_response"] = mock_sql_response;
        mock_sql_info["mock_expression"] = mock_sql_expression;
        mock_sql_info["mock_status"] =mock_status ;
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
    if ("2" == is_http_db)
    {
        var db_mock = get_db_mock();
        if($.isEmptyObject(db_mock)==false){
            mocks.push(db_mock);
        }

    }
    else if ( "1" == is_http_db)
    {
        //获取实际值请求-数据库请求
        var http_mock = get_http_mock();
        if($.isEmptyObject(http_mock)==false){
            mocks.push(http_mock);
        }
    }
    return mocks;
}


//保存用例
function saveCase() {
    // 用例基础信息获取
    var case_data = fill_entity();
    $.ajax({
        url: "/api/case/case/",
        contentType: "application/json; charset=UTF-8",
        headers: {"X-CSRFToken": csrf_token},
        async: true,
        jsonp: "callback",
        type: "POST",
        data: case_data,
        // 成功后开启模态框
        success: function (data) {
            console.log(data);
            if (data["code"] == 1) {
                toastr.warning("warning", data["msg"]);
            }
            else {
                var address = "/case/" + data.origin_data;
                $(location).attr('href', address);
                toastr.success("success", "添加用例成功");
            }
        },
        error: function () {
            toastr.error("error", "网络异常，请求失败");
        },
        dataType: "json"
    });

};

function fill_entity(){

    var case_mock_flag ='N';
    var case_name = $("#txt_case_name").val();
    var case_description = $("#txt_case_description").val();
    var case_type = $("#txt_case_type").val();
    var case_run_device = $("#sel_run_device").val();
    var case_run_group_property = $("#sel_run_group_property").val();
    var case_run_priority = $("#txt_run_priority").val();
    var case_is_exec = 1;
    var case_vars_name = $("#txt_case_vars_name").val()
    var case_run_task = $("#txt_case_next_task").val();
    var case_run_msg = $("#txt_case_next_msg").val();
    var case_ref_tapd_id = $("#case_ref_tapd_id").val();
    var case_wait_time = $("#txt_case_wait_time").val();
    var case_mock_flag_http = $("input:checkbox[id='is_http_mock']:checked").val();
    var case_mock_flag_db = $("input:checkbox[id='is_mock']:checked").val();
    if (case_mock_flag_db==true || case_mock_flag_http==true){
        case_mock_flag = 'Y'
    }else{
        case_mock_flag = 'N'
    }

    var case_from_system  =$("#sel_case_from_system").val();
    var case_belong_business = $("#sel_case_belong_business").val();
    var case_exec_group =$("#txt_case_exec_group").val();

    //获取实际值请求-http
    var is_http_db = $('#accordion input:radio:checked').val();

    var request_url = "";
    var request_method = "";
    var request_header = "";
    var request_args = "";
    var request_replace = "";
    var case_sql = "";
    var case_sql_args = "";
    var case_sql_replace = "";
    var case_sql_deveice = "";

    if ("1" == is_http_db)
    {
        var request_url = $("#txt_case_request_url").val();
        var request_method = $("#sel_request_method").val();
        var request_header = $.isEmptyObject(json_dict['sel_request_header'].get())==true ? "" : json_dict['sel_request_header'].get();

        var request_args = $.isEmptyObject(json_dict['json_case_request_args'].get())==true ? "" : json_dict['json_case_request_args'].get();
        var request_replace = $.isEmptyObject(json_dict['json_case_replace'].get()) == true ? "" : json_dict['json_case_replace'].get();
        var case_check_method = 'except'

        if(request_method!=="GET" && $.isEmptyObject(request_replace)==false){
            toastr.error("error", 'http 请求中的替换表达式仅仅只能在请求方式为GET时使用');
            return
        }

    }
    else if ( "2" == is_http_db)
    {
        //获取实际值请求-数据库请求
        var case_sql = $("#txt_case_sql").val();
        var case_sql_args =  $.isEmptyObject(json_dict['json_case_sql_args'].get())==true ?"" : json_dict['json_case_sql_args'].get();
        var request_replace = $.isEmptyObject(json_dict['json_case_sql_replace'].get()) ==true ? "":json_dict['json_case_sql_replace'].get();
        var case_sql_deveice = $("#sel_run_sql_device").val();
        var case_check_method = 'database'
    }

    //预期相关
    var case_expect = $.isEmptyObject(json_dict['json_case_expect'].get()) == true ? "": json_dict['json_case_expect'].get();

    //添加前置处理
    var pre_table_data = $('#tb_add_pre').bootstrapTable('getData');

    //添加初始化
    var init_table_data = $('#tb_add_init').bootstrapTable('getData');

    if (case_name == "" ||
        case_description == ""||
        case_from_system==""
    ) {
        toastr.warning("warning", '用例名称、用例描述、用户来源、参数不能为空');
        return
    }else if(case_run_device=="group"){
        if( case_exec_group=="" || case_run_group_property==""){
            toastr.warning("warning", '执行器为group 时，复杂用例属性和复杂用例分组都不能为空');
            return
        }
    }else if (case_run_device=="common"){

        if( case_exec_group!=="" || case_run_group_property!==""){
            toastr.warning("warning", '执行器为common 时，复杂用例属性和复杂用例分组不能有值');
            return
        }
    }else if (case_run_priority=="" ||typeof case_run_priority !=="number"){
        case_run_priority =0
    }else if (case_wait_time=="" || typeof case_wait_time !=="number"){
        case_wait_time = 0
    }


    var case_data = JSON.stringify({
        "case":{
            "basicInfo":{
                "case_exec_priority":case_run_priority,
                "case_from_system":case_from_system,
                "case_belong_business":case_belong_business,
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
                "case_check_method":case_check_method,
                "case_except_value": case_expect,
                "case_sql_actual_statement": case_sql,
                "case_sql_actual_database": case_sql_deveice,
                "case_sql_params": case_sql_args,
                "case_ref_tapd_id": case_ref_tapd_id,
                "case_is_exec":case_is_exec,
                "case_mock_flag":case_mock_flag,
                "case_next_msg":case_run_msg,
                "case_next_task":case_run_task,
                "case_replace_expression":request_replace,
                "case_init_id":"",
                "case_wait_time":case_wait_time,
                "case_vars_name":case_vars_name,
                "case_author":current_user,
                "case_in_date":get_date(),
                "case_in_user":current_user,
                "case_last_user":current_user,
                "case_last_date":get_date(),
            },
            "prevInfo": pre_table_data,
            "initInfo": init_table_data,
            "mockInfo": get_mocks(),
        }
    });
    return case_data
}

function show_mock(index){
    var myid = '#is_mock';
    var mycollose = '#collapse_case_mock';
    if(index == 1){
        myid = '#is_http_mock';
        mycollose = '#collapse_case_http_mock';
    }
    if ($(myid).prop('checked')) {
        $(mycollose).collapse('show');
    }
    else{
        $(mycollose).collapse('hide');
    }
}

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

$(function () { $("[data-toggle='tooltip']").tooltip(); });