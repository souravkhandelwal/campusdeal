$(document).ready(function(){
	//$('#submit').live("click",function(){
		//var bid=$('#mybid').val();
		//var id=$('#item_itemimage').attr("orderid");
//		if(id.attr("title")==""){
        //alert("Hi");
			$.ajax({
				type : 'GET',
				url : '/campusdeal/myitems',
				//              url : 'http://google.com',
				data: {
				//	p : bid
				},
				success: function(data) {
                    //alert(data);
//					$('#result').text(data);
					split_str = data.split('****');
				//	split_str[0]
                    //alert(split_str[0]);
					for(i=1;i<=parseInt(split_str[0])*5;i=i+5){
                        //alert(i);
					var item = $("<div class='myitem' id='"+split_str[i+4]+"'><div class='myitem_image'><img src='"+split_str[i]+"' width='100' height='100'></div> <div class='myitem_rest'>"+
							"<div class='myitem_title'>"+split_str[i+1]+"</div><div class='myitem_baseprice'>BasePrice : "+split_str[i+2]+"</div><div class='myitem_category'>Category : "+split_str[i+3]+"</div></div></div>");
							$('#itemlist').append(item);
						}
					 }
			});
		//});
		$(".myitem").live("click",function(){
			id=$(this).attr("id");
			$.ajax({
				type : 'GET',
				url : '/campusdeal/bids',
				//              url : 'http://google.com',
				data: {
					q : id
				},
				success: function(data) {
                    $('#bidlist .placed_bid').remove();
                    //alert(data);
//					$('#result').text(data);
					split_str = data.split('****');
				//	split_str[0]
					for(i=1;i<=parseInt(split_str[0])*4;i=i+4){
					var item = $("<div class='placed_bid' ><input type='radio' id='"+split_str[i]+"' name='bid_button' value='"+split_str[i+1]+"'>"+split_str[i+2]+" bid with Rs "+split_str[i+3]+"</div>");
							item.insertAfter('#bidlist_title');
						}
					 }
			});

					
		});
		$('#sell_button').click(function(){
				id=	$('input[name=bid_button]:checked').attr("id");
				$.ajax({
				type : 'GET',
				url : '/campusdeal/accept_bid',
				//              url : 'http://google.com',
				data: {
					q : id
				},
				success: function(data) {
//					$('#result').text(data);
				//	split_str[0]
					alert(data);
				}
			});
		});
//	});
});

