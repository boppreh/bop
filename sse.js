"ues strict";

function startListeningForChanges(path='subscribe') {
    new EventSource(path).onmessage = function(e) {
        var p = e.data.split(' ');
        document.getElementById(p[0]).innerHTML = decodeURIComponent(p[1]);
    }
}

function post(url) {
    var request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.send();
}

startListeningForChanges();
