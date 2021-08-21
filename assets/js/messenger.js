$(document).ready(function(){
    var msg_closed = true;


    $('.msg-icon').click(function(){
        if(msg_closed)
        {
            msg_closed = false;
            $('.messenger-wrap').addClass('expand');
            $('body').addClass('no-scroll');
        }
        else
        {
            msg_closed = true;
            $('.messenger-wrap').removeClass('expand');
            $('body').removeClass('no-scroll');
        }
    });
    $('#msg-close').click(function(){
        if(msg_closed)
        {
            msg_closed = false;
            $('.messenger-wrap').addClass('expand');
            $('body').addClass('no-scroll');
        }
        else
        {
            msg_closed = true;
            $('.messenger-wrap').removeClass('expand');
            $('body').removeClass('no-scroll');
        }
    });
    $('.close-messenger').click(function(){
        if(msg_closed)
        {
            msg_closed = false;
            $('body').addClass('no-scroll');
            $('.messenger-wrap').addClass('expand');
        }
        else
        {
            msg_closed = true;
            $('body').removeClass('no-scroll');
            $('.messenger-wrap').removeClass('expand');
        }
    });

    UpdateMain();
    setInterval(UpdateMain(), 15000);
    function UpdateMain(){
        console.log('Updating Messenger');
    }
});