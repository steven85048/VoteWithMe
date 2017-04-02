Stripe.setPublishableKey('pk_test_V9HjGk9iflRClWokNziS75G0');

Stripe.card.createToken({
  number: document.getElementById('ccnumber').value,
  exp_month: document.getElementById('expmonth').value,
  exp_year: document.getElementById('expyear').value,
  cvc: document.getElementById('cvc').value,
  address_zip: document.getElementById('zip').value
}, 1, stripeResponseHandler);

function stripeResponseHandler(status, response) {

  // Grab the form:

  if (response.error) { // Problem!
		console.log(response.error);
  } else { // Token was created!

	// Get the token ID:
	var token = response.id;

	console.log(JSON.stringify(response));

  }
}
