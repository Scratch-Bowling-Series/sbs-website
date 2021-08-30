$(document).ready(function(){
    var msg_closed = true;


    $('.msg-icon').click(function(){
        SetMessenger(!msg_closed);
    });
    $('#msg-close').click(function(){
        SetMessenger(!msg_closed);
    });
    $('.close-messenger').click(function(){
        SetMessenger(!msg_closed);
    });

    function SetMessenger(activate) {
        if (activate){
            msg_closed = true;
            $('.messenger-wrap').removeClass('expand');
            $('body').removeClass('no-scroll');
            $('.messenger-wrap').height(80);
            $('.messenger-wrap .messenger').height(70);
        }
        else{
            msg_closed = false;
            $('.messenger-wrap').addClass('expand');
            $('body').addClass('no-scroll');
            var value = window.innerHeight;

            $('.messenger-wrap').height(value);
            $('.messenger-wrap .messenger').height(value - 20);
        }
    }


    UpdateMain();
    setInterval(UpdateMain(), 15000);
    function UpdateMain(){
        console.log('Updating Messenger');
    }



});