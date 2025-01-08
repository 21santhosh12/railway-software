// Password toggle functionality
document.getElementById('togglePassword').addEventListener('click', function() {
    const passwordInput = document.getElementById('userPassword');
    const icon = this.querySelector('i');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
});

// Delete user functionality
function handleDelete(event, form) {
    event.preventDefault();
    
    if (!confirm('Are you sure you want to delete this user?')) {
        return false;
    }
    
    const feedbackDiv = document.getElementById('feedback');
    
    fetch(form.action, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Remove the row from the table
            const row = form.closest('tr');
            if (row) {
                row.remove();
                
                // Show success message
                if (feedbackDiv) {
                    feedbackDiv.className = 'alert alert-success mt-3';
                    feedbackDiv.innerHTML = '<i class="fas fa-check-circle"></i> ' + data.message;
                    feedbackDiv.style.display = 'block';
                    
                    // Hide feedback after 5 seconds
                    setTimeout(() => {
                        feedbackDiv.style.display = 'none';
                    }, 5000);
                }
            }
        } else {
            throw new Error(data.message || 'Failed to delete user');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (feedbackDiv) {
            feedbackDiv.className = 'alert alert-danger mt-3';
            feedbackDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i> ' + error.message;
            feedbackDiv.style.display = 'block';
            
            // Hide feedback after 5 seconds
            setTimeout(() => {
                feedbackDiv.style.display = 'none';
            }, 5000);
        }
    });
    
    return false;
}

// Create user form handling
document.getElementById('createUserForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const feedbackDiv = document.getElementById('feedback');
    const tbody = document.querySelector('.custom-table tbody');
    
    fetch(CREATE_USER_URL, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text().then(text => {
            try {
                return JSON.parse(text);
            } catch (e) {
                console.error('Failed to parse response:', text);
                throw new Error('Invalid response from server');
            }
        });
    })
    .then(data => {
        if (data.success) {
            const createdAt = new Date().toLocaleString();
            const createdBy = CURRENT_USER;
            const newRow = document.createElement('tr');
            
            if (!data.user || !data.user.rate) {
                throw new Error('Invalid user data received');
            }
            
            newRow.innerHTML = `
                <td>${data.user.username}</td>
                <td>${createdAt}</td>
                <td>${createdBy}</td>
                <td>₹${data.user.rate.initial_amount}</td>
                <td>${data.user.rate.initial_duration} hours</td>
                <td>₹${data.user.rate.extra_charge}</td>
                <td>${data.user.rate.extra_charge_duration} hours</td>
                <td>
                    <form action="/route_delete_user/${data.user.username}" 
                          method="POST" 
                          class="delete-user-form" 
                          style="display: inline;"
                          onsubmit="return handleDelete(event, this)">
                        <button type="submit" class="btn btn-custom btn-custom-danger">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </form>
                </td>
            `;
            tbody.insertBefore(newRow, tbody.firstChild);
            
            // Show success message
            feedbackDiv.className = 'alert alert-success mt-3';
            feedbackDiv.innerHTML = '<i class="fas fa-check-circle"></i> ' + data.message;
            feedbackDiv.style.display = 'block';
            
            // Reset form
            this.reset();
        } else {
            throw new Error(data.message || 'Failed to create user');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        feedbackDiv.className = 'alert alert-danger mt-3';
        feedbackDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i> ' + error.message;
        feedbackDiv.style.display = 'block';
    });
    
    // Hide feedback after 5 seconds
    setTimeout(() => {
        feedbackDiv.style.display = 'none';
    }, 5000);
}); 