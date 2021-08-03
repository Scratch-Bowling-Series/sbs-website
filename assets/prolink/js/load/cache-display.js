const fs = require('fs')
const { remote } = require('electron');
const app = remote.app;

$(document).ready(function()
{
    var multiplier = 10;

    var color_1 = '#157A6E';
    var color_2 = '#499F68';
    var color_3 = '#77B28C';
    var color_4 = '#C2C5BB';
    var color_5 = '#202225';

    var bowlers = GetFileSize('bowlers_cache.dat') * multiplier;
    var patterns = GetFileSize('patterns_cache.dat') * multiplier;
    var tournaments = GetFileSize('tournaments_cache.dat') * multiplier;
    var centers = GetFileSize('centers_cache.dat') * multiplier;

    console.log('BOWLERS: ' + bowlers);
    console.log('patterns: ' + patterns);
    console.log('tournaments: ' + tournaments);
    console.log('centers: ' + centers);


    patterns += bowlers;
    tournaments += patterns;
    centers += tournaments;

    var g_bowlers = color_1 + ' ' + 0 + '%, ' + color_1 + ' ' + bowlers + '%,';
    var g_patterns = color_2 + ' ' + bowlers + '%, ' + color_2 + ' ' + patterns + '%,';
    var g_tournaments = color_3 + ' ' + patterns + '%, ' + color_3 + ' ' + tournaments + '%,';
    var g_centers = color_4 + ' ' + tournaments + '%, ' + color_4 + ' ' + centers + '%,';
    var g_none = color_5 + ' ' + centers + '%, ' + color_5 + ' ' + 100 + '%';


    var gradient = 'linear-gradient(90deg, ' + g_bowlers + g_patterns + g_tournaments + g_centers + g_none + ')';

    $('.sr-cache .bar').css('background',gradient);
    console.log('set');
});

function GetFileSize(fileName)
{
    fileName = app.getPath("userData") + "/" + fileName;
    var stats = fs.statSync(fileName)
    var fileSizeInBytes = stats.size;
    var fileSizeInMegabytes = fileSizeInBytes / (1024*1024);
    return fileSizeInMegabytes;
}
