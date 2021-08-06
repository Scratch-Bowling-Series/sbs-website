const { ipcRenderer } = require('electron');

$(document).ready(function()
{
    CheckForUpdate();
});

function CheckForUpdate() {
    $('#updater-load').css('opacity', '1');
}
function UpdateFound() {
    $('#updater-done').css('opacity', '1');
    $('#updater-load').css('opacity', '0');
    $('#updater-text').text('UPDATE FOUND');
    setTimeout(function()
    {
        $('#updater-text').text('DOWNLOADING UPDATE');
    }, 1000);
}
function UpdateDownloaded() {
    $('#updater-text').text('UPDATE DOWNLOADED');
    setTimeout(function()
    {
        $('#updater-text').text('STARTING UPDATE');
        setTimeout(function ()
        {
            ipcRenderer.send('QuitInstallUpdate');
        }, 1000);
    }, 1000);
}
function NoUpdates() {
    $('#updater-text').text('VERSION IS CURRENT');
    setTimeout(function()
    {
        location.href = '/prolink/login/';
    }, 1000);
}

ipcRenderer.on('UpdateFound', function()
{
    UpdateFound();
});
ipcRenderer.on('Error', function()
{
    NoUpdates();
});
ipcRenderer.on('NoUpdate', function()
{
    NoUpdates();
});
ipcRenderer.on('Downloaded', function()
{
    UpdateDownloaded();
});

