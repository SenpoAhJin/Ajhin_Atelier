const passwordInput = document.getElementById("password");
const strengthMessage = document.getElementById("strengthMessage");

passwordInput.addEventListener("input", function() {
    const password = passwordInput.value;

    if (password.length < 8) {
        strengthMessage.innerText = "Weak (Minimum 8 characters)";
        strengthMessage.style.color = "red";
    } else if (!/[A-Z]/.test(password) || !/[0-9]/.test(password)) {
        strengthMessage.innerText = "Medium (Add uppercase & number)";
        strengthMessage.style.color = "orange";
    } else {
        strengthMessage.innerText = "Strong Password";
        strengthMessage.style.color = "green";
    }
});

document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;

    const response = await fetch("/api/accounts/register/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password,
            confirm_password: confirm_password
        })
    });

    const data = await response.json();

    if (response.ok) {
        window.location.href = "/";
    } else {
        document.getElementById("error-message").innerText =
            data.password ? data.password : "Registration failed";
    }
});

document.querySelectorAll(".toggle-password").forEach(toggle => {
    toggle.addEventListener("click", function () {
        const inputId = this.getAttribute("data-target");
        const input = document.getElementById(inputId);

        if (input.type === "password") {
            input.type = "text";
            this.textContent = "🙈";
        } else {
            input.type = "password";
            this.textContent = "👁";
        }
    });
});
