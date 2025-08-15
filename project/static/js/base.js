var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all animate-fade-up elements
document.querySelectorAll('.animate-fade-up').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    observer.observe(el);
});

// Auto-hide alerts after 5 seconds
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-dismissible')) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    });
}, 5000);

// Add loading state to buttons
document.querySelectorAll('.action-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Add loading state
        const originalContent = this.innerHTML;
        this.innerHTML = `
            <div class="loading mx-auto mb-2"></div>
            <div>جاري التحميل...</div>
        `;
        this.style.pointerEvents = 'none';
        
        // Simulate loading
        setTimeout(() => {
            this.innerHTML = originalContent;
            this.style.pointerEvents = 'auto';
            
            // Show success message
            showNotification('تم بنجاح!', 'success');
        }, 2000);
    });
});

// Notification function
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Search functionality
document.querySelector('.search-enhanced input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        const query = this.value.trim();
        if (query) {
            showNotification(`جاري البحث عن: "${query}"`, 'info');
            // Simulate search
            setTimeout(() => {
                showNotification('تم العثور على 3 نتائج', 'success');
            }, 1000);
        }
    }
});

// Real-time clock update
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('ar-SA');
    const dateString = now.toLocaleDateString('ar-SA', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    
    // Update any clock elements if they exist
    const clockElements = document.querySelectorAll('.live-clock');
    clockElements.forEach(el => {
        el.textContent = `${timeString} - ${dateString}`;
    });
}

// Update clock every second
setInterval(updateClock, 1000);
updateClock(); // Initial call

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add pulse animation to notification badge
const notificationBadge = document.querySelector('.notification-badge');
if (notificationBadge) {
    setInterval(() => {
        notificationBadge.style.animation = 'pulse 1s';
        setTimeout(() => {
            notificationBadge.style.animation = '';
        }, 1000);
    }, 5000);
}

document.addEventListener('DOMContentLoaded', function() {
  var date = document.getElementById('client-date');
  if (date) {
    date.textContent = new Date().toLocaleDateString('ar-EG', {
      weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
    });
    alert(date.textContent);
  }
});
