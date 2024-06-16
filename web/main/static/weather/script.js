document.addEventListener('DOMContentLoaded', function () {
    const servicesLink = document.getElementById('services-link');
    const servicesLink2 = document.getElementById('services-link2');
    const dropdowns = document.querySelectorAll('.dropdown');

    if (servicesLink) {
        servicesLink.addEventListener('click', function (event) {
            event.preventDefault();
            dropdowns.forEach(dropdown => dropdown.classList.remove('active')); // Close other dropdowns
            this.nextElementSibling.classList.toggle('active'); // Toggle current dropdown
        });
    } else {
        console.error('Element with ID "services-link" not found');
    }

    if (servicesLink2) {
        servicesLink2.addEventListener('click', function (event) {
            event.preventDefault();
            dropdowns.forEach(dropdown => dropdown.classList.remove('active')); // Close other dropdowns
            this.nextElementSibling.classList.toggle('active'); // Toggle current dropdown
        });
    } else {
        console.error('Element with ID "services-link2" not found');
    }

    document.addEventListener('click', function (event) {
        if ((!servicesLink || !servicesLink.contains(event.target)) &&
            (!servicesLink2 || !servicesLink2.contains(event.target)) &&
            !event.target.closest('.dropdown')) {
            dropdowns.forEach(dropdown => dropdown.classList.remove('active'));
        }
    });
});
