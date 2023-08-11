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


