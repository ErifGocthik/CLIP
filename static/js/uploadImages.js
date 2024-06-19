(function () {
    $(document).ready(function () {

        let cookie = document.cookie;
        let csrfToken = cookie.substring(cookie.indexOf('=') + 1);

        $('.upload-btn').click(function (e) {
            // alert('true');
            e.preventDefault();
            let form_data = $('.window').find('.files').prop('files');
            let keys = {};

            for (let i = 0; i < form_data.length; i++) {
                let reader = new FileReader();

                reader.onload = function () {
                    let image = new Image();

                    image.onload = function () {
                        let width = image.width;
                        let height = image.height;

                        console.log("Ширина: " + width);
                        console.log("Высота: " + height);

                        keys[`image`] = [width, height, form_data[i].size];

                        let formData = new FormData();

                        console.log(form_data[i], '  ==  ', keys['image']);
                        file = form_data[i];


                        formData.append('file', file);
                        formData.append('keys', keys['image']);

                        $.ajax({
                            url: '/uploading/',
                            type: 'POST',
                            // cache: false,
                            headers: {
                                'X-CSRFToken': csrfToken
                            },
                            data: formData,
                            // dataType: 'application/json',
                            processData: false,
                            contentType: false,
                            success: function (data) {
                                form_data = null;
                                $('.modal-window').css({'display': 'none'});
                            },
                            error: function (data) {
                                alert('Попробуйте заново');
                            }
                        });
                    }
                    image.src = reader.result;
                }
                reader.readAsDataURL(form_data[i]);
            }
            location.reload();
        });
    });
})();