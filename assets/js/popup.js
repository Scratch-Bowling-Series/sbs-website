$(document).ready(function()
{
    openPopup();
    registerPopupListeners();
    centerPopup();






    $('.claim-btn').click(function(){
        var btn = $(this);
        userId = btn.attr('data');
        if(userId != null && userId != 'undefined' && userId != ''){
            $.ajax(
            {
                type: "GET",
                url: "https://scratchbowling.pythonanywhere.com/account/claim/" + userId,
                contentType: "text/plain",
                dataType: "text",
                success: function (data) {
                    if(data == 'success')
                    {
                        btn.html('CLAIMED')
                        setTimeout(function(){$('.popup').hide();}, 2000)
                    }
                    else{
                        btn.html('ERROR')
                        setTimeout(function(){btn.html('CLAIM');}, 1500)
                    }
                }
            });
        }
    });
});

function openPopup(){
    if($('.popup').length > 0){
        var popup = $('.popup');
        var popupId = popup.attr('popupId');
        if ($.cookie('popup-closed-' + popupId) !== 1){
            popup.show();
        }
    }
}

function registerPopupListeners(){
    $('.pop-close').click(function (){
        var popup = $('.popup');
        var button = $(this);
        var remind = button.attr('remind');
        var popupId = popup.attr('popupId');
        if(remind === 'never'){
            $.cookie("popup-closed-" + popupId, 1);
        }
        else if(remind === 'default'){
            $.cookie("popup-closed-" + popupId, 1, { expires : 1 });
        }
        else{
            $.cookie("popup-closed-" + popupId, 1, { expires : 1 });
        }
        popup.hide();
    });
    $('.pop-continue').click(function (){
        var popup = $('.popup');
        var button = $(this);
        var remind = button.attr('remind');
        var popupId = popup.attr('popupId');
        var href = button.attr('data');
        if(href !== undefined){
            if(remind === 'never'){
                $.cookie("popup-closed-" + popupId, 1);
            }
            else if(remind === 'default'){
                $.cookie("popup-closed-" + popupId, 1, { expires : 1 });
            }
            else{
                $.cookie("popup-closed-" + popupId, 1, );
            }
            setTimeout(function (){ window.location.href = href; }, 1000);
        }
        popup.hide();
    });
    $(window).resize(function(){centerPopup();});
}

function centerPopup(){
    var inheight = $('.pop-inner').height();

    if(inheight > $(window).height()){
        $('.pop-inner').height($(window).height());
    }
    var margins = ($(window).height() - inheight) / 2;
    $('.pop-inner').css('margin-top', margins - 35);
    $('.pop-inner').css('margin-bottom', margins);
    console.log('inheight: ' + inheight + ' window:' + $(window).height());
}