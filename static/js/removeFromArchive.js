(function removeFromArchive() {
    $(document).ready(function () {
        let imageId = ''
        let archiveId = ''
        $(document).on('click', '.remove_btn', function () {
            imageId = $('.window_image_detail_id').attr('class').split(' ')[1].split('_')[2];
            archiveId=location.pathname.split('/')[2]
            $.ajax({
                url: '/removeInArchive/',
                type: 'GET',
                data: {'img_id': imageId, 'a_id': archiveId},
                success: function (data) {
                    // imageId = $('.window_image_detail_id').attr('class').split(' ')[1].split('_')[2];
                    $(`.card.id_${imageId}`).remove()
                    $('.modal_window_image_detail_id').css({
                        'display': 'none'
                    })
                }
            })
        });
    });
})();