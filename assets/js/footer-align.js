$(document).ready(function() {
    var height_diff = $(window).height() - ($('footer').offset().top + 50);
    if (height_diff > 0) {
        console.log(height_diff)
        $('footer').css('margin-top', height_diff);
    }

    var closed = true;
    $('#nav-expand').click(function(){
        if(closed)
        {
            closed = false;
            $('.nav-account').css('display', 'flex');
            $('.nav-buttons').css('display', 'block');
            $('.nav-drop-button i').css('text-shadow', '-1px -1px 0 #d9af62,  1px -1px 0 #d9af62,-1px 1px 0 #d9af62,1px 1px 0 #d9af62');
            $('#nav-icon1').addClass('open');
        }
        else
        {
            closed = true;
            $('.nav-account').css('display', 'none');
            $('.nav-buttons').css('display', 'none');
            $('.nav-drop-button i').css('text-shadow', 'none');
            $('#nav-icon1').removeClass('open');
        }
    });
    var msg_closed = true;
    $('.msg-icon').click(function(){
        if(msg_closed)
        {
            msg_closed = false;
            $('.messenger').addClass('expand');
        }
        else
        {
            msg_closed = true;
            $('.messenger').removeClass('expand');
        }
    });
    $('#msg-close').click(function(){
        if(msg_closed)
        {
            msg_closed = false;
            $('.messenger').addClass('expand');
        }
        else
        {
            msg_closed = true;
            console.log('close');
            $('.messenger').removeClass('expand');
        }
    });
});