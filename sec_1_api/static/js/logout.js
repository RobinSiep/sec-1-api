$(document).ready(function() {
	$("#logout").click(function() {
		var request = $.ajax({
			url: "/logout",
			type: "GET",
			contentType: "application/json; charset=utf-8"
		})

		request.done(function(response, textStatus, jqXHR){
			window.location.replace("/")
		})
	})
})