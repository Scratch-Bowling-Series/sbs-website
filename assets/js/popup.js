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
            var inheight = $('.pop-inner').height();

            if(inheight > $(window).height()){
                $('.pop-inner').height($(window).height());
            }
            var margins = ($(window).height() - inheight) / 2;
            $('.pop-inner').css('margin-top', margins);
            $('.pop-inner').css('margin-bottom', margins);
    }

    $(function() {
        var glower = $('.glow');
        window.setInterval(function() {
            glower.toggleClass('active');
        }, 2000);
    });
});