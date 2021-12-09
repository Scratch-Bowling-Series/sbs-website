var canClick = true;


var bowler_template = '<div class="t-roster-bowler preview">' +
    '<img class="t-r-bowler-image" src="/account/data/profile-pic/{0}" alt="Picture of {1} {2}">' +
    '<a class="t-r-bowler-name" href="/account/view/{0}">{1} <span class="bold">{2}</span></a>' +
    '<a href="/account/view/{0}" class="btn btn-small t-r-bowler-view">VIEW</a></div>';

var login_empty_template = '<a class="roster-msg">Be the first to join the roster!</a>' +
    '<div class="btn-bar-center">' +
    '<a class="btn btn-medium bkg-darkgreen border-bone text-white">LOGIN TO JOIN</a></div>';

var join_empty_template = '<a class="roster-msg">Be the first to join the roster!</a>' +
    '<div class="btn-bar-center">' +
    '<a class="btn btn-medium bkg-darkgreen border-none text-white join-roster" state="join">JOIN</a></div>';

var login_reg_template = '<a class="btn btn-medium bkg-none border-none text-darkgreen">${0} FEE DUE AT ENTRY</a>' +
    '<a class="btn btn-medium bkg-darkgreen border-none text-white">LOGIN TO JOIN</a>';

var join_reg_template = '<a class="btn btn-medium bkg-none border-none text-darkgreen">${0} FEE DUE AT ENTRY</a>' +
    '<a class="btn btn-medium bkg-darkgreen border-none text-white join-roster" state="join">JOIN</a>';

var leave_reg_template = '<a class="btn btn-medium bkg-none border-none text-darkgreen">${0} FEE DUE AT ENTRY</a>' +
    '<a class="btn btn-medium bkg-darkgreen border-none text-white join-roster" state="leave">LEAVE</a>';

$(document).ready(function(){
    var tournament_id = $('.t-roster').attr('tournamentId');
    if(tournament_id){
        var join_roster_url = '/tournaments/roster/join/' + tournament_id
        var leave_roster_url = '/tournaments/roster/leave/' + tournament_id
        var get_roster_url = '/tournaments/roster/get/' + tournament_id

        if($('.t-roster-bowler').length > 0){
            console.log('getting roster data');
            getRosterData(get_roster_url);
        }
    }
    registerSingleTournamentListeners();
});

function registerSingleTournamentListeners(){
    $('.join-roster').click(function(){
        var request_url = '';
        var button = $(this);
        if(button.attr('state') === 'join'){
            request_url = $(this).attr('join-roster');
        }else{
            request_url = $(this).attr('leave-roster');
        }
        $.get(request_url).done(function(data){
            if(data.success != null && data.success === true){
                if(data.onRoster === true){
                    button.attr('state', 'leave');
                    button.text('LEAVE');
                }
                else{
                    button.attr('state', 'join');
                    button.text('JOIN');
                }
                updateRosterViewport(data.rosterData);
            }
        });
    });
}

function getRosterData(request_url){
    $.get(request_url).done(function(data){
        if(data.success != null && data.success === true){
            if(data.rosterData){
                updateRosterViewport(data.rosterData);
            }
        }
    });
}

function updateRosterViewport(rosterData){
    var container = $('.t-roster');

    container.text('');
    if(rosterData.length > 0){
        $.each(rosterData, function(index, data){
            var user_id = data[0];
            var first_name = data[1];
            var last_name = data[2];
            var output = bowler_template.format(user_id, first_name, last_name);
            container.append(output);
        });
        $('.t-roster-bowler').removeClass('preview');
        $('.roster-btns').removeClass('empty');
    }
    else{
        $('.roster-btns').addClass('empty');
    }

}



//<editor-fold desc="HELPFUL FUNCTIONS">

// Format String
if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}

// Get Time Since DateTime
function timeSince(date) {

    var seconds = Math.floor((new Date() - date) / 1000);

    var interval = seconds / 31536000;

    if (interval > 1) {
        return Math.floor(interval) + "y";
    }
    interval = seconds / 604800;
    if (interval > 1) {
        return Math.floor(interval) + "w";
    }
    interval = seconds / 86400;
    if (interval > 1) {
        return Math.floor(interval) + "d";
    }
    interval = seconds / 3600;
    if (interval > 1) {
        return Math.floor(interval) + "h";
    }
    interval = seconds / 60;
    if (interval > 1) {
        return Math.floor(interval) + "m";
    }
    return Math.floor(seconds) + "s";
}

function canClickAgain(){
    if(canClick){
        canClick = false;
        setTimeout(function (){
            canClick = true;
        },500)
        return true;
    }
    return false;
}

// Number Formatter
function nFormatter(num, digits) {
    num = parseInt(num);
    var si = [
        { value: 1, symbol: "" },
        { value: 1E3, symbol: "k" },
        { value: 1E6, symbol: "m" },
        { value: 1E9, symbol: "g" },
        { value: 1E12, symbol: "t" },
        { value: 1E15, symbol: "p" },
        { value: 1E18, symbol: "e" }
    ];
    var rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
    var i;
    for (i = si.length - 1; i > 0; i--) {
        if (num >= si[i].value) {
            break;
        }
    }
    return (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol;
}

//</editor-fold>