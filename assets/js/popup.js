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


    $(window).resize(function(){

        CenterPopup();
    });

    function CenterPopup(){
            if($('.popup-inner').Height() > $('.popup').Height()){
                $('.popup-inner').Height($('.popup').Height());
            }
            $('.popup-inner').css('margin', margins + 'px auto');
            var margins = ($('.popup').Height() - $('.popup-inner').Height()) / 2;
    }

    $(function() {
        var glower = $('.glow');
        window.setInterval(function() {
            glower.toggleClass('active');
        }, 2000);
    });
});