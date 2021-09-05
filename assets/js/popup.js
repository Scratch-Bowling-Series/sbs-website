$(document).ready(function()
{
    $('.popup').show();
    $('.popup .close').click(function (){
        $('.popup').hide();
    });
    $('.popup .continue').click(function (){
        $('.popup').hide();
        var url = $('.popup .continue').attr('data');
        if(url != '' && url != 'undefined'){
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
            console.log('inheight: ' + inheight + ' window:' + $(window).height());
    }

    $(function() {
        var glower = $('.glow');
        window.setInterval(function() {
            glower.toggleClass('active');
        }, 2000);
    });



    function ClaimAccount(userId){

    }

    $('.claim-btn').click(function(){
        userId = $('.claim-btn').attr('data');
        if(userId != null && userId != 'undefined' && userId != ''){
            $.ajax(
            {
                type: "GET",
                url: "https://scratchbowling.pythonanywhere.com/accouant/claim/" + userId,
                contentType: "text/plain",
                dataType: "text",
                success: function (data) {
                    if(data == 'success')
                    {
                        $(this).text('CLAIMED')
                        setTimeout(function(){$('.popup').hide();}, 2000)
                    }
                    else{
                        $(this).text('ERROR')
                        setTimeout(function(){$(this).text('CLAIM');}, 1500)
                    }
                }
            });
        }
    });
});