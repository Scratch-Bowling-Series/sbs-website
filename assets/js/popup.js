$(document).ready(function()
{
    var cookieValue = $.cookie("viewedPopup-1");
    //cookieValue = false;
    if(cookieValue == false || cookieValue == null)
    {
        $('.popup').show();
        $('.popup .close').click(function ()
        {
            $.cookie("viewedPopup-1", true);
            $('.popup').hide();
        });
        $('.popup .continue').click(function ()
        {
            $.cookie("viewedPopup-1", true);
            $('.popup').hide();
            setTimeout(function (){window.location.href = "http://scratchbowling.pythonanywhere.com/support";},1000);

        });
    }
    $(function() {
        var glower = $('.glow');
        window.setInterval(function() {
            glower.toggleClass('active');
        }, 2000);
    });
});