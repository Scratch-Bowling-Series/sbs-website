const { ipcRenderer } = require('electron');

$(document).ready(function()
{
  var syncing = false;

  $('#con-ping').click(function ()
  {
    StartSync();
  });
  $('#con-ping-icon').click(function ()
  {
    StartSync();
  });

  function StartSync()
  {
    if(syncing){return;}
    syncing = true;
    StyleLoading();
    ipcRenderer.send('loadMin');
  }


  ipcRenderer.on('syncDone', function()
  {
    StyleRegular();
  });
  ipcRenderer.on('syncError', function()
  {
    StyleError();
    setTimeout(function ()
    {
      StyleRegular();
    }, 5000);
  });


  function StyleLoading()
  {
    $('#con-ping').html('SYNCING');
    $('#con-ping-icon').css('color','#9d9fa1');
    $('#con-ping-icon').removeClass('fa-circle');
    $('#con-ping-icon').addClass('fa-sync-alt');
    $('#con-ping-icon').css('font-size', '10px');
    $('#con-ping-icon').css('padding', '2px 2px 2px 2px');
    $('#con-ping-icon').css('transition', 'transform linear 20s');
    $('#con-ping-icon').css('transform', 'rotate(10000deg)');
  }
  function  StyleRegular()
  {
    $('#con-ping').html('SYNC');
    $('#con-ping-icon').css('color','#9d9fa1');
    $('#con-ping-icon').css('transition', 'none');
    $('#con-ping-icon').css('font-size', '6px');
    $('#con-ping-icon').css('padding', '3px 3px 1px 1px');
    $('#con-ping-icon').removeClass('fa-sync-alt');
    $('#con-ping-icon').addClass('fa-circle');
  }
  function StyleError() {
    $('#con-ping').html('ERROR');
    $('#con-ping-icon').removeClass('fa-sync-alt');
    $('#con-ping-icon').addClass('fa-circle');
    $('#con-ping-icon').css('color', 'red');
    $('#con-ping-icon').css('transition', 'none');
    $('#con-ping-icon').css('font-size', '6px');
    $('#con-ping-icon').css('padding', '3px 3px 1px 1px');
  }


});