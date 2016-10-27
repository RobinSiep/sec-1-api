$(document).ready(function() {
	$("#login-form").submit(function(event){
		var $form = $(this);

		var data = JSON.stringify($form.serializeObject());

		var request = $.ajax({
			url: "/login",
			type: "POST",
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: data
		})

		request.done(function(response, textStatus, jqXHR){
			window.location.replace("home")
		})

		request.fail(function(jqXHR, textStatus, errorThrown){
			refreshCaptcha();
			showErrors(JSON.parse(jqXHR.responseText))
		})

		return false;
})
})