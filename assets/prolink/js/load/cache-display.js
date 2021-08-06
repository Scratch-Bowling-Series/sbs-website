const fs = require('fs')
const { remote } = require('electron');
const app = remote.app;

$(document).ready(function()
{
    var multiplier = 100;

    var color_1 = '#157A6E';
    var color_2 = '#499F68';
    var color_3 = '#77B28C';
    var color_4 = '#C2C5BB';
    var color_5 = '#202225';

    var bowlers = GetFileSize('bowlers_cache.dat');
    var patterns = GetFileSize('patterns_cache.dat');
    var tournaments = GetFileSize('tournaments_cache.dat');
    var centers = GetFileSize('centers_cache.dat');




    $('.sr-cache .text-bowlers').text('(' + bowlers.toFixed(2) + 'MB)');
    $('.sr-cache .text-patterns').text('(' + patterns.toFixed(2) + 'MB)');
    $('.sr-cache .text-tournaments').text('(' + tournaments.toFixed(2) + 'MB)');
    $('.sr-cache .text-centers').text('(' + centers.toFixed(2) + 'MB)');

    bowlers *= multiplier;
    patterns *= multiplier;
    tournaments *= multiplier;
    centers *= multiplier;

    var longest = 0;
    if(bowlers > longest){longest = bowlers;}
    if(patterns > longest){longest = patterns;}
    if(tournaments > longest){longest = tournaments;}
    if(centers > longest){longest = centers;}



    var range = longest * 4;
    bowlers /= range;
    patterns /= range;
    tournaments /= range;
    centers /= range;

    bowlers *= 100;
    patterns *= 100;
    tournaments *= 100;
    centers *= 100;



    console.log('BOWLERS: ' + bowlers);
    console.log('patterns: ' + patterns);
    console.log('tournaments: ' + tournaments);
    console.log('centers: ' + centers);

    var array_1 = [bowlers, color_1, 'Bowlers'];
    var array_2 = [patterns, color_2, 'Oil Patterns'];
    var array_3 = [tournaments, color_3, 'Tournaments'];
    var array_4 = [centers, color_4, 'Centers'];

    var sortarr = [array_1, array_2, array_3, array_4];

    // Sort the array based on the second element
    sortarr.sort(function(first, second) {
        return second[0] - first[0];
    });


    var col_1 = sortarr[0][1];
    var col_2 = sortarr[1][1];
    var col_3 = sortarr[2][1];
    var col_4 = sortarr[3][1];
    var col_5 = color_5;
    var var_1 = sortarr[0][0];
    var var_2 = sortarr[1][0];
    var var_3 = sortarr[2][0];
    var var_4 = sortarr[3][0];


    var_2 += var_1;
    var_3 += var_2;
    var_4 += var_3;

    var gradient = col_1 + ' 0%, ' + col_1 + ' ' + var_1 + '%,' + col_2 + ' ' + var_1 + '%,' + col_2 + ' ' + var_2 + '%,' + col_3 + ' ' + var_2 + '%,' + col_3 + ' ' + var_3 + '%,' + col_4 + ' ' + var_3 + '%, ' + col_4 + ' ' + var_4 + '%,' + col_5 + ' ' + var_4 + '%, ' + col_5 +' 100%';
    gradient = 'linear-gradient(90deg, ' + gradient + ')';
    $('.sr-cache .bar').css('background', gradient);

    $.each(sortarr, function(index, value)
    {
        var amount = (value[0] / 100) * range;
        amount /= 100;
        var html = '<div class="type-row"><div class="type-color" style="background-color:' + value[1] + ';"></div><label>' + value[2] + '<span class="text-bowlers">(' + amount.toFixed(2) + 'MB)</span></label></div>'
        console.log(html);
        $('.sr-cache').append(html);
    });
});

function GetFileSize(fileName)
{
    fileName = app.getPath("userData") + "/" + fileName;
    var stats = fs.statSync(fileName)
    var fileSizeInBytes = stats.size;
    var fileSizeInMegabytes = fileSizeInBytes / (1024*1024);
    return fileSizeInMegabytes;
}

String.format = function() {
    var s = arguments[0];
    for (var i = 0; i < arguments.length - 1; i++) {
        var reg = new RegExp("\\{" + i + "\\}", "gm");
        s = s.replace(reg, arguments[i + 1]);
    }
    return s;
}


