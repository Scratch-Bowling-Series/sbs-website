$(document).ready(function()
{
    const url = 'http://127.0.0.1';
    let currentPage = 0;
    var amountPerPage = 9;
    var initialLoad = true;
    var element = document.getElementById('content');

    LoadNext();

    element.addEventListener('scroll', function(event)
    {
        const element = event.target;
        const scrolltop = (element.scrollTop + 0);
        if (element.scrollHeight  - scrolltop  === element.clientHeight)
        {

            LoadNext();
            console.log("SCROLL LOAD");
        }
    });

    function LoadNext()
    {
        var ammountPerPageTemp = amountPerPage;
        if(initialLoad)
        {
            amountPerPageTemp = 20;
            initialLoad = false;
        }
        console.log('Loading ' + amountPerPageTemp);
        $.getJSON('request/' + (currentPage + 1) + '/' + amountPerPageTemp + '/', function(data) {
            var length = data.length;
            console.log('DATA RECEIVED: ' + length);
            $.each(data, function(index, oil)
            {
                var generated_html = '<section class="grid-2-25">';
                generated_html += '<div class="oil-obj-wrap" data="' + oil[0] + '">';
                generated_html += '<a class="oil-name">' + oil[1] + '</a>';
                generated_html += '<a class="oil-location">KEGAL ID:' + oil[2] + '</a>';
                generated_html += '<div class="t-oil-display-wrap"><div class="t-oil-display">'

                display_length = oil[3].length;
                $.each(oil[3], function(count, oil_cell)
                {
                    var last = false;
                    if (count = display_length - 1){ last = true; }
                    generated_html += GetOilDisplayHtml(oil_cell, last);
                });


                generated_html += '</div></div></section>';
                $('#pattern-objects-container').append(generated_html);

                if(index == length - 1)
                {
                    setTimeout(function()
                    {
                        $('.grid-2-25').css('opacity',1);
                    }, 1000);
                }
            });
            currentPage += 1;
        });
    }

    function GetOilDisplayHtml(data, last=false)
    {   var lastCell = '';
        if (last){ lastCell = ' t-oil-cell-right'; }
        var html = "<span class='t-oil-cell " + lastCell + "'>";
        html += "<span class='t-oil-row t-oil-row-top' style='background:" + data[0] + ";'></span>";
        html += "<span class='t-oil-row' style='background:" + data[1] + ";'></span>";
        html += "<span class='t-oil-row' style='background:" + data[2] + ";'></span>";
        html += "<span class='t-oil-row' style='background:" + data[3] + ";'></span>";
        html += "<span class='t-oil-row' style='background:" + data[4] + ";'></span>";
        html += "<span class='t-oil-row' style='background:" + data[5] + ";'></span>";
        html += "<span class='t-oil-row t-oil-row-bottom' style='background:" + data[6] + ";'></span></span>";
        return html;
    }
});


