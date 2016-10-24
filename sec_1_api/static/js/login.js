$(document).ready(function() {
	$("#login-form").submit(function(event){
		var $form = $(this);

		var data = JSON.stringify($form.serializeObject());

		console.log(data);
		var request = $.ajax({
			url: "/login",
			type: "POST",
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: data
		})

		request.done(function(response, textStatus, jqXHR){
			console.log("worked");
			window.location.replace("home")
		})

		request.fail(function(jqXHR, textStatus, errorThrown){
			console.log("fail");
		})

		return false;
})
})