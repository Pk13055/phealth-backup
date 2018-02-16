/*
	JS code for the discounts addition and tick inputs

*/

$(document).ready(function() {


	// add disabling function to the tick buttons
	$("table tbody tr td").on('click', "input.enabler", function() {
		$(this).closest("tr").find("td.form-eles").find("input, select, button").prop({
			'disabled' : !this.checked,
			'required' : this.checked
		});
	});

	// add tick all event listener
	$("table thead tr th").on('click', "input[type='checkbox']", function() {
		$(this).closest("table").find("tbody")
		.find("input.enabler").click();
	});
	$("table thead tr th input").click()

});
