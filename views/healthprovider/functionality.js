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

// function to validate current inputs
// and perform any other tasks
var validateCurrent = (section) => {
    console.log("Validating " + section);
    return true;
};

// the function wrapping the ajax for the overall registration
var register = () => {
    console.log("Submit form for approval");
    /*$.ajax({
        url: "#",
        method: "POST",
        data: {

        },
        success: function(response) {

        }
    });*/
};

// add submit button to final section
var addSubmit = (final_section) => {
    let $btn = $("<button>", {
            'type': "button",
            'class': "btn btn-block btn-danger",
            'id': "submitBtn"
        }).text("Register")
        .on('click', register);
    $("section." + final_section).append($("<div>", {
        'class': "row"
    }).append($("<hr>"), $btn));
};

// iterate over sections fitting the data params
// and adding the previous next buttons
var sectionNav = (sections) => {
    $("section").each(function(idx) {
        $(this).addClass(sections[idx]);
        $(this).attr({ 'current-section': sections[idx] });
        current_sections = { current_section: sections[idx] };
        if (idx > 0) {
            $(this).attr('previous-section', sections[idx - 1]);
            current_sections.previous_section = sections[idx - 1];
        }
        if (idx < sections.length) {
            $(this).attr('next-section', sections[idx + 1]);
            current_sections.next_section = sections[idx + 1];
        }
        $(this).append(navButtons(current_sections));
        if (idx) $(this).hide();
    });
}
