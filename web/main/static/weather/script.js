document.addEventListener('DOMContentLoaded', function () {
    const servicesLink = document.getElementById('services-link');
    const servicesLink2 = document.getElementById('services-link2');
    const dropdowns = document.getElementById('services_list');
    const dropdowns2 = document.getElementById('accounts_list');

    servicesLink.addEventListener('click', function (event) {
        event.preventDefault();
        dropdowns.classList.remove('active'); // Close other dropdowns
        this.nextElementSibling.classList.toggle('active'); // Toggle current dropdown
    });

    servicesLink2.addEventListener('click', function (event) {
        event.preventDefault();
        dropdowns2.classList.remove('active'); // Close other dropdowns
        this.nextElementSibling.classList.toggle('active'); // Toggle current dropdown

    });

    document.addEventListener('click', function (event) {
        if (!servicesLink.contains(event.target) && !event.target.closest('.dropdown')) {
            dropdowns.classList.remove('active');
        }
        if (!servicesLink2.contains(event.target) && !event.target.closest('.dropdown')) {
            dropdowns2.classList.remove('active');
        }
    });
});
