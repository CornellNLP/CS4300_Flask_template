$(document).ready(function() {

  $("#resort-recommendations").on("submit", function () {

    var valid = true;

    if( $("#location").prop("validity").valid ) {
      $("#locationError").addClass("hidden");
    } else {
      $("#locationError").removeClass("hidden");
      valid = false;
    }

    if( $("#distance").prop("validity").valid ) {
      $("#distanceError").addClass("hidden");
    } else {
      $("#distanceError").removeClass("hidden");
      valid = false;
    }

    if( $("#description").prop("validity").valid ) {
      $("#descriptionError").addClass("hidden");
    } else {
      $("#descriptionError").removeClass("hidden");
      valid = false;
    }

    return valid;

  });

});
