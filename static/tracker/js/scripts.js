
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all maps on the page
    initMaps();

    // Add click event listeners for analytics
    setupAnalytics();

    // Handle any forms with custom JavaScript
    setupForms();
});

function initMaps() {
    if (typeof L === 'undefined') {
        console.error('Leaflet.js not loaded. Maps cannot be initialized.');
        return;
    }

    document.querySelectorAll('.map-container').forEach(container => {
        const mapId = container.id;
        const lat = parseFloat(container.dataset.lat);
        const lon = parseFloat(container.dataset.lon);
        const popupContent = container.dataset.popup || 'Location';

        if (!isNaN(lat) && !isNaN(lon)) {
            const map = L.map(mapId).setView([lat, lon], 13);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            L.marker([lat, lon]).addTo(map)
                .bindPopup(popupContent);
        }
    });
}

function setupAnalytics() {
    document.querySelectorAll('a[href^="/view/p/"]').forEach(link => {
        link.addEventListener('click', function(e) {
            console.log('Tracker link clicked:', this.href);
        });
    });

    document.querySelectorAll('a[href$="/download/"]').forEach(link => {
        link.addEventListener('click', function(e) {
            console.log('PDF download initiated:', this.href);
        });
    });
}

function setupForms() {
    const urlForm = document.querySelector('form[method="post"]');
    if (urlForm) {
        const urlInput = urlForm.querySelector('input[type="url"]');

        urlInput.addEventListener('input', function() {
            if (this.value.includes('instagram.com')) {
                this.setCustomValidity('');
            } else {
                this.setCustomValidity('Please enter a valid Instagram URL');
            }
        });

        urlForm.addEventListener('submit', function(e) {
            console.log('Form submitted with URL:', urlInput.value);
        });
    }
}

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initMaps,
        setupAnalytics,
        setupForms,
        showToast
    };
}
