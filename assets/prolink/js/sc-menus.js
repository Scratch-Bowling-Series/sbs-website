$(document).ready(function()
{
    var currentPage = 2;
    OpenPage(currentPage);

    $('.sc-next').click(function()
    {
        OpenPage(currentPage + 1);
    });

    $('.sc-prev').click(function()
    {
        OpenPage(currentPage - 1);
    });

    $('.sc-sidebar a').click(function()
    {
        OpenPage($(this).index());
    });



    function OpenPage(pageNumber)
    {
        if ($('.sc-p-' + pageNumber).length)
        {
            var sideHeight = $('.sc-sidebar a:last-child').offset().top;
            var totalTop = $('.sc').offset().top;
            sideHeight -= totalTop;
            console.log(sideHeight);
            $('.sc').css('min-height', sideHeight + 400);
            var pageHeight = $('.sc-p-' + pageNumber).height();
            $('.sc').css('height', pageHeight + 100);
            $('.sc-content-page').css('display','none');
            $('.sc-p-' + pageNumber).css('display','block');
            $('.sc-sidebar i').css('display','none');
            $('.sc-sidebar i').eq(pageNumber - 1).css('display','inline-block');
            $('.sc-sidebar a').removeClass('selected');
            $('.sc-sidebar a').eq(pageNumber - 1).addClass('selected');
            Align();
            currentPage = pageNumber;
        }
    }
       Align();
            $(window).resize(function()
            {
                Align();
            });
            function Align()
            {
                var element = $('.center-vertically');
                var windowHeight = $(window).height() - 25;
                var height = element.height();
                var margin = ((windowHeight - height) / 2);
                if(margin < 10){ margin = 10;}
                element.css('margin-top', margin);
            }
});