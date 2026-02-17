document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("access");

    if (!token) return;

    try {
        const response = await fetch("/api/accounts/me/", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        if (response.ok) {
            // Token valid → go to dashboard
            window.location.href = "/dashboard/";
        } else {
            // Token invalid/expired → clear it
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
        }

    } catch (error) {
        console.error("Token validation failed");
    }
});



document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/accounts/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        window.location.href = "/dashboard/";

    } else {
        document.getElementById("error-message").innerText = "Invalid credentials";
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
