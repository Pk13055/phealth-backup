$(document).ready(function(){
	$('.flight-line-b').click(function(){
	  if ( $(this).is('.open') ) {
		$(this).removeClass('open');
		$(this).closest('.appointment_main_hero').find('.alt-details').slideUp();  
	  } else {
		$(this).addClass('open');
		$(this).closest('.appointment_main_hero').find('.alt-details').slideDown();  
	  }
	});
    $("#timeslots").click(function(){
        $(".timeslots").show();
        $(".doctorinfo").hide();
    });
    $("#doctorinfo").click(function(){
        $(".doctorinfo").show();
        $(".timeslots").hide();
    });
});


/*
$(document).ready(function(){
	$('.appointment_main_hero2 .flight-line-b2 b').click(function(){
	  if ( $(this).is('.open') ) {
		$(this).removeClass('open');
		$(this).closest('.appointment_main_hero2').find('.alt-details2').slideUp();  
	  } else {
		$(this).addClass('open');
		$(this).closest('.appointment_main_hero2').find('.alt-details2').slideDown();  
	  }
	});
});
*/

