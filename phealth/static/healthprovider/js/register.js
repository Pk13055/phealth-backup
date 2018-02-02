/* PAGE SPECIFIC JS */

$("#find_btn").click(function() { //user clicks button
    if ("geolocation" in navigator) { //check geolocation available
        //try to get user current location using getCurrentPosition() method
        navigator.geolocation.getCurrentPosition(function(position) {
            $("#latitude").val(position.coords.latitude);
            $("#longitude").val(position.coords.longitude);
        });
    } else {
        console.log("Browser doesn't support geolocation!");
    }
});

// Specific Section wise features
let specificUI = () => {

    console.log("specific UI trigger");

    // group button functionality section PLANS
    $("section.plans div.package_groups").hide();
    $("section.plans div.group_toggles button")
        .on('click', function() {
            let toggle = $(this).attr('section');
            $("section.plans div.package_groups").hide();
            $("div.group-" + toggle).fadeIn();
        });


    // send OTP section
    $("section.instant_registration button.validate_current").on('click', () => {
        let credentials = $("section.instant_registration")
        .find("input#mobile, input#email").get()
        .map((e) => { return $(e).val(); });
        console.log(credentials);
        if(!$("section.instant_registration").find(":invalid").length)
            sendOTP(credentials[0], credentials[1]);
    });

    // validate whether the correct OTP was sent or not
    $("section.otp").find("input").on('input', function() {
        let otp_val = $("section.otp").find("input").val(),
        cook_otp = document.cookie.split(";").map((e) => {
                return (e.split("=")[0] == " otp")? e.split("=")[1] : null;
            }).filter((e) => { return e; })[0];
        $(this)[0].setCustomValidity((otp_val !== cook_otp)? "OTPs don't match!" : "");
    });
};

$(document).ready(function() {

    specificUI();
    $("form").on('submit', function(e) { e.preventDefault(); });


    // Basic usage
    $(".placepicker").placepicker();

    // Advanced usage
    $("#advanced-placepicker").each(function() {
        var target = this;
        var $collapse = $(this).parents('.form-group').next('.collapse');
        var $map = $collapse.find('.another-map-class');

        var placepicker = $(this).placepicker({
            map: $map.get(0),
            placeChanged: function(place) {
                console.log("place changed: ", place.formatted_address, this.getLocation());
            }
        }).data('placepicker');
    });


});
