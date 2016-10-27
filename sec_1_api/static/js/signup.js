$(document).ready(function() {
	$("#signup-form").submit(function(event){
		var $form = $(this);

		var data = $form.serializeObject();

		var request = $.ajax({
			url: "/register",
			type: "POST",
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: JSON.stringify(data)
		})

		request.done(function(response, textStatus, jqXHR){
			var loginData = {password: data.password, username: data.username}
			var loginRequest = $.ajax({
				url: "/login",
				type: "POST",
				contentType: "application/json; charset=utf-8",
				dataType: "json",
				data: JSON.stringify(loginData)
			})

			loginRequest.done(function(response, textStatus, jqXHR){
				window.location.replace("home")
			})

			request.fail(function(jqXHR, textStatus, errorThrown){
				window.location.replace("/")
			})
		})

		request.fail(function(jqXHR, textStatus, errorThrown){
			refreshCaptcha();
			showErrors(JSON.parse(jqXHR.responseText))
		})

		return false;
})
})