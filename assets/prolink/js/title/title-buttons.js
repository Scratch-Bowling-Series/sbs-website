        const remote = require('electron').remote;
        document.getElementById("t-btn-min").addEventListener("click", function (e) {
            var window = remote.getCurrentWindow();
            window.minimize();
        });
        document.getElementById("t-btn-max").addEventListener("click", function (e) {
            var window = remote.getCurrentWindow();
            if (!window.isMaximized()) {
                window.maximize();
            } else {
                window.unmaximize();
            }
        });
        document.getElementById("t-btn-close").addEventListener("click", function (e) {
            var window = remote.getCurrentWindow();
            window.close();
        });