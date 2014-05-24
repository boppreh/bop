"ues strict";

function startListening(path='/sse/subscribe') {
    new EventSource(path).onmessage = function(e) {
        var p = e.data.split(' ');
        document.getElementById(p[0]).innerHTML = decodeURIComponent(p[1]);
    }
}

function call(method) {
    var r = new XMLHttpRequest();
    r.open('POST', '/' + method, true);
    r.send();
}

startListening();
