$('documnet').ready(() => {    
    let checkBox = $('INPUT[type="checkbox"]');
    let amenities = {};
    let apiStatusEl = $('DIV#api_status');

    $.ajax({
        method: 'GET',
        url: `http://${window.location.hostname}:5001/api/v1/status/`,
        success: (res) => {
            // console.log(res);

            if (res.status == "OK") {
                apiStatusEl.addClass('available');
            } else {
                if (apiStatusEl.hasClass('available')) {
                    apiStatusEl.removeClass("available")
                }
            }
        }
    })

    function addItem() {
        if (Object.values(amenities).length === 0) {
            $('.amenities H4').html('&nbsp;');
        } else if(Object.values(amenities).length > 2) {
            $('.amenities H4').text(Object.values(amenities).slice(0, 2).join(', ') + '...');
        }else {
            $('.amenities H4').text(Object.values(amenities).join(', '));
        }
    }
    
    checkBox.change(function () {
        if ($(this).is(':checked')) {
            amenities[$(this).attr('data-id')] = $(this).attr('data-name');
        } else {
            delete amenities[$(this).attr('data-id')];
        }
        addItem();
    });
});