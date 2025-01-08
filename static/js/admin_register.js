// Password toggle functionality
document.getElementById('togglePassword')?.addEventListener('click', function() {
    const passwordInput = document.getElementById('password');
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

// Password strength checker
function checkPasswordStrength(password) {
    let strength = 0;
    
    // Length check
    if (password.length >= 8) strength++;
    
    // Contains number
    if (/\d/.test(password)) strength++;
    
    // Contains letter
    if (/[a-zA-Z]/.test(password)) strength++;
    
    // Contains special character
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++;
    
    return strength;
}

// Update password strength indicator
document.getElementById('password')?.addEventListener('input', function() {
    const strength = checkPasswordStrength(this.value);
    const indicator = document.getElementById('passwordStrength');
    
    // Remove all classes
    indicator.classList.remove('strength-weak', 'strength-medium', 'strength-strong');
    
    if (this.value.length === 0) {
        indicator.style.display = 'none';
    } else {
        indicator.style.display = 'block';
        if (strength <= 2) {
            indicator.classList.add('strength-weak');
        } else if (strength === 3) {
            indicator.classList.add('strength-medium');
        } else {
            indicator.classList.add('strength-strong');
        }
    }
});

// Form validation
document.getElementById('adminRegisterForm')?.addEventListener('submit', function(e) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    let isValid = true;
    
    // Reset previous error states
    document.querySelectorAll('.is-invalid').forEach(el => {
        el.classList.remove('is-invalid');
    });
    
    // Username validation
    if (!username.trim()) {
        document.getElementById('username').classList.add('is-invalid');
        isValid = false;
    }
    
    // Password validation
    if (!password.trim()) {
        document.getElementById('password').classList.add('is-invalid');
        isValid = false;
    } else if (checkPasswordStrength(password) < 3) {
        document.getElementById('password').classList.add('is-invalid');
        document.getElementById('passwordFeedback').textContent = 'Password is too weak';
        isValid = false;
    }
    
    // Confirm password validation
    if (password !== confirmPassword) {
        document.getElementById('confirmPassword').classList.add('is-invalid');
        document.getElementById('confirmPasswordFeedback').textContent = 'Passwords do not match';
        isValid = false;
    }
    
    if (!isValid) {
        e.preventDefault();
    }
});

// OTP form validation
document.getElementById('otpVerificationForm')?.addEventListener('submit', function(e) {
    const otp = document.getElementById('otp').value;
    let isValid = true;
    
    // Reset previous error states
    document.querySelectorAll('.is-invalid').forEach(el => {
        el.classList.remove('is-invalid');
    });
    
    // OTP validation
    if (!otp.trim() || otp.length !== 6 || !/^\d+$/.test(otp)) {
        document.getElementById('otp').classList.add('is-invalid');
        isValid = false;
    }
    
    if (!isValid) {
        e.preventDefault();
    }
});

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });
}); 