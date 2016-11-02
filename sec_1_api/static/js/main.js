var default_error_p = "<p class='help-block error'>{}</p>"


$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

showSnackbar = function(message) {
    var options =  {
        content: "pattern saved", // text of the snackbar
        style: "snackbar", // add a custom class to your snackbar
        timeout: 2000 // time in milliseconds after the snackbar autohides, 0 is disabled
    }
    $.snackbar(options);
}


showErrors = function(errors, elementType='input') {
    // Loop through all errors and show the error message below the affected input.
    for (var key in errors) {
        var error = default_error_p.replace("{}", errors[key]);

        var focusInput = $("" + elementType +"[name=" + key +"]");
        
        
        if(typeof focusInput == 'undefined') {
            $("select[name=" + key +"]");
        }
        $(error).insertAfter(focusInput);
        // hide all other help classes found
        focusInput.siblings('.help-block:not(.error)').hide();
        focusInput.closest('.form-group').addClass('is-focused has-error');
    }
}

refreshCaptcha = function() {
    captcha = $(".g-recaptcha").detach();
    captcha.prependTo("#captcha")
}

$(document).ready(function() {
    $("form").submit(function(event){
        $(".error").remove();
        $(".has-error is-focused").removeClass(".has-error is-focused");
    })


    $( "#device" ).change(function() {
        var pattern =  JSON.parse($('option:selected', this).attr('pattern'));

        for(second in pattern) {
            checkbox =  $( "#" + second);
            
            if (pattern[second] == 0) {
                checkbox.prop("checked", false);
            }

            else if (pattern[second] == 1) {
                checkbox.prop("checked", true);
            }
            
        }

    });

    $("#pattern-form").submit(function(event){
        var $form = $(this);

        var data = JSON.stringify($form.serializeObject());
        var request = $.ajax({
            url: "/pattern",
            type: "POST",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: data
        })

        request.done(function() {
            showSnackbar();
        })

        request.fail(function(jqXHR, textStatus, errorThrown){
            showErrors(JSON.parse(jqXHR.responseText), 'select')
        })

        return false;
})
})