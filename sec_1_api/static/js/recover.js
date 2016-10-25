$(document).ready(function() {
	$("#recover-email-form").submit(function(event){
		var $form = $(this);

		var data = JSON.stringify($form.serializeObject());

		var request = $.ajax({
			url: "/sendrecover",
			type: "POST",
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: data
		})

		request.done(function(response, textStatus, jqXHR){
			toggleVisibility();
		})

		request.fail(function(jqXHR, textStatus, errorThrown){
			console.log("fail");
		})

		return false;
	})

	$("#recover-code-form").submit(function(event){
		var $form = $(this);

		var data = $form.serializeObject();
		var emailFormData = $("#recover-email-form").serializeObject();
		data["email"] = emailFormData.email;

		var request = $.ajax({
			url: "/recover",
			type: "POST",
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: JSON.stringify(data)
		})

		request.done(function(response, textStatus, jqXHR){
		})

		request.fail(function(jqXHR, textStatus, errorThrown){
		})

		return false;
	})

	$("#stepBack").click(function(){
		toggleVisibility();
	})
})

toggleVisibility = function() {
	$("#recover-email-form").toggle();
	$("#recover-code-form").toggle();
}