/* CROSS PAGE REUSABLE */

// previous next buttons to be appended
var navButtons = (sections) => {
    let $row = $("<div>", { 'class': "row center-block" }),
        icons = {
            'previous_section': $("<i>", { 'class': "fa fa-lg fa-chevron-left" }),
            'next_section': $("<i>", { 'class': "fa fa-lg fa-chevron-right" })
        };
    ["previous_section", "next_section"].forEach(function(ele) {
        if (sections[ele])
            $row.append($("<div>", {
                'class': "col-xs-12 col-md-6 text-center"
            }).append($("<button>", {
                'class': "btn btn-default btn-block nav-btns " + ((ele == "next_section") ? "validate_current" : ""),
                'type': "button",
            }).on('click', function() {
                let status = true;
                // validate current before moving onto the next
                if (ele == "next_section") status = validateCurrent(sections.current_section);
                if (status) {
                    $("section." + sections.current_section).hide();
                    $("section." + sections[ele]).fadeIn();
                }
            }).append(
                icons[ele],
                "  " + sections[ele]
            )));
    });
    return $row;
};



// send the otp to the user and move to next step
let sendOTP = (number, email) => {
    let csrf_token = getCSRF();
    $.ajax({
        'url' : "/auth/otp/",
        'method' : "POST",
        'headers' : {
            'X-CSRFToken' : csrf_token
        },
        'data' : {
            'email' : email,
            'mobile' : number
        },
        'success' : function(response) {
            console.log(response);
        }
    });

};

// function to validate current inputs
// and perform any other tasks
var validateCurrent = (section, custom_validation = null) => {
    console.log("Validating " + section);
    if($("section." + section).find(":invalid").length) {
        // trigger the submission
        // will not work due to invalid fields being present on the page
        $("button#submitBtn").click();
        return false;
    }
    return (custom_validation)? true && custom_validation() : true;
};

// the function wrapping the ajax for the overall registration
var register = (section, btn) => {
    console.log("Submit form for approval");
    let csrf_token = getCSRF();
    if($(document).find("form")[0].checkValidity()) {
        $(btn)[0].setCustomValidity("");
        $.ajax({
            url: window.location.pathname,
            method: "POST",
            headers: {
                'X-CSRFToken' : csrf_token
            },
            processData: false,
            contentType: false,
            data: new FormData($(document).find("form")[0]),
            success: function(response) {
                console.log(response);
            }
        });
    }
    else $(btn)[0].setCustomValidity("Check last section!");
};

// add submit button to final section
var addSubmit = (final_section) => {
    let $btn = $("<button>", {
            'type': "submit",
            'class': "btn btn-block btn-danger",
            'id': "submitBtn"
        }).text("Register")
        .on('click', function() { register(final_section, this); });
    $("section." + final_section).append($("<div>", {
        'class': "row"
    }).append($("<hr>"), $btn));
};

// iterate over sections fitting the data params
// and adding the previous next buttons
var sectionNav = (sections) => {
    $("section").each(function(idx) {
        current_sections = { current_section: sections[idx] };
        $(this).addClass(current_sections.current_section);
        if (idx > 0) current_sections.previous_section = sections[idx - 1];
        if (idx < sections.length)  current_sections.next_section = sections[idx + 1];
        $(this).attr(current_sections);
        $(this).append(navButtons(current_sections));
        if (idx) $(this).hide();
    });
}


$(document).ready(function() {
    $(document).find("form").on('submit', function(e) { e.preventDefault(); });
});
