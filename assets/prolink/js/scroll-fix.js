$(document).ready(function()
{
    Fix();
    $(window).resize(function(){
        Fix();
    });
    $('body').on('DOMSubtreeModified', '#content-wrapper', function(){
        console.log('changed');
        Fix();
    });

    function Fix()
    {
        var windowHeight = $('.content-wrapper').height();
        var contentHeight = $('#content')[0].scrollHeight;
        console.log(windowHeight + ' ' + contentHeight);
        if (contentHeight > windowHeight)
        {
            $('#content').css('width', 'calc(100% - 10px)');
            $('#content').css('margin-right', '10px');
        }
        else
        {
            $('#content').css('margin-right', '0px');
            $('#content').css('width', 'calc(100% - 0px)');
        }
    }
});