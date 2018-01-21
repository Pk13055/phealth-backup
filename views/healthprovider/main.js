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
$(document).ready(function() {

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

        }); // END document.ready
