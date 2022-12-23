$('documnet').ready(() => {
    const inputEls = $('INPUT.input_amenities');
    const header4El = $('.amenities h4');
    let amenDict = {};

    inputEls.click(() => {
        let $input = $(this);

        if ($input.is(':checked')) {
            amenDict[$input.attr('data-id')] = $input.attr('data-name');
        }else {
            delete amenDict[`${$input.attr('data-id')}`];
        }

        header4El.text(Object.values(amenDict).join(','));
    })
});