

$(function () {
    var oTable = new TableInit();
    oTable.Init();

    var runTable = new RunCaseTableInit();
    runTable.Init();

    $(window).resize(function (){
        var page_height = $(window).height();
        $( '#tb_new_case' ).bootstrapTable('resetView',{ height: page_height - 80 } );
        var page_height = $(window).height();
        $( '#tb_run_case' ).bootstrapTable('resetView',{ height: page_height - 80 } );
});
});

var TableInit = function () {
    var oTableInit = new Object();
    var page_height = $(window).height();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_new_case').bootstrapTable({
            url: '/api/case/last_case/',         //请求后台的URL（*）
            method: 'GET',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            queryParams: oTableInit.queryParams,//传递参数（*）
            height: page_height - 80,
            sortOrder: "asc",                   //排序方式
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            paginationPreText:"上一页",
            paginationNextText:"下一页",
            pageSize: 20,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
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
                field: 'case_id',
                title: 'ID',
                visible: true,
            }, {
                field: 'case_name',
                title: '用例名称',
                align:'left',
                class: 'col-case-name',
                formatter: showCaseNameFormatter,
            }, {
                field: 'case_from_system_name',
                title: '用例系统',
                align: 'left',
            }, {
                field: 'case_author',
                title: '用例作者',
                align:'left'
            }, {
                field: 'case_last_date',
                title: '最新修改时间',
                align:'left'
            }]
        });
    };

    function showCaseNameFormatter(value, row, index) {
        return "<div style='width:240px;text-overflow: ellipsis;overflow: hidden;'>" + value + "</div>"
    };

    oTableInit.subqueryParams = function(params){
      var temp = {

      };
      return temp;
    };
    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            case_from_system: $("#txt_case_from_system").val(),
            case_description: $("#txt_case_description").val(),
            case_name: $("#txt_case_name").val(),
            case_id:$("#txt_case_id").val(),
            case_is_exec: $("#is_run").val(),
            case_executor: $("#txt_case_device").val(),
            case_exec_group:$("#txt_case_exec_group").val(),
            case_exec_priority:$("#txt_case_exce_priority").val(),
            page_index: (params.offset / params.limit) + 1,
            page_size: params.limit,
        };
        return temp;
    };
    return oTableInit;
};

var RunCaseTableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    var page_height = $(window).height();
    oTableInit.Init = function () {
        $('#tb_run_case').bootstrapTable({
            url: '/api/case/history/last_update',         //请求后台的URL（*）
            method: 'GET',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            queryParams: oTableInit.queryParams,//传递参数（*）
            height: page_height - 80,
            pageSize: 20,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            sortOrder: "asc",                   //排序方式
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            paginationPreText:"上一页",
            paginationNextText:"下一页",
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
                field: 'run_id',
                title: 'ID',
                visible: true,
            }, {
                field: 'run_status',
                title: '总状态',
                formatter: resultFormat,
                align:'left'
            }, {
                field: 'run_from_system',
                title: '系统',
                align: 'left'
            }, {
                field: 'run_case_count',
                title: '执行数',
                align:'left'
            }, {
                field: 'run_success',
                title: '成功数',
                align:'left'
            }, {
                field: 'run_fail',
                title: '失败数',
                align:'left'
            }, {
                field: 'run_success_rate',
                title: '成功率',
                formatter: successRateFormat,
                align:'left'
            }, {
                field: 'run_durations',
                title: '执行耗时',
                formatter: runtTimeFormat,
                align:'left'
            }, {
                field: 'run_created_at',
                title: '执行时间',
                align:'left'
            }]
        });
    };

    function decimal(num,v){
        var vv = Math.pow(10,v);
        return Math.round(num*vv)/vv;
    }

    function resultFormat(value, row, index){
        if (value == 0 ){
            return "失败"
        }
        else{
            return "成功"
        }
    }

    function decimal(num,v){
        var vv = Math.pow(10,v);
        return Math.round(num*vv)/vv;
    }

    function successRateFormat(value, row, index) {
        return (decimal(value* 100, 2)).toString() + "%"
    }

    function runtTimeFormat(value, row, index) {
        var seconds = parseInt(value / 1000);
        var ret = "";
        if(seconds < 60)
        {
            ret = seconds.toString() + "秒";
        }else {
            var minutes = parseInt(seconds / 60);
            var seoonds = seconds % 60;
            if (minutes < 60){
                ret = minutes.toString() + "分" + seoonds + "秒";
            }
            else {
                var hour = parseInt(minutes / 60);
                var minutes = minutes % 60;
                ret = hour.toString() + "时" + minutes.toString() + "分" + seoonds + "秒";
            }
        }
        return ret
    }

    function reportFormat(value, row, index) {
        return '<a href="#">详情</a>'
    }

    oTableInit.subqueryParams = function(params){
      var temp = {

      };
      return temp;
    };
    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            case_from_system: $("#txt_case_from_system").val(),
            case_description: $("#txt_case_description").val(),
            case_name: $("#txt_case_name").val(),
            case_id:$("#txt_case_id").val(),
            case_is_exec: $("#is_run").val(),
            case_executor: $("#txt_case_device").val(),
            case_exec_group:$("#txt_case_exec_group").val(),
            case_exec_priority:$("#txt_case_exce_priority").val(),
            page_index: (params.offset / params.limit) + 1,
            page_size: params.limit,
        };
        return temp;
    };
    return oTableInit;
};