// Common function to handle receipts and messages
function handleResponse(data) {
    if (data.error) {
        showFlashMessage(data.message, 'danger');
    } else {
        showFlashMessage(data.message, 'success');
        document.getElementById('receiptContainer').innerHTML = data.receipt;
    }
}

// Check-in form handler
document.getElementById('checkinForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    
    fetch(CHECKIN_URL, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showFlashMessage(data.message, 'danger');
        } else {
            // Show success message
            showFlashMessage(data.message, 'success');
            
            // Insert the receipt HTML into the receipt container
            const receiptContainer = document.getElementById('receiptContainer');
            receiptContainer.innerHTML = data.receipt;
            
            // Get the receipt element
            const receipt = receiptContainer.querySelector('.receipt-container');
            
            // Wait a bit for the receipt to be rendered
            setTimeout(() => {
                // Trigger print
                printReceipt(receipt.id);
            }, 500);
            
            // Reset the form
            this.reset();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showFlashMessage('An error occurred during check-in', 'danger');
    });
});

// Check-out form handler
document.getElementById('checkoutForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    
    fetch(CHECKOUT_URL, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showFlashMessage(data.message, 'danger');
        } else if (data.needsAdditionalPayment) {
            showPaymentModal(data);
        } else {
            // Show success message
            showFlashMessage(data.message, 'success');
            
            // Insert the receipt HTML into the receipt container
            const receiptContainer = document.getElementById('receiptContainer');
            receiptContainer.innerHTML = data.receipt;
            
            // Get the receipt element
            const receipt = receiptContainer.querySelector('.receipt-container');
            
            // Wait a bit for the receipt to be rendered
            setTimeout(() => {
                // Trigger print
                printReceipt(receipt.id);
            }, 500);
            
            // Reset the form
            this.reset();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showFlashMessage('An error occurred during checkout', 'danger');
    });
});

function showFlashMessage(message, type = 'success') {
    const flashDiv = document.getElementById('flashMessage');
    flashDiv.textContent = message;
    flashDiv.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    flashDiv.style.display = 'block';
    flashDiv.style.zIndex = '1050';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        flashDiv.style.display = 'none';
    }, 5000);
}

// Additional payment form handler
document.getElementById('additionalPaymentForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const paymentMode = document.getElementById('additionalPaymentMode').value;
    if (!paymentMode) {
        showFlashMessage('Please select a payment mode', 'danger');
        return;
    }
    
    const formData = new FormData(this);
    console.log('Submitting additional payment with mode:', paymentMode); // Debug log
    
    fetch(CHECKOUT_URL, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showFlashMessage(data.message, 'danger');
        } else {
            const modal = bootstrap.Modal.getInstance(document.getElementById('paymentModal'));
            if (modal) {
                modal.hide();
            }
            showFlashMessage(data.message, 'success');
            document.getElementById('receiptContainer').innerHTML = data.receipt;
            
            document.getElementById('checkoutForm').reset();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showFlashMessage('An error occurred during checkout', 'danger');
    });
});

