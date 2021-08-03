const fs = require('fs')
const { remote } = require('electron');
const app = remote.app;


$(document).ready(function()
{
    LoadBowlersToPage();
    function LoadBowlersToPage()
    {
        fileName = app.getPath("userData") + '/bowlers_cache.dat';
        fs.readFile(fileName, 'utf8' , (err, data) => {
            if (err) {
                return false;
            }
            var bowlers = JSON.parse(data);
            var length = Object.keys(bowlers).length;
            var count = 0;
            $.each(bowlers, function(index, bowler){
                count += 1;
                if(bowler[0] != 'None')
                {
                    var date = bowler[2];
                    if(date != 'None')
                    {
                        date = new Date(date);
                        date = date.getMonth() + '/' + date.getDay() + '/' + date.getYear();
                    }
                    else
                    {
                        date = '8/1/21';
                    }

                    generated_html = '<section class="grid-2-25">';
                    generated_html += '<img class="bowler-picture" src="/media/' + bowler[5] + '" alt="">';
                    generated_html += '<div class="bowler-obj-wrap">';
                    generated_html += '<a class="bowler-name">' + bowler[0] + ' ' + bowler[1] + '</a>';
                    generated_html += '<a class="bowler-location">' + bowler[3] + ' ' + bowler[4] + '</a>';
                    generated_html += '<a class="bowler-date">JOINED: ' + date + '</a>';
                    generated_html += '</div></section>';
                    $('#bowler-objects-container').append(generated_html);
                    if (count == length - 1)
                    {
                        $('.grid-2-25').css('opacity', 1);
                        $('section').css('opacity', 1);
                        console.log('OPACITY' + index);
                        Fix();
                    }
                }
            });
        });
    }
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