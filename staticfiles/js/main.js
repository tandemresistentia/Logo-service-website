var stripe = Stripe('pk_test_51Mbox2IQDkGdDbUYvfjf4ItvBDZI4ZMA5Ic6XJnytAEZG1mwkR7J0Jc1Zo2xpDMBX4FqKi1aANHsQa8eFgRbpldt00JYckHaYg');

// Gets all buy buttons
var buttons = document.getElementsByClassName('buy-button');
for (i = 0; i < buttons.length; i++) {

  // for every button we will add a Stripe POST request action
  buttons[i].addEventListener('click', function(event) {
    var targetElement = event.target || event.srcElement;
    var productName =  targetElement.value;
    console.log('Buying: ' + productName);

    // Our endpoint with the chosen product name
    var url = '/create-checkout-session/' + productName

    // Create a new Checkout Session
    fetch(url, {
      method: 'POST',
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(session) {
      return stripe.redirectToCheckout({ sessionId: session.id });
    })
    .then(function(result) {
      // If `redirectToCheckout` fails due to a browser or network
      // error, you should display the localized error message to your
      // customer using `error.message`.
      if (result.error) {
        alert(result.error.message);
      }
    })
    .catch(function(error) {
      console.error('Error:', error);
    });

  });

}