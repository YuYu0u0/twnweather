document.addEventListener('DOMContentLoaded', function () {
    const servicesLink = document.getElementById('services-link');
    const servicesLink2 = document.getElementById('services-link2');
    const dropdowns = document.querySelectorAll('.dropdown');

    servicesLink.addEventListener('click', function (event) {
        event.preventDefault();
        dropdowns.forEach(dropdown => dropdown.classList.remove('active')); // Close other dropdowns
        this.nextElementSibling.classList.toggle('active'); // Toggle current dropdown
    });

    servicesLink2.addEventListener('click', function (event) {
        event.preventDefault();
        dropdowns.forEach(dropdown => dropdown.classList.remove('active')); // Close other dropdowns
        this.nextElementSibling.classList.toggle('active'); // Toggle current dropdown
    });

    document.addEventListener('click', function (event) {
        if (!servicesLink.contains(event.target) && !servicesLink2.contains(event.target) && !event.target.closest('.dropdown')) {
            dropdowns.forEach(dropdown => dropdown.classList.remove('active'));
        }
    });
});
