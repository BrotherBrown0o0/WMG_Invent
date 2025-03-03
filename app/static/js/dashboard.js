// Dashboard charts and functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize any additional charts if they exist
    if (document.getElementById('salesChart')) {
        initSalesChart();
    }
});

function initSalesChart() {
    const ctx = document.getElementById('salesChart').getContext('2d');
    
    // Sample data - in a real app, this would come from the server
    const salesData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Sales',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            borderColor: 'rgba(59, 130, 246, 1)',
            borderWidth: 1
        }]
    };
    
    // Create the chart
    new Chart(ctx, {
        type: 'bar',
        data: salesData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Function to handle product filtering
function filterProducts() {
    const searchInput = document.getElementById('productSearch');
    const filter = searchInput.value.toUpperCase();
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        const title = card.querySelector('.product-title').textContent;
        if (title.toUpperCase().indexOf(filter) > -1) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

// Function to handle order status updates
function updateOrderStatus(orderId, status) {
    // In a real app, this would make an AJAX request to update the status
    console.log(`Updating order ${orderId} to status: ${status}`);
    
    // For demo purposes, update the UI directly
    const statusElement = document.querySelector(`#order-${orderId} .status`);
    if (statusElement) {
        statusElement.textContent = status;
        statusElement.className = `status ${status.toLowerCase()}`;
    }
} 