$(function() {
  $('.toggle').on('click', function() {

    var card = $(this).parent('.card');
    var isMaximizing = card.hasClass('card-small');
    var animationDelay = 500; // in ms

    /**
      Ordering of animations is different depending on if we maximize or minimize a card
    **/
    if(isMaximizing) {
      card.toggleClass('top');
      $('.card').toggleClass('center');
      // Wait for cards to center, then maximize
      setTimeout(function() {
        card.toggleClass('card-small card-large');
      }, animationDelay);
    } else {
      card.toggleClass('card-small card-large');
      // Wait until card has minized, then re-position cards
      setTimeout(function() {
        $('.card').toggleClass('center');

        // Reset z-index after cards are in their rightful place
        setTimeout(function() {
          card.toggleClass('top');
        }, animationDelay);
      }, animationDelay);
    }

     $(this).toggleClass('glyphicon-resize-full glyphicon-resize-small');
  });
});