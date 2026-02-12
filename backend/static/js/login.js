document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/token/", {
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
        window.location.href = "/api/marketplace/";
    } else {
        document.getElementById("error-message").innerText = "Invalid credentials";
    }
});
