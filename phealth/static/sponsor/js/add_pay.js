/*
	JS for discountcard/healthcheckup addition

*/

// Verify if a coupon has been applied or not
var verify_coupon = () => {
        let $form = $("form#coupon_form");
        $form.on('submit', function(e) { e.preventDefault(); });
        $.ajax({
            url: '/common/coupon/',
            method: "POST",
            data: $form.serialize(),
            success: function(response) {
                x = response;
                if (response['status']) {
                    alert("Coupon Applied!");
                    $form.find("input, button").attr('disabled', true);
                }
                else alert("Invalid Coupon!");
            }
        });
    },
    calculate_new = () => {
    	let total = $("table#participants tbody").find("input.add_card:checked"),
    	new_cost = total.length * parseFloat($("th#single_price").text());
    	$("th#multi_price").text(new_cost);
    };

// event listener assignment
$(document).ready(function() {

	// check all or invert selection
	$("input.all_check").on('click', function() {
		$(this).closest("table").find("tbody input.add_card").click();
	}).click();

	// check a row enables inputs
	$("tbody tr td input.add_card").on('click', function() {
		let $id = $(this).closest("tr").find("input.can_id");
		$id.prop('disabled', !$(this).prop('checked'));
		calculate_new();
	});

	// calculate new cost
	calculate_new();
});
