$(document).ready(function()
{
    var prevData = '';
    var proto = 'https';
    if (location.protocol !== 'https:') {
                proto = 'http';
            }
    setInterval(function()
    {
        $.ajax(
        {



            type: "GET",
            url: proto + "://scratchbowling.pythonanywhere.com/get-last-commit",
            contentType: "text/plain",
            dataType: "text",
            success: function (data) {
                if(data != prevData)
                {
                    if (prevData != '')
                    {
                        Refresh();
                    }
                    prevData = data;
                }
            }
        });
    }, 1000);

    function Refresh()
    {
        location.reload();
    }
});