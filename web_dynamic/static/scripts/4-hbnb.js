$('documnet').ready(() => {    
    let checkBox = $('INPUT[type="checkbox"]');
    let amenities = {};
    let apiStatusEl = $('DIV#api_status');

    function appendPlaces(places) {
        let placesEl = $('SECTION.places')
        placesEl.append(places.map(place => {
            return `
                <article>
                    <div class="title_box">
                        <h2>${place.name}</h2>
                        <div class="price_by_night">${place.price_by_night}</div>
                    </div>
                    <div class="information">
                        <div class="max_guest">${ place.max_guest } Guest ${place.max_guest != 1 && 's'}</div>
                            <div class="number_rooms">${place.number_rooms} Bedroom ${place.number_rooms != 1 && 's'}</div>
                            <div class="number_bathrooms">${place.number_bathroomss} Bathroom ${ place.number_bathrooms != 1 && 's' }</div>
                    </div>
                    <div class="user">
                        <b>Owner:</b> ${ place.user.first_name} ${ place.user.last_name }
                    </div>
                    <div class="description">
                    ${place.description | 'safe'}
                    </div>
                </article>`
        }))
    };

    $.ajax({
        method: 'GET',
        url: `http://${window.location.hostname}:5001/api/v1/status/`,
        success: (res) => {
            // console.log(res);

            if (res.status == "OK") {
                apiStatusEl.addClass('available');
            } else {
                if (apiStatusEl.hasClass('available')) {
                    apiStatusEl.removeClass("available");
                }
            }
        }
    });

    $.ajax({
        method: 'POST',
        url: `http://${window.location.hostname}:5001/api/v1/places_search/`,
        contentType: 'application/json',
        data: '{}',
        dataType: 'json',
        success: (places) => {
            // console.log(places)
            appendPlaces(places);
        }
    });

    $('BUTTON').click(() => {
        $.ajax({
            method: 'POST',
            url: `http://${window.location.hostname}:5001/api/v1/places_search/`,
            contentType: 'application/json',
            data: JSON.stringify({ 'amenities': Object.keys(amenities) }),
            dataType: 'json',
            success: (places) => {
                appendPlaces(places);
            }
        });
    });

    function addItem() {
        if (Object.values(amenities).length === 0) {
            $('.amenities H4').html('&nbsp;');
        } else if(Object.values(amenities).length > 2) {
            $('.amenities H4').text(Object.values(amenities).slice(0, 2).join(', ') + '...');
        }else {
            $('.amenities H4').text(Object.values(amenities).join(', '));
        }
    };
    
    checkBox.change(function () {
        if ($(this).is(':checked')) {
            amenities[$(this).attr('data-id')] = $(this).attr('data-name');
        } else {
            delete amenities[$(this).attr('data-id')];
        }
        addItem();
    });
});
