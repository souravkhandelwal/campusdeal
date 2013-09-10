$(document).ready(function () {

//	alert("Hi");
	$(".user").bind("mouseover",function(){
	id=$(this).attr("id");
//	alert(id)
	$.ajax({
	type : 'GET',
	url : '/campusdeal/user_info',
	// url : 'http://google.com',
	data: {
	q : id
	},
	success: function(data) {
	// $('#result').text(data);
//	alert(data);
	split_str = data.split('****');
	// split_str[0]
	data1="";
	for(i=1;i<=4;i++){
		data1+=split_str[i-1];
		data1+="</br>";
	}
	$("<div id='info'>" + data1 + "</div>").appendTo("body");
	var e;
	if (!e) e = window.event;
//	$('#info').css('z-index','10000000').css('position','absolute').css('height','40px').css('top',e.clientY).css('left',e.clientX).css('display','block').css('width','40px').css('padding','10px').css('margin','0px');
//	alert($('#info').html());
	}

	});




	});
});
