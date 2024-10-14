let grandTotal = 0;

function calculateTotalPrice(quantityInput) {
    const quantity = quantityInput.value;
    const price = quantityInput.dataset.price;
    const totalPriceElement = quantityInput.closest('tr').querySelector('.total-price');

    // Calculate the new total price
    // Adjust to 2 decimal places
    const itemTotalPrice = (quantity * price).toFixed(2);
    // Update the displayed total price
    totalPriceElement.innerText = `£${itemTotalPrice}`; 

    // Call to update grand total
    calculateGrandTotal(); 
}

function calculateGrandTotal() {
    // Reset grand total
    grandTotal = 0; 

    document.querySelectorAll('.total-price').forEach(element => {
        // Remove the currency symbol
        const priceText = element.innerText.replace('£', ''); 
        // Convert to number and add to grand total
        grandTotal += parseFloat(priceText); 
    });

    // Update the grand total displayed in the basket
    document.getElementById('grand-total').innerText = `£${grandTotal.toFixed(2)}`; 
}

function updatePrice(event, form) {
    // Prevent the default form submission
    event.preventDefault();
    // Get the quantity input
    const quantityInput = form.querySelector('input[name="quantity"]');
    // Calculate the price based on quantity
    calculateTotalPrice(quantityInput); 
    form.submit(); 
}
