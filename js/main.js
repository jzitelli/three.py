var app;
var avatar = new THREE.Object3D();
var scene;

var stats;

function onLoad() {
    "use strict";
    stats = new Stats();

    THREE.py.extractShaderLib();

    if (window.JSON_SCENE !== undefined) {
        scene = THREE.py.parse(JSON_SCENE, undefined);
    } else {
        scene = new THREE.Scene();
        var textGeom = new THREE.TextGeometry("This is what you get when you don't define window.JSON_SCENE", {size: 0.3, height: 0, font: 'anonymous pro'});
        var textMaterial = new THREE.BasicMaterial({color: 0xeeeb00});
        var textMesh = new THREE.Mesh(textGeom, textMaterial);
        scene.add(textMesh);
        textMesh.position.set(-3, 2, -6);
    }

    scene.add(avatar);

    app = new WebVRApplication(scene, {useWebVRBoilerplate: true});
    
    avatar.add(app.camera);

    stats.setMode( 0 ); // 0: fps, 1: ms, 2: mb
    // align top-left
    stats.domElement.style.position = 'absolute';
    stats.domElement.style.left = '0px';
    stats.domElement.style.top = '0px';
    document.body.appendChild( stats.domElement );

    app.start(animate());
}


var animate = function () {
    "use strict";
    var lt = 0;
    function animate(t) {
        stats.begin();

        requestAnimationFrame(animate);

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

        stats.end();
    }
    return animate;
};
