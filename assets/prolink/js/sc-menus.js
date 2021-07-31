$(document).ready(function()
{
    var currentPage = 1;
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
            $('.sc-content-page').css('display','none');
            $('.sc-p-' + pageNumber).css('display','block');
            $('.sc-sidebar i').css('display','none');
            $('.sc-sidebar i').eq(pageNumber - 1).css('display','inline-block');
            $('.sc-sidebar a').removeClass('selected');
            $('.sc-sidebar a').eq(pageNumber - 1).addClass('selected');
            currentPage = pageNumber;
        }
    }

});