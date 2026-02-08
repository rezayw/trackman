/**
 * Trackman - Instagram Link Tracker
 * Main JavaScript file
 */

document.addEventListener('DOMContentLoaded', function() {
    initMaps();
    setupForms();
    setupCopyButtons();
});

/**
 * Initialize Leaflet maps on the page
 */
function initMaps() {
    if (typeof L === 'undefined') {
        console.warn('Leaflet.js not loaded. Maps cannot be initialized.');
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
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            }).addTo(map);

            L.marker([lat, lon])
                .addTo(map)
                .bindPopup(popupContent)
                .openPopup();

            // Fix map rendering issues in hidden containers
            setTimeout(() => {
                map.invalidateSize();
            }, 100);
        }
    });
}

/**
 * Setup form validation and enhancements
 */
function setupForms() {
    const urlForm = document.querySelector('form[method="post"]');
    if (!urlForm) return;

    const urlInput = urlForm.querySelector('input[type="url"]');
    if (!urlInput) return;

    urlForm.addEventListener('submit', function(e) {
        const url = urlInput.value.trim();
        
        // Basic Instagram URL validation
        if (!url.includes('instagram.com')) {
            e.preventDefault();
            showToast('Please enter a valid Instagram URL', 'error');
            urlInput.focus();
            return;
        }

        // Show loading state
        const submitBtn = urlForm.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
            submitBtn.disabled = true;
        }
    });

    // Clear custom validity on input
    urlInput.addEventListener('input', function() {
        this.setCustomValidity('');
    });
}

/**
 * Setup copy button functionality
 */
function setupCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const textToCopy = this.dataset.copy || 
                              this.previousElementSibling?.value ||
                              this.previousElementSibling?.textContent;
            
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy.trim())
                    .then(() => showToast('Copied to clipboard!', 'success'))
                    .catch(() => showToast('Failed to copy', 'error'));
            }
        });
    });
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => showToast('Link copied to clipboard!', 'success'))
        .catch(() => showToast('Failed to copy link', 'error'));
}

/**
 * Display a toast notification
 * @param {string} message - Message to display
 * @param {string} type - Type of toast ('success' or 'error')
 */
function showToast(message, type = 'success') {
    // Remove existing toasts
    document.querySelectorAll('.toast').forEach(t => t.remove());

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icon = type === 'success' ? 'check-circle' : 'exclamation-circle';
    toast.innerHTML = `<i class="fas fa-${icon}"></i> ${message}`;
    
    document.body.appendChild(toast);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Expose functions globally for inline onclick handlers
window.showToast = showToast;
window.copyToClipboard = copyToClipboard;
