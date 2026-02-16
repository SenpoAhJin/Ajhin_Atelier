document.addEventListener("DOMContentLoaded", loadOrders);

async function loadOrders() {
    const token = localStorage.getItem("access");

    if (!token) {
        window.location.href = "/login/";
        return;
    }

    const response = await fetch("/api/orders/my-orders/", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    if (response.status === 401) {
        logout();
        return;
    }

    const data = await response.json();
    renderOrders(data);
}

function renderOrders(orders) {
    const container = document.getElementById("orders-container");
    container.innerHTML = "";

    if (!orders.length) {
        container.innerHTML = "<p>No orders yet.</p>";
        return;
    }

    orders.forEach(order => {
        container.innerHTML += `
            <div class="card" style="margin-bottom:20px;">
                <h3>Order #${order.id}</h3>
                <p>Status: ${order.status}</p>
                <p>Total: ₱${order.total_price}</p>
                <p>Date: ${new Date(order.created_at).toLocaleString()}</p>
            </div>
        `;
    });
}

function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    window.location.href = "/login/";
}

function goToDashboard() {
    window.location.href = "/";
}

function goToCart() {
    window.location.href = "/cart/";
}
