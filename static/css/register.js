$(document).ready(function () {
	$('#faculty').css("display","none");
	
$("input[name='ask']").change(function(){
	    if ($("input[name='ask']:checked").val() == 'Y'){
	$('#student').css("display","block");
	$('#faculty').css("display","none");}
		    else if ($("input[name='ask']:checked").val() == 'N'){
	$('#faculty').css("display","block");
	$('#student').css("display","none");}
				});


	});
