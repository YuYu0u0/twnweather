function submitForm(city) {
    // Set the value of the hidden input to the ID of the clicked element
    document.getElementById('city').value = city;

    // Submit the form
    document.getElementById('weatherform').submit();
}

function showCities(element, region) {
    const regionButtons = document.querySelectorAll('.region-link');
    regionButtons.forEach(btn => {
        btn.classList.remove('active');
    });


    element.classList.add('active');

    const cities = {
        '北部': ['基隆市', '台北市', '新北市', '桃園市', '新竹縣', '新竹市', '苗栗縣'],
        '中部': ['台中市', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '嘉義市'],
        '南部': ['台南市', '高雄市', '屏東縣'],
        '東部': ['宜蘭縣', '花蓮縣', '台東縣'],
        '離島': ['澎湖縣', '金門縣', '連江縣']
    };

    const cityList = cities[region];

    if (cityList) {
        let links = '';
        cityList.forEach(city => {
            links += `<a href="javascript:void(0);" class="btn btn-outline-primary mx-2" onclick="submitForm('${city}')">${city}</a>`;
        });

        document.getElementById('city-links').innerHTML = links;
    }
}