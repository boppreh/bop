"ues strict";

var pageid = String(Math.random()).slice(2);

new EventSource('/sse/subscribe/' + pageid).onmessage = function(e) {
    console.log(e.data);
    eval(e.data);
}

function call(method /*, elements*/) {
    var data = new FormData();
    data.append('pageid', pageid);
    var i = 1;
    Array.prototype.slice.call(arguments, 1).forEach(function (elementId) {
        data.append(i++, document.getElementById(elementId).value);
    });

    var r = new XMLHttpRequest();
    r.open('POST', '/' + method, true);
    r.send(data);
}

function get(elementId) {
    var element = document.getElementById(elementId);
    if (element.value !== undefined) {
        return element.value;
    } else {
        return element.innerHTML;
    }
}

function set(elementId, value) {
    var element = document.getElementById(elementId);
    if (element.value !== undefined) {
        element.value = value;
    } else {
        element.innerHTML = value;
    }
}
