
$(document).ready(function () {

	$('#login-button').live("mouseenter",function(){
//		$('#login-box').animate({opacity: 0.25,height: 'toggle'}, 600);
		if($('.login-box').css("display")!="block")
			$('.login-box').css("display","block");
		else
			$('.login-box').css("display","none");

	});
	$('#login-button').live("mouseleave",function(){
//		$('#login-box').animate({opacity: 0.25,height: 'toggle'}, 600);
		if($('.login-box').css("display")=="block")
			$('.login-box').css("display","none");
	});
});
