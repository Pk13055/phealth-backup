/*
    JS file for professional details
 */

$(document).ready(function() {
    // table all-toggle
    $("input#all-toggle").on('click', function() {
        $(this).closest("table").find("tbody input[type='checkbox']").prop({'checked' : true});
    });
});