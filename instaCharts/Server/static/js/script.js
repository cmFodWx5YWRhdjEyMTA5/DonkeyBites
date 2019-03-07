$(function(){
	$('button').click(function(){
		var user = $('#txtUsername').val();
		var pass = $('#txtPassword').val();
		$.ajax({
			url: '/signUpUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				
				if (response == 'ok'){
					window.alert("you have signed in");
				} else { 
					window.alert("wrong user or password");
				}
			},
			error: function(error){

				console.log(error);
				
			}
		});
	});
});
