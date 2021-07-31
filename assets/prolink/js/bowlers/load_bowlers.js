$(document).ready(function()
{
    var url = 'http://127.0.0.1'
    var currentPage = 0;
    var amountPerPage = 15;
    var element = document.getElementById('scroll-content');

    LoadNext();

    element.addEventListener('scroll', function(event)
    {
        var element = event.target;
        var scrolltop = (element.scrollTop + 00);
        if (element.scrollHeight  - scrolltop  === element.clientHeight)
        {
            LoadNext();
            console.log("SCROLL LOAD");
        }
    });

    function LoadNext()
    {
        $.getJSON('request/' + (currentPage + 1) + '/' + amountPerPage + '/', function(data) {
            $.each(data, function(index, bowler)
            {
                generated_html = '<section class="grid-2-33">';
                generated_html += '<img class="bowler-picture" src="/media/' + bowler[4] + '" alt="">';
                generated_html += '<div class="bowler-obj-wrap">';
                generated_html += '<a class="bowler-name">' + bowler[0] + '</a>';
                generated_html += '<a class="bowler-location">' + bowler[1] + '</a>';
                generated_html += '<a class="bowler-date">JOINED: ' + bowler[2] + '</a>';
                generated_html += '</div></section>';
                $('#bowler-objects-container').append(generated_html);
                currentPage += 1;
            });
        });
    }
    function LoadFirst()
    {
        $.getJSON('request/' + (currentPage + 1) + '/' + 100 + '/', function(data) {
            $.each(data, function(index, bowler)
            {
                generated_html = '<section class="grid-2-33">';
                generated_html += '<img class="bowler-picture" src="/media/' + bowler[4] + '" alt="">';
                generated_html += '<div class="bowler-obj-wrap">';
                generated_html += '<a class="bowler-name">' + bowler[0] + '</a>';
                generated_html += '<a class="bowler-location">' + bowler[1] + '</a>';
                generated_html += '<a class="bowler-date">JOINED: ' + bowler[2] + '</a>';
                generated_html += '</div></section>';
                $('#bowler-objects-container').append(generated_html);
                currentPage += 1;
            });
        });
    }
});



