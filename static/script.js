$(document).ready(function () {
    $(".hover").hover(function () {
    $(this).find('ul').slideDown('medium');
    },
    function (){
    $(this).find('ul').slideUp('medium');
	});
});




