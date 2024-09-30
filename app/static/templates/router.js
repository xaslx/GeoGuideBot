if (ymaps) {
    ymaps.ready(init);
} else {
    alert('ошибка');
}


function init() {
    try {
        var start_address = document.getElementById('start_address').value.trim();
        var end_address = document.getElementById('end_address').value.trim();

        start_address = decodeURIComponent(start_address);
        end_address = decodeURIComponent(end_address);

        var latitude = parseFloat(document.getElementById('latitude').value.trim());
        var longitude = parseFloat(document.getElementById('longitude').value.trim());

        var myMap = new ymaps.Map("map", {
            center: [latitude, longitude],
            zoom: 13
        });

        const tg = window.Telegram.WebApp;
        tg.expand();

        ymaps.route([start_address, end_address]).then(function (route) {
            myMap.geoObjects.add(route);

            var points = route.getWaypoints();
            points.options.set('preset', 'twirl#redStretchyIcon');
            points.get(0).properties.set('iconContent', 'Точка отправления');
            points.get(points.length - 1).properties.set('iconContent', 'Точка прибытия');

        }, function (error) {
            alert('Ошибка при построении маршрута: ' + error.message);
        });
    } catch (e) {
        alert('Произошла ошибка в функции init: ' + e.message);
    }
}