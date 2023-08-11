
$(function () {

    //1.初始化Add Init Table
    var oInitTable = new systemVariableInit();
    oInitTable.Init();

    $(window).resize(function (){
        var page_height = $(window).height();
        $( '#var_tb_case' ).bootstrapTable('resetView',{ height: page_height - 250 } );
    });
});

window.operateEvents = {
    'click .var_delete': function (e, value, row, index) {
        $.ajax({
            type: "PUT",
            headers: {"X-CSRFToken": csrf_token},
            url: "/api/case/variable/delete/",
            data: JSON.stringify({
                "id": row['id'],
                "status": "N",
                "lastdate": get_date(),
                "lastuser": current_user
            }),
            contentType: "application/json; charset=UTF-8",
            success: function (data) {
                if (data["code"] != 0) {
                    toastr.info("warning", data.msg);
                    return;
                }
                toastr.success("success", '删除成功');
                $("#var_tb_case").bootstrapTable("refresh");
                // $("#var_tb_case").bootstrapTable('remove', {
                //     field: 'id',
                //     values: [row['id']]
                // });
            }
        });

        return false;
    }
};

var systemVariableInit = function () {

    var oTableInit = new Object();
    //初始化Table

    oTableInit.Init = function () {
        $('#var_tb_case').bootstrapTable({
            url: '/api/case/search/variable/',         //请求后台的URL（*）
            method: 'GET',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            height: $(window).height() - 250,
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            paginationPreText: "上一页",
            paginationNextText: "下一页",
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: false,
            showColumns: false,                  //是否显示所有的列
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
                field: 'id',
                title: '变量id',
                visible: false
            }, {
                field: 'operate',
                align: 'center',
                width: "100px",
                events: operateEvents,
                formatter: operateFormatter,
                title: '操作'
            }, {
                field: 'name',
                title: '变量名称',
                align: 'left'
            }, {
                field: 'type',
                title: '变量类型',
                align: 'left'
            }, {
                field: 'action',
                title: '变量行为',
                align: 'left'
            },  {
                field: 'value',
                title: '变量值',
                align: 'left'
            },
                {
                field: 'status',
                title: '是否有效',
                align: 'left'
            }, {
                field: 'lastuser',
                title: '最后修改人',
                align: 'left'
            }, {
                field: 'lastdate',
                title: '最后更新时间',
                align: 'left'
            }]
        });

        function operateFormatter(value, row, index) {
            return [
                '<a class="var_update" style="cursor: pointer" data-toggle="modal" data-target="#updateSystemVariable" title="Update" onclick="update_var(' + row.id + ', ' + index + ')">',
                '<span>编辑</span>',
                '</a>&nbsp;&nbsp;&nbsp;&nbsp;',
                '<a class="var_delete" href="javascript:void(0)" title="Delete">',
                '<span>删除</span>',
                '</a>',
            ].join('');
        };
    };
    //得到查询的参数
    oTableInit.queryParams = function (params) {

        var action = $("#txt_var_select_action").val().trim();
        if(action=="div"){
            action = "division";
        }

        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            name: $("#txt_var_select_name").val().trim(),
            action: action,
            type: $("#sel_var_select_type").val().trim(),
            status: $("#sel_var_select_useful").val() == "否" ? "N" : "Y",
            page_index: (params.offset / params.limit) + 1,
            page_size: params.limit,
        };
        return temp;
    };
    return oTableInit;
};

function getNow(s) {
    return s < 10 ? '0' + s : s;
}

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

function update_var(id, index) {
    if (id) {
        $.ajax({
            type: "POST",
            headers: {"X-CSRFToken": csrf_token},
            url: "/api/case/variable/id/",
            data: JSON.stringify({
                "id": id
            }),
            contentType: "application/json; charset=UTF-8",
            success: function (data) {
                if (data['code'] != 0) {
                    toastr.warning("info", data.message);
                    return;
                }
                $("#txt_var_update_name").val(data.data.name);
                $("#txt_var_update_value").val(data.data.value);
                $("#sel_var_update_type").selectpicker('val', data.data.type);
                $("#sel_var_update_act").selectpicker('val', data.data.action);
                $("#sel_var_update_status").selectpicker('val', data.data.status =="Y" ? '是':'否');
                $("#update_id").val(id);
                $("#update_index").val(index);

            },
            error: function () {
                toastr.error("error", "获取数据异常");
            }

        });
    }
};


function add_var() {
    var var_name = $("#txt_var_name").val();
    var var_value = $("#txt_var_value").val();
    if (var_name == "" || var_value == "") {
        toastr.warning("info", "变量名称和变量值不能为空！");
        return
    }

    $.ajax({
        type: "POST",
        headers: {"X-CSRFToken": csrf_token},
        url: "/api/case/variable/add/",
        data: JSON.stringify({
            "name": var_name,
            "value": var_value,
            "status": $("#sel_var_add_status").val()=="是" ? "Y":"N",
            "action": $("#sel_var_act").val(),
            "type": $("#sel_var_type").val(),
            "indate": get_date(),
            "inuser": current_user,
            "lastdate": get_date(),
            "lastuser": current_user
        }),
        contentType: "application/json; charset=UTF-8",
        success: function (data) {
            if (data["code"] != 0) {
                toastr.warning("info", data.message);
                return;
            }
            $("#var_btn_cancel").click();
            $('#var_tb_case').bootstrapTable('insertRow', {index: 0, row: data.origin_data})
            toastr.success("success", "新增成功");
        },
        error: function () {
            toastr.error("error", "获取数据异常");
        }

    });
};


function save_update_var() {
    var id = $("#update_id").val();
    var index = $("#update_index").val();
    if (id) {
        $.ajax({
            type: "PUT",
            headers: {"X-CSRFToken": csrf_token},
            url: "/api/case/variable/update/",
            data: JSON.stringify({
                "id": id,
                "name": $("#txt_var_update_name").val(),
                "value": $("#txt_var_update_value").val(),
                "action": $("#sel_var_update_act").val(),
                "type": $("#sel_var_update_type").val(),
                "status":$("#sel_var_update_status").val() =="是" ? 'Y':'N',
                "lastdate": get_date()
            }),
            contentType: "application/json; charset=UTF-8",
            success: function (data) {
                if (data["code"] != 0) {
                    toastr.warning("info", data.message);
                    return;
                }
                $("#var_update_btn_cancel").click();
                $('#var_tb_case').bootstrapTable('updateRow', {index: index, row:data.origin_data });
                toastr.success("success", "更新成功");
            },
            error: function () {
                toastr.error("error", "获取数据异常");
            }

        });
    }
}

$("#var_select_btn_query").click(function () {
    $("#var_tb_case").bootstrapTable('selectPage', 1);
});

$(document).keydown(function (event) {
    if (event.keyCode == 13) {
        $('#var_select_btn_query').triggerHandler('click');
    }
});