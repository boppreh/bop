"ues strict";

function startListening(path) {
    new EventSource(path).onmessage = function(e) {
        var p = e.data.split(' ');
        document.getElementById(p[0]).innerHTML = decodeURIComponent(p[1]);
    }
}

var pageid = String(Math.random()).slice(2);

function call(method) {
    var data = new FormData();
    data.append('pageid', pageid);
    Array.prototype.slice.call(arguments, 1).forEach(function (elementId) {
        var value = document.getElementById(elementId).value;
        data.append(elementId, value);
    });

    var r = new XMLHttpRequest();
    r.open('POST', '/' + method, true);
    r.send(data);
}

startListening('/sse/subscribe/' + pageid);
