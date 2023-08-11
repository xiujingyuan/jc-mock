$(function () {

    $.each($("#left_menu li"), function (i, item) {
        var path_name = window.location.pathname,
            child_a = $(item).children('a').eq(0),
            child_a_id = child_a.attr("id").replace("menu_", "");
        if(child_a.attr("href") == path_name || path_name.indexOf(child_a_id) > -1){
            $(item).addClass("active")
        }
    });

    $('#sidebar_tests').on("click",function () {
        $('#sidebar_tests').controlSidebar("");
    });

    $.each($("i.fa-heart-o"), function (index, item) {
           $(item).on("click", function () {
                if($(item).hasClass("checked")){
                    $(item).removeClass("checked");
                }
                else{
                    $(item).addClass("checked");
                }
        });
    });

    var menu_list = ["menu_assumpt_task", "menu_report", "second_menu"];

    $.each(menu_list, function (i, menu) {

        $("#" + menu).on("mouseleave",function () {
            $("#" + menu).secondMneuSidebar(true);
            $(".control-sidebar").removeClass("test");
        });
        $("#" + menu).on("mouseenter",function () {
            $(".control-sidebar").addClass("test");
            $("#" + menu).secondMneuSidebar(true);
            // change_menu_href(menu);
            change_second_menu(menu);
        });

    });

    $('ul.sidebar-menu li').click(function () {
        var li = $('ul.sidebar-menu li.active');
        var first = $(this).children(":first");
        if(!($.inArray(first.attr("id"), menu_list) > -1)){
            li.removeClass('active');
            $(this).addClass('active');
        }
    });

    $(".sidebar-toggle").click();

    $('.myLeftMenu').click(function (e) {

        var url = $(this).attr('data');
      //  console.log(url);
        $('#container').load(url);
    });

    // bootstrap响应式导航条<br>;(function($, window, undefined) {
    //

    // keep track of all dropdowns
    var $allDropdowns = $();

    // if instantlyCloseOthers is true, then it will instantly
    // shut other nav items when a new one is hovered over
    $.fn.dropdownHover = function(options) {

        // the element we really care about
        // is the dropdown-toggle's parent
        $allDropdowns = $allDropdowns.add(this.parent());

        return this.each(function() {
            var $this = $(this).parent(),
                defaults = {
                    delay: 500,
                    instantlyCloseOthers: true
                },
                data = {
                    delay: $(this).data('delay'),
                    instantlyCloseOthers: $(this).data('close-others')
                },
                options = $.extend(true, {}, defaults, options, data),
                timeout;

            $this.hover(function() {
                console.log("hover ", $(this), options.instantlyCloseOthers);
                if(options.instantlyCloseOthers === true)
                    $allDropdowns.removeClass('open');

                window.clearTimeout(timeout);
                $(this).addClass('open');
            }, function() {
                timeout = window.setTimeout(function() {
                    $this.removeClass('open');
                }, options.delay);
            });
        });
    };

    $('[data-hover="dropdown"]').dropdownHover();

    function change_second_menu(menu) {
        if(menu == "menu_report"){
            $("#control-sidebar-group-tab").removeClass("hidden");
            $("#control-sidebar-program-tab").addClass("hidden");
        }
        else if (menu == "menu_assumpt_task"){
            $("#control-sidebar-group-tab").addClass("hidden");
            $("#control-sidebar-program-tab").removeClass("hidden");
        }
    }

    function change_menu_href(menu) {
        console.log(menu);
        var menu_url = "";
        if(menu == "menu_assumpt_task"){
            menu_url = "/assumpt_task/";
        }
        else if (menu == "menu_report"){
            menu_url = "/report/new/";
        }
        if(menu == "second_menu"){

        }
        else {
            $.each($("#control-sidebar-program-tab a"), function (i, item) {
                console.log(item);
                var program_list = $(item).attr("href").split("/"),
                    program_id = program_list[program_list.length - 2];
                $(item).attr("href", menu_url + program_id + "/");
            })
        }
    }

});


