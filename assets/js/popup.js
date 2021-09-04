$(document).ready(function()
{
    $('.popup').show();
    $('.popup .close').click(function ()
        {
            $('.popup').hide();
        });
        $('.popup .continue').click(function ()
        {
            $('.popup').hide();
            var url = $('.popup .continue').attr('data');
            if(url != ''){
                setTimeout(function (){ window.location.href = url; }, 1000);
            }
        });

    CenterPopup();
    $(window).resize(function(){

        CenterPopup();
    });

    function CenterPopup(){
            if($('.popup-inner').height() > $('.popup').height()){
                $('.popup-inner').height($('.popup').height());
            }
            var margins = ($('.popup').height() - $('.popup-inner').height()) / 2;
            $('.popup-inner').css('margin', margins + 'px auto');
    }

    $(function() {
        var glower = $('.glow');
        window.setInterval(function() {
            glower.toggleClass('active');
        }, 2000);
    });
});