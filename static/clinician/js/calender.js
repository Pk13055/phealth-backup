/*
	JS for the clinician calender page
*/

let updateSection = (section) => {
	console.log("Submitting " + section);
	let $form = $("section#" + section).find("form");
	let form_data = new FormData($form[0]),
	csrf_token = document.cookie.split(";")
    .map((e) => {
        return (e.split("=")[0] == "csrftoken")? e.split("=")[1] : null;
    }).filter((e) => { return e; })[0];
	$.ajax({
		url: window.location.pathname,
		method: "POST",
		processData: false,
    	contentType: false,
		headers: {
			'X-CSRFToken': csrf_token
		},
		data: form_data,
		success: function(response) {
			console.log(response);
		}
	});
};

let calenderUI = () => {

	// add event listener on the update button
	$("button.update_section").on('click', function() {
		updateSection($(this).attr('current_section'));
	});

	// add a check all function to the same
	$("table thead tr th input[type='checkbox']").on('click', function() {
		$(this).closest("table").find("tbody :checkbox").click();
	}).click();

	// add disable option
	$("table tbody").on('click', ':checkbox', function() {
		$(this).closest("tr").find("input[type='time'], input[type='date']").prop({
			'disabled' : !this.checked,
			'required' : this.checked
		});
	});

	// add the option to add more rows on clicking +
	$("table tbody tr td").on('click', "button.add_rows", function() {
		let $row = $(this).closest("tr").clone(true, true),
		$btn = $row.find("td button.add_rows");
		$btn.parent().addClass("text-danger");
		$btn.remove();
		$(this).closest("tr").after($row);
	});

	// delete the given vacation rows
	$("table tbody tr td").on('click', "button.delete_rows", function() {
		$(this).closest("tr").remove();
	});

	// add a vacation row
	$("button.add_vacation").on('click', function() {
		// clone true for event binding preserve
		let $ref = $(this).closest("section").find("table tbody"),
			$row = $($ref.find("tr")[0]).clone(true, true);
		$row.find("input[type='date']").attr({
			'name' : "timings[]"
		}).val("");
		$ref.append($row);
	});
};

$(document).ready(function() {
	// disable default behaviour for forms
	$("form").on('submit', function(e) { e.preventDefault(); })
	// all the page calender functions
	calenderUI();
});
