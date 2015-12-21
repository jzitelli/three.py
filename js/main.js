var app;
var avatar = new THREE.Object3D();
var scene;
var controls;
if (THREE.py.config.controls) {
    controls = new THREE[THREE.py.config.controls](avatar, renderer.domElement);
    if (THREE.py.config.controls === 'FirstPersonControls') {
        controls.lon = -90;
    }
}

var stats;
var leapController,
    animateLeap;

function onLoad() {
    "use strict";
    pyserver.log('THREE.REVISION = ' + THREE.REVISION);

    stats = new Stats();

    if (window.extractShaderLib) {
        extractShaderLib();
    }

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

    app = new WebVRApplication(scene);

    var mouseStuff = setupMouse(avatar);
    var animateMousePointer = mouseStuff.animateMousePointer;

    stats.setMode( 0 ); // 0: fps, 1: ms, 2: mb
    // align top-left
    stats.domElement.style.position = 'absolute';
    stats.domElement.style.left = '0px';
    stats.domElement.style.top = '0px';
    document.body.appendChild( stats.domElement );

    var toolOptions = {};
    var toolStuff = addTool(avatar, app.world, toolOptions);
    leapController = toolStuff.leapController;
    animateLeap    = toolStuff.animateLeap;

    app.start(animate(animateMousePointer));
}


var animate = function (animateMousePointer) {
    "use strict";
    var lt = 0;
    var lastFrameID;
    function animate(t) {
        stats.begin();

        var dt = 0.001 * (t - lt);
        requestAnimationFrame(animate);
        app.world.step(1/75, dt, 10);
        if (controls) {
            controls.update(dt);
        }
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
        var frame = leapController.frame();
        if (frame.valid && frame.id !== lastFrameID) {
            animateLeap(frame, dt);
            lastFrameID = frame.id;
        }

        animateMousePointer(t);

        lt = t;

        stats.end();
    }
    return animate;
};
