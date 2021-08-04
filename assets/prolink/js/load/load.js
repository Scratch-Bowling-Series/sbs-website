const fs = require('fs')
const { ipcRenderer, remote } = require('electron');
const app = remote.app;

$(document).ready(function() {
    Load();

    function Load()
    {
        $('#inner').css('width', '0%');
        LoadBowlers();
    }


    function LoadBowlers()
    {
        SetLoadText('Requesting all bowlers.');
        SetLoadPercentage(12.5);

        //  Load Operation
        var timeout_min = 1;
        url = 'bowlers/';
        $.ajax({
          dataType: "json",
          url: url,
          timeout: 60000 * timeout_min,
          success: function(data){
            SetLoadText('Storing all bowlers.');
            StoreJsonData('bowlers_cache.dat', JSON.stringify(data));
            setTimeout(function()
            {
                SetLoadPercentage(25);
                LoadPatterns();
            },2000);
          },
          error: function(err)
          {
              ipcRenderer.send('syncError');
          }
        });
    }
    function LoadPatterns()
    {
        SetLoadText('Requesting all oil patterns.');
        SetLoadPercentage(37.5);
        //  Load Operation
        var timeout_min = 1;
        url = 'patterns/';
        $.ajax({
          dataType: "json",
          url: url,
          timeout: 60000 * timeout_min,
          success: function(data){
            SetLoadText('Storing all oil patterns.');
            StoreJsonData('patterns_cache.dat', JSON.stringify(data));
            setTimeout(function()
            {
                SetLoadPercentage(50);
                LoadTournaments();
            },2000);
          },
          error: function(err)
          {
              ipcRenderer.send('syncError');
          }
        });
    }
    function LoadTournaments()
    {
        SetLoadText('Requesting all tournaments.');
        SetLoadPercentage(62.5);
        //  Load Operation
        var timeout_min = 1;
        url = 'tournaments/';
        $.ajax({
          dataType: "json",
          url: url,
          timeout: 60000 * timeout_min,
          success: function(data){
            SetLoadText('Storing all tournaments.');
            StoreJsonData('tournaments_cache.dat', JSON.stringify(data));
            setTimeout(function()
            {
                SetLoadPercentage(75);
                LoadCenters();
            },2000);
          },
          error: function(err)
          {
              ipcRenderer.send('syncError');
          }
        });
    }
    function LoadCenters()
    {
        SetLoadText('Requesting all centers.');
        SetLoadPercentage(87.5);
        //  Load Operation
        var timeout_min = 1;
        url = 'centers/';
        $.ajax({
          dataType: "json",
          url: url,
          timeout: 60000 * timeout_min,
          success: function(data){
            SetLoadText('Storing all centers.');
            StoreJsonData('centers_cache.dat', JSON.stringify(data));
            setTimeout(function()
            {
                SetLoadPercentage(100);
                setTimeout(function()
                {
                    SetLoadText('Master Sync Complete');
                    LoadMainWindow();
                },2000);
            },2000);
          },
          error: function(err)
          {
              ipcRenderer.send('syncError');
          }
        });
    }

    function SetLoadText(value)
    {

        $('#load-container a').text(value);
    }
    function SetLoadPercentage(value)
    {

        $('#inner').css('width', value + '%');
    }
    function LoadMainWindow()
    {

        ipcRenderer.send('mainWindow');
        ipcRenderer.send('syncDone');
    }

    function GetCacheData(dataName)
    {
        var timeout_min = 1;
        url = dataName + '/';
        $.ajax({
          dataType: "json",
          url: url,
          timeout: 60000 * timeout_min,
          success: function(data){
            console.log('RECIEVED DATA: ' + data.length);
            return data;
          }
        });
    }


    function ReadJsonData(fileName)
    {
        fileName = app.getPath("userData") + "/" + fileName;
        fs.readFile(fileName, 'utf8' , (err, data) => {
            if (err) {
                return false;
            }
            return data;
        });
    }
    function StoreJsonData(fileName, data)
    {
        if(data != null)
        {
            fileName = app.getPath("userData") + "/" + fileName;
            fs.writeFile(fileName, data, err => {
              if (err) {
                return false;
              }
              return true;
            });
        }
    }
});