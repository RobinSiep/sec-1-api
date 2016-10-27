$(document).ready(function() {
	$("#device-form").submit(function(event){
		var $form = $(this);

		var data = JSON.stringify($form.serializeObject());

		var request = $.ajax({
			url: "device",
			type: "PUT",
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: data
		})

		request.done(function(response, textStatus, jqXHR){
			location.reload();
		})

		request.fail(function(jqXHR, textStatus, errorThrown){
			showErrors(JSON.parse(jqXHR.responseText));
		})

		return false;
	})
})

remove = function(name) {
	data = JSON.stringify({name: name})

	var request = $.ajax({
			url: "device",
			type: "DELETE",
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: data
		})

		request.done(function(response, textStatus, jqXHR){
			location.reload();
		})
}