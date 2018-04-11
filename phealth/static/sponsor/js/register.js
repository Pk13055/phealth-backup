/* PAGE SPECIFIC JS */

// send the otp to the user and move to next step
let sendOTP = (email, mobile, csrf_token) => {
    $.ajax({
        'url' : "/common/otp",
        'method' : "POST",
        'headers' : {
            'X-CSRFToken' : csrf_token
        },
        'data' : {
            'email' : email,
            'mobile' : mobile
        },
        'success' : function(response) {
            console.log(response);
            alert(response['status']);
        }
    });
};


$(document).ready(function() {

    // trigger OTP on generateOTP click
    $("button#otp_send").on('click', () => {
        let mobile = $("input[name='mobile']").val(),
        email = $("input[name='email']").val(),
        csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        if(email != "" && mobile != "") sendOTP(email, mobile, csrf_token);
    });
});
