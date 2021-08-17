$(document).ready(function() {
    if($('.match-height master').css('') == ''){
        var height = $('.match-height master').height();
        $('.match-height slave').height(height);
    }
    if ($('.my-account-past-tournaments-container')[0].scrollHeight > $('.my-account-past-tournaments-container').height())
    {
        $('.my-account-past-tournaments-container').css('width', 'calc(100% - 20px)');
    }
});