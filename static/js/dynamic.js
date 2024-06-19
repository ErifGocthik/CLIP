(function () {
    $(document).ready(function (e) {
        function get_size(file_size) {
            let result = 0;
            let size = file_size;
            let name = 'б';
            let remains = 0.0;
            if (size > 1024) {
                result = size / 1024;
                name = 'Кб'
                if (result > 1024) {
                    result = result / 1024;
                    name = 'Мб';
                    if (result > 1024) {
                        result = result / 1024;
                        name = 'Гб';
                    }
                }
            }
            remains = Number('0.' + String(remains));
            return `${result.toFixed(2)} ${name}`;
        }

        let upload_btn = $('.upload');
        let page = 2;
        let notEmptyPage = 0;
        upload_btn.click(function (event) {
            $('.modal-window').css({
                'display': 'block'
            });
        });
        let modalWindow = $('.modal-window');
        let win = $('.window');
        let trigger = true;
        let nextPage = 0;
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
        $(window).scroll(function () {
            // console.log($(window).scrollTop(), '  ===  ', $(document).height() - $(window).height());
            // console.log($(window).scrollTop(), '>=', ($(document).height() - $(window).height()) - 1);
            if ($(window).scrollTop() >= $(document).height() - $(window).height() - 1) {
                nextPage = page++;
                // console.log(nextPage, '  +  ', page, $(window).scrollTop() >= $(document).height() - $(window).height());
                // notEmptyPage = page;
                $.ajax({
                    url: '/inf/',
                    data: {'page': nextPage},
                    success: function (data) {
                        // if (data.results.length <= 0) {
                        //     page--;
                        // }

                        nextPage = page;
                        console.log($(window).scrollTop());
                        for (let j = 0; j < data.results.length; j++) {
                            imageUrl = data.results[j].image
                            imageName = data.results[j].name
                            imageW = data.results[j].width
                            imageH = data.results[j].height
                            imageSize = data.results[j].file_size
                            // console.log(data.results)
                            $('.images').append(
                                `<div class="card id_${data.results[j].id}" style="background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.4)), url('/media/${imageUrl}')">
                                    <div class="img-info">
                                        
                                    </div>
                                    <div class="title"><p style="word-break: break-all; width: 100%">${imageName}</p></div>
                                </div>`
                            );
                        }
                        // console.log(nextPage);
                    },
                    error: function () {
                        alert('')
                    }
                });
            }
        });
    });
})();