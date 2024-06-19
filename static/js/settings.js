(function f() {
    $(document).ready(function () {
        let trigger = false;
        $(document).on('click', '.settings', function (e) {
            if ($('.modal_settings').css('display') == 'none') {
                $('.modal_settings').css({'display': 'flex'});
                // elem = $('.settings');
            } else {
                $('.modal_settings').css({'display': 'none'});
                // elem = $('.settings');
            }
        });
    });
})();