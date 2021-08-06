const { remote, ipcRenderer } = require('electron');
const fs = require('fs');
const app = remote.app;



ReadRememberFile();
document.login.username.spellcheck = false;
document.login.password.spellcheck = false;


var rememberOnLogin = false;

function ReadRememberFile()
{
    var fileName = app.getPath("userData") + "/user_login.data";
    fs.readFile(fileName, 'utf8' , (err, data) => {
        if (err) {
            throw err;
        }
        data = data.split(',');
        email = data[0];
        password = data[1];
        document.login.username.value = email;
        document.login.password.value = password;
        if(email != null && password != null)
        {
            document.login.remember.checked = true;
        }
    });
}

document.login.remember.addEventListener("click",function()
{
    rememberOnLogin = document.login.remember.checked;
    if(rememberOnLogin)
    {
        UpdateRememberFile();
    }
});

document.login.username.addEventListener("keyup",function()
{
    if(rememberOnLogin)
    {
        UpdateRememberFile();
    }
});
document.login.password.addEventListener("keyup",function()
{
    if(rememberOnLogin)
    {
        UpdateRememberFile();
    }
});

function UpdateRememberFile()
{
    email = document.login.username.value;
    password = document.login.password.value;
    var fileName = app.getPath("userData") + "/user_login.data";
    var content = email + ',' + password;
    fs.writeFile(fileName, content, err => {
      if (err) {
        console.error(err);
        return
      }
      console.log('Wrote to Save: ' + email + ' ' + password);
    })
}

function OpenMainWindow()
{

    ipcRenderer.send('loadWindow');
}