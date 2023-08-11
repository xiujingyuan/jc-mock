$(function () {
    var content_height = $('#page_menu').height();
    $('#data-panel').height(content_height - 80);
    var page_menu = $('#page_menu').height();
    $("#coverage_content").height(page_menu);
    set_jacoco_height();
    $(window).resize(function () {
        set_jacoco_height();
    });
});

function set_jacoco_height() {
    $(".jacoco-content-show").css("height", $(window).height() - 100);
    $(".jacoco-div-show").css("height", $(window).height() - 100);
}

var ContentTableInit = function (data) {
    var oTableInit = new Object();
    //初始化Table

    oTableInit.Init = function () {
        $("#tb_content").bootstrapTable({
            data: data,
            method: 'GET',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: true,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            sortName: 'miss_line',//排序字段
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            paginationPreText: "上一页",
            paginationNextText: "下一页",
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 20, 50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: false,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: false,                //是否启用点击选中行
            queryParams: oTableInit.queryParams,
            //height: 700,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle: false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            sortStable:true,
            columns: [
                {
                field: 'fileName',
                title: '文件名',
                align: 'left',
                formatter: showName,
            }, {
                field: 'miss_line',
                title: '未覆盖',
                align: 'center',
                sortable: true
            }, {
                field: 'total_line',
                title: '总行数',
                align: 'center',
                halign: 'center',
                sortable: true
            }, {
                field: 'coverage',
                title: '覆盖率',
                align: 'center',
                align: 'center',
                sortable: true
            },{
                field: 'filter_line',
                title: '逻辑总行',
                align: 'center',
                halign: 'center',
                sortable: true
            }, {
                field: 'filter_coverage',
                title: '逻辑覆盖率',
                align: 'center',
                halign: 'center',
                sortable: true
            }, ],
            onSort: function (sortName, sortOrder) {
                var order = sortOrder === 'desc' ? -1 : 1;
                var reserve = sortOrder === 'desc' ? 1 : -1;
                var mydata = $('#tb_content').bootstrapTable('getData');
                var total = mydata.shift();
                var total_calc = mydata.shift();
                mydata.sort(function (a,b) {
                    if(a[sortName] > b[sortName]){
                        return order
                    }
                    else if (a[sortName] < b[sortName]){
                        return reserve
                    }
                    else {
                        return 0
                    }
                });
                mydata.unshift(total_calc);
                mydata.unshift(total);
                $("#tb_content").bootstrapTable("load", mydata);
            },
            onClickCell:function(field, value, row, $element)
            {
                if(field == "fileName"){
                    var nodes = $('#record-tree').treeview('getNode', 0);
                    var is_out = false;
                    $.each(nodes.nodes, function () {
                        var item_nodes  = $('#record-tree').treeview('getNode', this.nodeId);
                        $.each(item_nodes.nodes, function () {
                            var value_list = value.split("/");
                            var name = value_list[value_list.length - 1];
                            if(this.text == name){
                                $('#record-tree').treeview('collapseAll', { silent: true });
                                $('#record-tree').treeview('revealNode', [ this.nodeId, { silent: true } ]);
                                $('#record-tree').treeview('selectNode', [ this.nodeId, { silent: false } ]);
                                is_out = true;
                                return
                            }
                        });

                        if(is_out){
                            return
                        }
                    });
                }

            }
        });

        function showName(value, row, index, field) {
            var head = value.split("/")[0].length;
            if(value.length >= 100){
                value = value.substring(0, head + 1) + "..." + value.substring(head + value.length - 99, value.length)
            }
            return value
        }


    };

    return oTableInit;
};

function init_tree(data, system, branch, csrf_token) {
    var assumpt_table = ContentTableInit(data[0]["content"]);
    assumpt_table.Init();
    $("#tb_content").removeClass("hidden");
    $("#data-panel").addClass("hidden");
    $("#record-tree").treeview({
        data: JSON.parse(JSON.stringify(data)),// 赋值
        highlightSelected: true,// 选中项不高亮，避免和上述制定的颜色变化规则冲突
        multiSelect: false,// 不允许多选，因为我们要通过check框来控制
        showCheckbox: false,// 展示checkbox
        highlightSearchResults: false, // 高亮查询结果
        levels: 2, // 展开级别 Default: 2
        searchResultBackColor: '#CCC', // 查找背景
        //selectedIcon: 'glyphicon glyphicon-tint',
        showTags: true,
        onNodeSelected: function (event, data) {
            if(data.text.endsWith(".java")){
                $.ajax({
                type: "POST",
                url: "/api/coverage/content",
                headers: {"X-CSRFToken": csrf_token,
                        "content-type": "application/json"},
                data: JSON.stringify({
                    "url": data["src"],
                    "lines": data["content"]["missLines"],
                    "addLines": data["content"]["addLines"],
                    "filterLines": data["content"]["filterLines"],
                    "system": system,
                    "branch": branch
                }),
                dataType: 'JSON',
                success: function (response) {
                    $("#tb_content").addClass("hidden");
                    $("#data-panel").removeClass("hidden");
                    if (response["code"] == 1) {
                        toastr.warning(response["message"], "warning");
                        $("#data-panel").html(response["message"]).show();
                    }
                    else {
                         $("#data-panel").html(response["data"]).show();
                         console.log(response["message"], "success");
                    }
                },
                error: function () {
                    toastr.error("网络异常，请求失败", "error");
                }

            });
            }
            else{
                $("#tb_content").bootstrapTable("load", data.content);
                $("#tb_content").removeClass("hidden");
                $("#data-panel").addClass("hidden");
            }
        }
    });
};

$("#tree-query").on("keyup", function () {
    var value = $.trim($(this).val());
    if (value.length > 0) {
        // 先折叠
        $('#record-tree').treeview('collapseAll', {silent: true});
        // 自动展开结果，返回搜索到的集合
        var nodes = $("#record-tree").treeview('clearSearch').treeview('search', [value, {
            ignoreCase: false,    // 忽略大小写
            exactMatch: false,   // like or equals
            revealResults: true, // reveal matching nodes
        }]);
    } else {
        $('#record-tree').treeview('clearSearch').treeview('expandAll', {levels:2, silent: true});
    }
});
