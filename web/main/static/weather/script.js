document.addEventListener('DOMContentLoaded', function () {
    const servicesLink = document.getElementById('services-link');
    const dropdown = document.querySelector('.dropdown');

    servicesLink.addEventListener('click', function (event) {
        event.preventDefault();
        dropdown.classList.toggle('active');
    });

    document.addEventListener('click', function (event) {
        if (!servicesLink.contains(event.target) && !dropdown.contains(event.target)) {
            dropdown.classList.remove('active');
        }
    });
});
