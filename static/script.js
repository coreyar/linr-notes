$(document).ready(function () {
    $(".hover").hover(function () {
    $(this).find('ul').slideDown('medium');
    },
    function (){
    $(this).find('ul').slideUp('medium');
	});
});









// $(document).ready(function() {
//     $('div').click(function() {
//         $('div').fadeOut('slow');
//     });
// });


// $(document).ready() {
// 	$(".hoverli").hover(function() {
// 			$(".track-info").slideDown('slow');
// 	}, function(){
// 		$(".track-info").slideUp("slow");
// 	}
// 	});
// $(document).ready(function () {
// $('.hoverli ul').hover(
//     function() { $('li', $(this)).show(); },
//     function() { $('li', $(this)).hide(); }
// )	
// )};

// $(document).ready(function () {
// 	$(".hoverli").hover(
// 		function(){
// 			$(this).children(".track-info").slideToggle();

// 		},
// 		function(){
// 			$(this).siblings(".track-info").slideDown('medium');
// 		}
// 		);
// });
//
//
//

// $(document).ready(function () {
//     $(".hoverli").hover(
//   function () {
//      $('ul.track-info').slideDown('medium');
//   }, 
//   function () {
//      $('ul.track-info').slideUp('medium');
//   }
// );

// });