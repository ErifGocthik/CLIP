(function imageInfo() {
    $(document).ready(function (e) {
        let image_id = 0;
        $(document).on('click', '.card', function (event) {
            // let btn = $('.card');
            let window = $('.modal_window_image_detail_id');
            let close_btn = $('.back');
            image_id = event.currentTarget.className.split('_')[1]
            console.log(image_id);
            $.ajax({
                url: '/getimage/',
                data: {'image_id': image_id},
                // type: 'GET',
                // dataType: 'json',
                success: function (data) {
                    $('.window_image_detail_id').html(
                        `<img src="${data.image_url}" alt="">`
                    );
                    $('.window_image_detail_id').toggleClass(`image_id_${image_id}`);
                },
                error: function (data) {
                    alert('');
                }
            });
            window.css({
                'display': 'block'
            });
            close_btn.click(function () {
                $('.window_image_detail_id').removeClass(`image_id_${image_id}`);
                window.css({
                    'display': 'none'
                });
            });
        });
    });
})();
