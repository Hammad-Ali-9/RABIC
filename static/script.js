document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value; // Assuming email is also needed for submission
        const password = document.getElementById("pwd").value;

        // Collect error messages
        let errorMessages = [];

        if (!validateUsername(username)) {
            errorMessages.push("Username must be between 8 and 20 characters.");
        }

        if (!validatePassword(password)) {
            errorMessages.push("Password must be at least 8 characters long, contain one uppercase letter, and one special character.");
        }

        // If there are any error messages, show a single alert and stop the form submission
        if (errorMessages.length > 0) {
            alert(errorMessages.join("\n")); // Display all errors in a single alert
            return;
        }

        // If all validations pass, submit the form
        form.submit();
    });

    function validateUsername(username) {
        return username.length >= 8 && username.length <= 20;
    }

    function validatePassword(password) {
        const hasUppercase = /[A-Z]/.test(password);
        const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        const hasMinLength = password.length >= 8;

        return hasUppercase && hasSpecialChar && hasMinLength;
    }
});
