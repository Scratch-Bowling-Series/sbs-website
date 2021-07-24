$(document).ready(function() {
    var height_diff = $('#my-account-preview').height();
    $('#my-account-past-tournaments').height(height_diff);
    $('#my-account-season-stats').height(height_diff);

    if ($('.my-account-past-tournaments-container')[0].scrollHeight > $('.my-account-past-tournaments-container').height())
    {
        $('.my-account-past-tournaments-container').css('width', 'calc(100% - 20px)')
    }
});