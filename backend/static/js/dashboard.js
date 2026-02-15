document.addEventListener("DOMContentLoaded", () => {

    const token = localStorage.getItem("access");

    if (!token) {
        window.location.href = "/login/";
        return;
    }

    loadMarketplace(token);
});

async function loadMarketplace(token) {
    try {
        const response = await fetch("/api/marketplace/", {
            headers: {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json"
            }
        });

        if (response.status === 401) {
            logout();
            return;
        }

        const data = await response.json();
        renderProducts(data);

    } catch (error) {
        console.error("Error:", error);
    }
}

function renderProducts(products) {
    const grid = document.getElementById("products-grid");
    grid.innerHTML = "";

    if (!products.length) {
        grid.innerHTML = "<p class='text-gray-400'>No items available.</p>";
        return;
    }

    products.forEach(product => {
        grid.innerHTML += `
        <article class="product-card group">
            <div class="glow-border bg-gray-800/80 backdrop-blur-sm rounded-2xl overflow-hidden border border-gray-700/50">
                <div class="relative h-48 bg-gradient-to-br from-purple-500 to-cyan-500"></div>

                <div class="p-5">
                    <span class="inline-block px-3 py-1 text-xs font-medium bg-purple-500/20 text-purple-400 rounded-full mb-3">
                        ${product.category_name || "General"}
                    </span>

                    <h3 class="text-lg font-semibold text-white mb-2">
                        ${product.title || product.name}
                    </h3>

                    <div class="flex items-center justify-between">
                        <span class="text-2xl font-bold text-purple-400">
                            ₱${product.price}
                        </span>

                        <button class="px-5 py-2 bg-gray-700 hover:bg-purple-500 rounded-xl text-white transition-all">
                            View Details
                        </button>
                    </div>
                </div>
            </div>
        </article>
        `;
    });
}

function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    window.location.href = "/login/";
}
