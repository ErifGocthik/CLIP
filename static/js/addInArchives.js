(function addInArchives() {
    $(document).ready(function () {
        let add_btn = $('.archive-btn-add');
        let archives_arr = [];
        let img_id = '';
        let a_id = '';
        add_btn.click(function (event) {
            $('.modal_window_add_in_archive').css({
                'display': 'flex'
            });
            let archives_html = $('.archives .archive')
        for (let j = 0; j < archives_html.length; j++) {
            $.ajax({
                url: 'checkIIA/',
                data: {'img_id': $('.window_image_detail_id').attr('class').split(' ')[1].split('_')[2], 'a_id': archives_html.eq(j).attr('class').split(' ')[1].split('_')[1]},
                success: function (data) {
                    if(data.image_exists) {
                        archives_html.eq(j).addClass('disabled');
                        $('.archives .archive .content').eq(j).removeAttr('style');
                    } else {
                        if (archives_html.eq(j).hasClass('disabled')) {
                            console.log('nonono');
                            archives_html.eq(j).removeClass('disabled');
                        }
                    }
                    console.log(data)
                },
                error: function (data) {
                    console.error('KeyError');
                }
            });
        }
        });
        let modalWindow = $('.modal_window_add_in_archive');
        let win = $('.archives');
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
        $(document).on('click', '.archive', function (event) {
            a_id = event.currentTarget.className.split(' ')[1].split('_')[1];
            img_id = $('.window_image_detail_id').attr('class').split(' ')[1].split('_')[2];
            let archiveId = $(`.archive.id_${a_id}`);
            if (archiveId.hasClass('check')) {
                archiveId.removeClass('check');
                archives_arr.splice(archives_arr.indexOf(a_id), 1);
            } else {
                archiveId.addClass('check');
                archives_arr.push(a_id);
            }
        });
        $('.accept-btn').click(function () {
            for (let i = 0; i < archives_arr.length; i++) {
                $.ajax({
                    url: 'addInArchive/',
                    data: {'img_id': img_id, 'a_id': archives_arr[i]},
                    success: function (data) {
                        if (!data.has) {
                            let archive = $(`.archive.id_${archives_arr[i]} .content`);
                            archive.css({'background-color': 'rgba(28,141,28,0.1)'});
                            $('.modal_window_add_in_archive').css({
                                'display': 'none'
                            })
                            if ($(`.archive.id_${archives_arr}`).hasClass('check')) {
                                $(`.archive.id_${archives_arr}`).removeClass('check');
                                archives_arr = [];
                            }
                        } else {
                            let archive = $(`.archive.id_${archives_arr[i]} .content`);
                            archive.css({'background-color': 'rgba(141,28,28,0.1)'});
                        }
                    }
                });
            }
        });
    });
})();