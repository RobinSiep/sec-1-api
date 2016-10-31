$(document).ready(function() {
	$("#firmware-form").submit(function(event) {
		event.preventDefault();
		var $form = $(this);
		var fd = new FormData();

		$form.find("#upload").attr("value", "uploading...");
		var file = $form.find("#inputFirmware").prop('files')[0];
		console.log(file)

		if (file == undefined) {
			showErrors({firmware: "No file selected"})
			return
		} else if (!file.type.match('zip.*')) {
			showErrors({firmware: "File is not a .zip!"})
			return
		}

		fd.append('firmware', file, file.name);

		var xhr = new XMLHttpRequest();

		xhr.open('POST', 'firmware', true)

		//xhr.setRequestHeader(
		//	'content-type',
		//	'application/x-www-form-urlencoded'
		//);

		xhr.onload = function() {
			if (xhr.status == 200) {
				console.log("true");
			} else {
				console.log("false");
			}
		}

		xhr.send(fd);

	})

	return false;
})