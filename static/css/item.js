$(document).ready(function(){
	$('#submit').live("click",function(){
			var bid=$('#mybid').val();
			var id=$('#item_itemimage').attr("orderid");
//			if(id.attr("title")==""){
			$.ajax({
				type : 'GET',
				url : '/campusdeal/updateBidder/'+id,
//				url : 'http://google.com',
				data: {
					p : bid,
					q : id
				},
				success: function(data) {
					$('#result').text(data);
				}
			});
	});	
});
