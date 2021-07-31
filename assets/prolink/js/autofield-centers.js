$(document).ready(function()
{
    var search_args = '';
    var last_searched = '';

    console.log('loaded');
    $('#autofield-center').on('click', 'a', function (){
        $('.autofield-center-input').val($(this).attr('data'));
        $('#autofield-center').empty();
    });

    $('.autofield-center-input').keyup(function()
    {
        search_args = $('.autofield-center-input').val();
        if(search_args == ''){ $('#autofield-center').empty(); }
    });

    const interval = setInterval(function()
    {
        if(search_args.length > 2 && last_searched != search_args)
        {
            last_searched = search_args;
            RunSearch(search_args);
        }
    }, 1000);

    function RunSearch(search)
    {
        $.getJSON('/prolink/centers/autofield/' + search + '/', function(data) {
            $('#autofield-center').empty();
            $.each(data, function(index, bowler)
            {
                Add(bowler);
            });
        });
    }

    function Add(center)
    {
        generated_html = '<a class="autofield-button-center" data="' + center[0] +'">';
        generated_html += center[0];
        generated_html += '&nbsp;<span>';
        generated_html += center[1];
        generated_html += '</span></a>';
        $('#autofield-center').append(generated_html);
    }

});