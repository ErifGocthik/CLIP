(function download() {
    $(document).ready(function () {
        let imageId = '';
        $(document).on('click', '.download', function () {
            imageId = $('.window_image_detail_id').attr('class').split(' ')[1].split('_')[2];
            document.location.pathname = `/image/${imageId}/download/`;
        });
        let image_pk = $(document).find('.window_image_detail_id')
        $(document).on('click', '.share', function () {
            $.ajax({
                url: `/link/${image_pk.attr('class').split(' ')[1].split('_')[2]}`,
                type: 'get',
                success: function (data) {
                    alert(`ссылка для копирования:  ${data.link}`);
                    console.log(data.link)
                }
            })
        })
    });
})();