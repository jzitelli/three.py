var app;
var avatar = new THREE.Object3D();
var scene;

var rS = new rStats();

function onLoad() {
    "use strict";
    THREE.py.extractShaderLib();

    if (window.JSON_SCENE !== undefined) {
        scene = THREE.py.parse(JSON_SCENE, undefined);
    } else {
        scene = new THREE.Scene();
        var textGeom = new THREE.TextGeometry("This is what you get when you don't define window.JSON_SCENE", {size: 0.3, height: 0, font: THREE.py.fonts.helvetiker});
        var textMaterial = new THREE.BasicMaterial({color: 0xeeeb00});
        var textMesh = new THREE.Mesh(textGeom, textMaterial);
        scene.add(textMesh);
        textMesh.position.set(-3, 2, -6);
    }

    scene.add(avatar);

    app = new WebVRApplication(scene, {useWebVRBoilerplate: true});
    
    avatar.add(app.camera);

    var objectLoader = new THREE.ObjectLoader();
    objectLoader.load('models/vrDesk.json', function (object) {
        object.scale.set(0.01, 0.01, 0.01);
        object.position.z -= 1.41;
        object.position.y -= 0.83;
        scene.add(object);
    }, undefined, function (err) {
        pyserver.log('vrDesk.json could not be loaded: ' + JSON.stringify(err, undefined, 2));
    });

    app.start(animate());
}


var animate = function () {
    "use strict";
    var lt = 0;

    function animate(t) {
        rS('frame').start();
        rS('raF').tick();
        rS('FPS').frame();

        var dt = 0.001 * (t - lt);
        app.world.step(1/75, dt, 10);
        for (var i = 0; i < app.world.bodies.length; i++) {
            var body = app.world.bodies[i];
            if (body.mass > 0) {
                var mesh = body.mesh;
                if (mesh) {
                    mesh.position.copy(body.position);
                    mesh.quaternion.copy(body.quaternion);
                }
            }
        }
        app.vrControls.update();
        app.vrManager.render(scene, app.camera, t);

        lt = t;

        rS('frame').end();
        rS().update();

        requestAnimationFrame(animate);
    }

    return animate;
};
