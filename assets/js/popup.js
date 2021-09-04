$(document).ready(function()
{
    $('.popup').show();
    $('.popup .close').click(function (){
        $('.popup').hide();
    });
    $('.popup .continue').click(function (){
        $('.popup').hide();
        var url = $('.popup .continue').attr('data');
        if(url != ''){
            setTimeout(function (){ window.location.href = url; }, 1000);
        }
    });

    $(window).resize(function(){

        CenterPopup();
    });

    CenterPopup();


    function CenterPopup(){
            var inheight = $('.popup-inner').height();

            if(inheight > $(window).height()){
                $('.popup-inner').height($(window).height());
            }
            var margins = ($(window).height() - inheight) / 2;
            $('.popup-inner').css('margin-top', margins);
            $('.popup-inner').css('margin-bottom', margins);
            console.log('applied margin ' + margins);
    }

    $(function() {
        var glower = $('.glow');
        window.setInterval(function() {
            glower.toggleClass('active');
        }, 2000);
    });
});