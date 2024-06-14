$(document).ready(function() {

    var csrf_token = $("input[name='csrfmiddlewaretoken']").val()
    var isLog = $("#checkIsLog").text()
    $("#checkIsLog").hide()

    console.log("isLog: " + isLog)

    if (isLog.length > 0) {
        $("#login-div").hide()
        $("#logout-div").show()
    } else {
        $("#login-div").show()
        $("#logout-div").hide()
    }

    $(".logout-button").click(function() {
        $.ajax({
            url: "/account/logout/",
            type: "get",
            data: {
                
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function(response) {
                console.log("logout successfully, response =", response)
                if (response.message == "success") {
                    $("#login-div").show()
                    $("#logout-div").hide()
                    $("#id_password").val("")
                    $("#id_username").val("")
                    $("#login-error-msg").val("")
                    $("#logout-error-msg").val("")
                    updateCSRFToken()
                }
            }
        })
    })

    $(".login-button").on("click", function() {
        var formData = $("#login-form").serialize()

        $.ajax({
            url: "/account/",
            type: "post",
            data: formData,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function(response) {
                if (response.message == "success") {
                    console.log("login successfully")
                    $("#login-div").hide()
                    $("#logout-div").show()
                    $("#id_password").val("")
                    $("#id_username").val("")
                    fetchUserName()
                    $("#login-error-msg").val("")
                    $("#logout-error-msg").val("")
                    updateCSRFToken()
                }
            },
            error: function(xhr, status, error) {
                var errorMessage = "An error occured, try later please";
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                $("#login-error-msg").html(errorMessage);
            }
        })
    })

    function fetchUserName() {
        $.ajax({
            url: '/account/getUsername',
            type: 'get',
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function(data) {
                $('#log-as').text("Logged as " + data.username);
                updateCSRFToken()
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

    function updateCSRFToken() {
        $.ajax({
            url: "/account/updateCRSFToken",
            type: "get",
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function(response) {
                if (response.newToken) {
                    csrf_token = response.newToken
                    console.log("new token ->" + csrf_token)
                } else {
                    console.log("@@@ no new token")
                }
            },
            error: function(error) {
                console.log(error);
            }
        })
    }


})