"ues strict";

// http://stackoverflow.com/questions/5639346/
(function(){
    var cookies;

    function readCookie(name,c,C,i){
        if(cookies){ return cookies[name]; }

        c = document.cookie.split('; ');
        cookies = {};

        for(i=c.length-1; i>=0; i--){
           C = c[i].split('=');
           cookies[C[0]] = C[1];
        }

        return cookies[name];
    }

    window.readCookie = readCookie;
})();


var pageid = window.readCookie('pageid') || String(Math.random()).slice(2);

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
    r.open('POST', '/call/' + method, true);
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
