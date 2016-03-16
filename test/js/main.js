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


// adapted from detectmobilebrowsers.com
function isMobile() {
    "use strict";
    var a = navigator.userAgent || navigator.vendor || window.opera;
    return (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4)));
}


function onLoad() {
    "use strict";
    var testLinks = document.getElementsByClassName('testLink');

    var deskCheckbox = document.getElementById('deskCheckbox');
    deskCheckbox.addEventListener('change', function () {
        var append = "?model=test/models/vrDesk.json";
        var checked = deskCheckbox.checked;
        for (var i = 0; i < testLinks.length; i++) {
            var testLink = testLinks[i];
            if (checked) testLink.href = testLink.href + append;
            else testLink.href = testLink.href.slice(0, -append.length);
        }
    }, false);

    var rS;
    if (URL_PARAMS.rstats) {
        rS = new rStats({CSSPath: 'rstats/'});
    } else {
        var nop = function () {};
        rS = function () { return {start: nop, end: nop, frame: nop, tick: nop, update: nop}; };
    }

    var world = new CANNON.World();
    world.gravity.set( 0, -9.8, 0 );
    world.broadphase = new CANNON.SAPBroadphase( world );
    world.defaultContactMaterial.contactEquationStiffness   = 1e7;
    world.defaultContactMaterial.frictionEquationStiffness  = 1e7;
    world.defaultContactMaterial.contactEquationRelaxation  = 3;
    world.defaultContactMaterial.frictionEquationRelaxation = 3;
    world.solver.iterations = 10;

    var avatar = new THREE.Object3D();
    avatar.position.y = 3.5*12*0.0254

    var app;

    var animate = function () {
        var lt = 0;

        function animate(t) {
            rS('FPS').frame();
            rS('raF').tick();
            rS('frame').start();

            var dt = 0.001 * (t - lt);

            rS('render').start();
            app.render();
            rS('render').end();

            rS('step').start();
            world.step(Math.min(dt, 1/60), dt, 20);

            for (var i = 0; i < world.bodies.length; i++) {
                var body = world.bodies[i];
                body.mesh.position.copy(body.interpolatedPosition);
                body.mesh.quaternion.copy(body.interpolatedQuaternion);
            }
            rS('step').end();

            lt = t;

            rS('frame').end();
            rS().update();

            requestAnimationFrame(animate);
        }

        return animate;
    };

    function onSceneReady(scene) {
        scene.add(avatar);

        if (URL_PARAMS.model) {
            var url = URL_PARAMS.model;
            var objectLoader = new THREE.ObjectLoader();
            objectLoader.load(url, function (object) {
                object.scale.set(0.01, 0.01, 0.01);
                object.position.z -= 1.41;
                object.position.y = avatar.position.y - 0.73;
                scene.add(object);
            }, undefined, function (error) {
                console.error(url + ' could not be loaded: ' + JSON.stringify(error, undefined, 2));
            });
        }

        app = new WebVRApp(scene, {
            rendererOptions: {
                canvas: document.getElementById('webgl-canvas'),
                antialias: !isMobile()
            }
        });

        var shadowMapCheckbox = document.getElementById('shadowMapCheckbox');
        shadowMapCheckbox.addEventListener('change', function () {
            app.renderer.shadowMap.enabled = shadowMapCheckbox.checked;
            if (app.renderer.shadowMap.enabled) {
                app.renderer.shadowMap.needsUpdate = true;
            }
        }, false);

        if (shadowMapCheckbox.checked) {
            if (!app.renderer.shadowMap.enabled) {
                app.renderer.shadowMap.enabled = true;
            }
        }

        app.camera.layers.enable(1);
        app.camera.layers.enable(2);

        avatar.add(app.camera);

        THREE.py.CANNONize(scene, world);

        requestAnimationFrame(animate());
    }

    if (window.THREEPY_SCENE) {
        THREE.py.parse(window.THREEPY_SCENE).then( function (scene) {
            onSceneReady(scene);
        } );
    } else {
        onSceneReady(new THREE.Scene());
    }
}
