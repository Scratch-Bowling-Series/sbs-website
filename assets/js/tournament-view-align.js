$(document).ready(function() {
    //var height_diff = $('#my-account-preview').height() + 15;
    //$('#my-account-past-tournaments').height(height_diff);my-account-past-tournaments-container
    //$('#my-account-season-stats').height(height_diff);width:calc(100% - 20px)

    if ($('.tournament-info-slide-container')[0].scrollHeight > $('.tournament-info-slide-container').height())
    {
        $('.tournament-info-slide-container').css('width', 'calc(100% - 20px)')
        $('.tournament-view-qualifying-slide-label').css('width', 'calc(100% - 65px)')
    }
});