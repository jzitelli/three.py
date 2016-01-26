var URL_PARAMS = (function () {
    "use strict";
    var params = {};
    location.search.substr(1).split("&").forEach( function(item) {
        var k = item.split("=")[0],
            v = decodeURIComponent(item.split("=")[1]);
        if (k in params) {
            params[k].push(v);
        } else {
            params[k] = [v];
        }
    } );
    for (var k in params) {
        if (params[k].length === 1)
            params[k] = params[k][0];
        if (params[k] === 'true')
            params[k] = true;
        else if (params[k] === 'false')
            params[k] = false;
    }
    return params;
})();


function combineObjects(a, b) {
    "use strict";
    var c = {},
        k;
    for (k in a) {
        c[k] = a[k];
    }
    for (k in b) {
        if (!c.hasOwnProperty(k)) {
            c[k] = b[k];
        }
    }
    return c;
}


function makeObjectArray(obj, keyKey) {
    "use strict";
    keyKey = keyKey || "key";
    return Object.keys(obj).map(function (k) {
        var item = {};
        item[keyKey] = k;
        for (var p in obj[k]) {
            item[p] = obj[k][p];
        }
        return item;
    });
}
