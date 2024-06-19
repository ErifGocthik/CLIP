(function () {
    $(document).ready(function () {
        $(document).on('click', '.archive', function (e) {
            let archive_id = e.currentTarget.className.split(' ')[1].split('_')[1];
            window.location.replace(`/archive/${archive_id}`);
            // alert('click');
        });
        let add_btn = $('.add-archives');
        add_btn.click(function (event) {
            $('.modal-window-archives').css({
                'display': 'block'
            });
        });
        let modalWindow = $('.modal-window-archives');
        let win = $('.window-archives');
        let trigger = true;
        win.mouseover(function () {
            trigger = false;
        });
        win.mouseout(function () {
            trigger = true;
        });
        modalWindow.click(function (e) {
            if (trigger) {
                modalWindow.css({
                    'display': 'none'
                });
            }
        });
    });
})();