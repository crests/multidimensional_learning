jQuery(document).ready(function(){
	$('#subscribeform').submit(function(){

		var action = $(this).attr('action');

		$("#entry").slideUp(750,function() {
		$('#entry').hide();

 		$('#subsubmit')
			.after('')
			.attr('disabled','disabled');

		$.post(action, {
			email: $('#subemail').val()
		},
			function(data){
				document.getElementById('mesaj').innerHTML = data;
				$('#entry').slideDown('slow');
				$('#subscribeform img.subscribe-loader').fadeOut('slow',function(){$(this).remove()});
				$('#subsubmit').removeAttr('disabled');
				if(data.match('success') != null) $('#subscribeform').slideUp('slow');
			}
		);

		});

		return false;

	});

});
