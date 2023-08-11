$(function () {
    set_content_height();
    $(window).resize(function (){
        set_content_height()
    });
    $(window).on('load', function () {
        $('#sel_captial').selectpicker({
            'selectedText': 'hami_tianshan',
        });
    });

    $('#sel_add_type').selectpicker({"width": 200});
    $("#sel_add_type").selectpicker("refresh");

    $('#sel_pro_env').selectpicker({"width": 100});
    $("#sel_pro_env").selectpicker("refresh");

    $('#sel_grant_day').selectpicker({"width": 80});
    $("#sel_grant_day").selectpicker("refresh");

    $('#sel_country').selectpicker({"width": 80});
    $("#sel_country").selectpicker("refresh");

    $('#sel_count').selectpicker({"width": 80});
    $("#sel_count").selectpicker("refresh");

    $('#sel_loan_channel').selectpicker({"width": 120});
    $("#sel_loan_channel").selectpicker("refresh");

    $("#sel_add_type").on("changed.bs.select", function (e) {
        console.log(this, $(this).val());
        $("#add_exist_content").addClass("hidden");
        $("#auto_create_content").addClass("hidden");
        if($(this).val() == 'add_exist'){
            $("#add_exist_content").removeClass("hidden")
        }else {
            $("#auto_create_content").removeClass("hidden")
        }
    });

    $('#sel_captial').selectpicker({"width": 120});
    $("#sel_captial").selectpicker("refresh");

    $('#sel_captial_period').selectpicker({"width": 100});
    $("#sel_captial_period").selectpicker("refresh");

    $("#sel_base_url").selectpicker({"width": 100});
    $("#sel_base_url").selectpicker("refresh");

    $("#add_asset").click(function () {

        $("#addAsset").modal('show');
    });

    $("#btn_asset_create").click(function () {
        $("#btn_asset_create_cancel").click();
    });

    $(".workspace_header_program_ul.dropdown-menu a").click(function () {
        var  sel_program_str = $("#dropdown_program").html(),
             country = $("#dropdown_country").val(),
             display_str = $(this).html();
        if(sel_program_str.indexOf(display_str) <= -1){
            $("#dropdown_program").val($(this).attr("id"));
            $("#dropdown_program").html('' + display_str +
                '                <span class="caret"></span>');
            change_env_list(country, $(this).attr("id"));
        }
    });

    $(".workspace_header_country_ul.dropdown-menu a").click(function () {
        var sel_country_str = $("#dropdown_country").html(),
            program = $("#dropdown_program").val(),
            display_str = $(this).html();
        if(sel_country_str.indexOf(display_str) <= -1){
            $("#dropdown_country").val($(this).attr("id"));
            $("#dropdown_country").html('' + display_str +
                '                <span class="caret"></span>');
            change_env_list($(this).attr("id"), program);
            var env = $("#sel_pro_env").val(),
                pro = $("#sel_base_url").val();
            change_base_url($(this).attr("id"), env, pro);
        }
    });

    $("#sel_base_url").on("changed.bs.select", function (e){
        var country = $("#dropdown_country").val(),
            env = $("#sel_pro_env").val();
        console.log($(this).val(), country, env);
        change_base_url(country, env, $(this).val());
    });

    $("#sel_pro_env").on("changed.bs.select", function (e){
        var country = $("#dropdown_country").val(),
            pro = $("#sel_base_url").val();
        console.log('sel_pro_env', $(this).val(), country, pro);
        change_base_url(country, $(this).val(), pro);
    });

    // $(".workspace_program li").click(function () {
    //     $(".workspace_program li").removeClass("active");
    //     $(this).addClass("active");
    //     var pro_list = $(this).find("a").attr("id").split("_"),
    //         env = $("#sel_base_url").val(),
    //         country = $("#dropdown_country").val(),
    //         pro = pro_list[pro_list.length - 1];
    //     // $.each(program_url_config[country], function (name, value) {
    //     //     console.log(name, value[env].replace("{0}", pro));
    //     // });
    //     change_base_url(country, env, pro);
    //     //save_cache("case_sel_program", pro);
    //     // setTimeout(function () {
    //     //     $("#tb_case").bootstrapTable("refresh");
    //     // }, 100);
    // });


});

function change_base_url(country, env, pro) {
    $.each($(".base-url-ul a"), function (index, item) {
        console.log(index, item, country, env, pro);
        if(index > 1){
            var name = $(this).text();
            console.log(name, program_url_config[country][name][pro]);
            if(program_url_config[country][name][pro]){
                $(this).attr("href", program_url_config[country][name][pro].replace("{0}", env));
                $(this).parent().removeClass("hidden");
            }else{
                $(this).attr("href", program_url_config[country][name][pro]);
                $(this).parent().addClass("hidden");
            }
        }
    });
}

function change_env_list(country, program) {
    console.log("country", country, program);
    $.each($(".workspace_program"), function (index, item) {
        var id = $(item).attr("id").replace("ul_program_", "").split("_");
        if(country == id[0] && program == id[1]){
            $(this).removeClass('hidden');
            $(this).find("a:first").click();
        }
        else{
            $(this).addClass("hidden")
        }
    });
}

function set_content_height() {
    $('.content-show').css('height',{ height: $(window).height() - 150 } );
}