function showPaymentModal(data) {
    const modalHtml = `
        <div class="modal fade" id="paymentModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-warning">
                        <h5 class="modal-title">
                            <i class="fas fa-exclamation-triangle"></i> Additional Payment Required
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="payment-details mb-4">
                            <h4>Payment Details:</h4>
                            <p>Vehicle Number: ${data.vehicle_number}</p>
                            <p>Additional Charge: ₹${data.additional_charge}</p>
                            <p>Total Charge: ₹${data.total_charge}</p>
                        </div>
                        <div class="payment-options">
                            <div class="payment-option" data-mode="UPI">
                                <i class="fas fa-mobile-alt"></i>
                                <div>UPI</div>
                            </div>
                            <div class="payment-option" data-mode="Cash">
                                <i class="fas fa-money-bill-wave"></i>
                                <div>Cash</div>
                            </div>
                            <div class="payment-option" data-mode="Card">
                                <i class="fas fa-credit-card"></i>
                                <div>Card</div>
                            </div>
                        </div>
                        <button id="completeCheckoutBtn" class="btn btn-primary mt-3" disabled>
                            Complete Checkout
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('paymentModal'));
    modal.show();
    
    let selectedPaymentMode = null;
    const paymentOptions = document.querySelectorAll('.payment-option');
    
    paymentOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove selected class from all options
            paymentOptions.forEach(opt => opt.classList.remove('selected'));
            // Add selected class to clicked option
            this.classList.add('selected');
            // Store selected payment mode
            selectedPaymentMode = this.dataset.mode;
            // Enable complete checkout button
            document.getElementById('completeCheckoutBtn').disabled = false;
        });
    });
    
    document.getElementById('completeCheckoutBtn').addEventListener('click', function() {
        if (!selectedPaymentMode) {
            showFlashMessage('Please select a payment mode', 'danger');
            return;
        }
        
        const formData = new FormData();
        formData.append('vehicle_number', data.vehicle_number);
        formData.append('payment_mode', selectedPaymentMode);
        formData.append('additional_charge', data.additional_charge);
        formData.append('total_charge', data.total_charge);
        
        fetch(CHECKOUT_URL, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(responseData => {
            if (responseData.error) {
                showFlashMessage(responseData.message, 'danger');
            } else {
                modal.hide();
                showFlashMessage(responseData.message, 'success');
                document.getElementById('receiptContainer').innerHTML = responseData.receipt;
                
                // Wait for receipt to be rendered then print
                setTimeout(() => {
                    const receipt = document.querySelector('.receipt-container');
                    if (receipt) {
                        printReceipt(receipt.id);
                    }
                }, 500);
                
                document.getElementById('checkoutForm').reset();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showFlashMessage('An error occurred during checkout', 'danger');
        });
    });
}

function selectPayment(element, mode, inputId) {
    // Remove selected class from all options in the same group
    element.closest('.payment-options').querySelectorAll('.payment-option').forEach(option => {
        option.classList.remove('selected');
    });
    // Add selected class to clicked option
    element.classList.add('selected');
    // Set the hidden input value
    document.getElementById(inputId).value = mode;
    console.log('Selected payment mode:', mode); // Debug log
}

// Add form submission handler
document.getElementById('checkinForm').addEventListener('submit', function(e) {
    const paymentMode = document.getElementById('checkinPaymentMode').value;
    if (!paymentMode) {
        e.preventDefault();
        alert('Please select a payment mode');
    }
});

// Store the last printed receipt HTML
let lastPrintedReceiptHtml = '';

// Function to handle printing
function printReceipt(receiptId) {
    const receipt = document.getElementById(receiptId);
    if (!receipt) {
        console.error('Receipt not found');
        return;
    }
    
    // Store the receipt HTML for future reprints
    lastPrintedReceiptHtml = receipt.innerHTML;
    
    // Create a new window for printing
    const printWindow = window.open('', '_blank');
    
    // Write the print-optimized content
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Parking Receipt</title>
            <style>
                @page {
                    margin: 0;
                    size: 80mm 140mm;
                }
                body {
                    font-family: 'Courier New', monospace;
                    margin: 0;
                    padding: 20px;
                }
                .receipt {
                    width: 80mm;
                    margin: 0 auto;
                }
                .receipt-header {
                    text-align: center;
                    margin-bottom: 20px;
                }
                .receipt-divider {
                    border-top: 1px dashed #000;
                    margin: 10px 0;
                }
                .receipt-row {
                    display: flex;
                    justify-content: space-between;
                    margin: 5px 0;
                }
                @media print {
                    body {
                        width: 80mm;
                    }
                }
            </style>
        </head>
        <body>
            ${lastPrintedReceiptHtml}
        </body>
        </html>
    `);
    
    // Print and close the window
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
}

// Function to handle reprinting last receipt
function reprintLastReceipt() {
    if (!lastPrintedReceiptHtml) {
        showFlashMessage('No receipt available for reprinting', 'warning');
        return;
    }

    // Create a new window for printing
    const printWindow = window.open('', '_blank');
    
    // Write the print-optimized content with same style as original
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Parking Receipt</title>
            <style>
                @page {
                    margin: 0;
                    size: 80mm 140mm;
                }
                body {
                    font-family: 'Courier New', monospace;
                    margin: 0;
                    padding: 20px;
                }
                .receipt {
                    width: 80mm;
                    margin: 0 auto;
                }
                .receipt-header {
                    text-align: center;
                    margin-bottom: 20px;
                }
                .receipt-divider {
                    border-top: 1px dashed #000;
                    margin: 10px 0;
                }
                .receipt-row {
                    display: flex;
                    justify-content: space-between;
                    margin: 5px 0;
                }
                @media print {
                    body {
                        width: 80mm;
                    }
                }
            </style>
        </head>
        <body>
            ${lastPrintedReceiptHtml}
        </body>
        </html>
    `);
    
    // Print and close the window
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
    
    showFlashMessage('Receipt printed successfully', 'success');
}

// Vehicle suggestions functionality
document.addEventListener('DOMContentLoaded', function() {
    const checkoutInput = document.getElementById('checkoutVehicleNumber');
    const suggestionsDiv = document.getElementById('vehicleSuggestions');
    let currentFocus = -1;
    
    checkoutInput.addEventListener('input', function() {
        const value = this.value.toUpperCase();
        
        if (value.length < 2) {
            suggestionsDiv.style.display = 'none';
            return;
        }
        
        // Fetch suggestions from server
        fetch(`${SUGGESTIONS_URL}?query=${value}`)
            .then(response => response.json())
            .then(data => {
                if (data.suggestions.length > 0) {
                    displaySuggestions(data.suggestions);
                } else {
                    suggestionsDiv.style.display = 'none';
                }
            });
    });
    
    function displaySuggestions(suggestions) {
        suggestionsDiv.innerHTML = '';
        suggestions.forEach(vehicle => {
            const div = document.createElement('div');
            div.innerHTML = `<i class="fas fa-motorcycle"></i> ${vehicle}`;
            div.className = 'suggestion-item';
            div.addEventListener('click', function() {
                checkoutInput.value = this.textContent.trim();
                suggestionsDiv.style.display = 'none';
            });
            suggestionsDiv.appendChild(div);
        });
        suggestionsDiv.style.display = 'block';
    }
});