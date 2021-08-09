$(document).ready(function()
{
    var prevData = '';
    setInterval(function()
    {
        $.ajax(
        {
            type: "GET",
            url: "http://scratchbowling.pythonanywhere.com/get-last-commit",
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