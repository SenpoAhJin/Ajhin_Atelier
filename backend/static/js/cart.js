document.addEventListener("DOMContentLoaded", loadCart);

async function loadCart() {
    const token = localStorage.getItem("access");

    if (!token) {
        window.location.href = "/login/";
        return;
    }

    const response = await fetch("/api/orders/cart/", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    if (response.status === 401) {
        logout();
        return;
    }

    const data = await response.json();
    renderCart(data.items || []);
}

function renderCart(items) {
    const container = document.getElementById("cart-items");
    const summary = document.getElementById("cart-summary");

    container.innerHTML = "";
    let total = 0;

    if (!items.length) {
        container.innerHTML = "<p>Your cart is empty.</p>";
        summary.innerHTML = "";
        return;
    }

    items.forEach(item => {
        total += item.product_price * item.quantity;

        container.innerHTML += `
            <div class="card" style="margin-bottom:15px;">
                <h3>${item.product_name}</h3>
                <p>Price: ₱${item.product_price}</p>
                <p>Quantity: ${item.quantity}</p>
                <button onclick="removeItem(${item.id})">
                    Remove
                </button>
            </div>
        `;
    });

    summary.innerHTML = `
        <h2>Total: ₱${total.toFixed(2)}</h2>
        <button onclick="checkout()">Proceed to Checkout</button>
    `;
}

async function removeItem(itemId) {
    const token = localStorage.getItem("access");

    await fetch(`/api/orders/cart/remove/${itemId}/`, {
        method: "DELETE",
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    loadCart();
}

async function checkout() {
    const token = localStorage.getItem("access");
    const address = prompt("Enter shipping address:");

    if (!address) return;

    const response = await fetch("/api/orders/checkout/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            shipping_address: address
        })
    });

    if (response.ok) {
        alert("Order placed!");
        loadCart();
    }
}

function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    window.location.href = "/login/";
}

function goToDashboard() {
    window.location.href = "/";
}

function goToOrders() {
    window.location.href = "/orders/";
}
