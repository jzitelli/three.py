var scene;

var avatar = new THREE.Object3D();

var camera;
if (window.JSON_CAMERA !== undefined) {
    camera = THREE.py.parse(JSON_CAMERA);
} else {
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
}

avatar.add(camera);

var renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

var controls;
if (THREE.py.config.controls) {
    controls = new THREE[THREE.py.config.controls](avatar, renderer.domElement);
    if (THREE.py.config.controls === 'FirstPersonControls') {
        controls.lon = -90;
    }
}

var vrControls = new THREE.VRControls(camera);
var vrEffect = new THREE.VREffect(renderer);
var vrManager = new WebVRManager(renderer, vrEffect, {
    hideButton: false
});
window.addEventListener('resize', function () {
    "use strict";
    vrEffect.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});


var world = new CANNON.World();
world.gravity.set(0, -9.8, 0 );


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
        scene = THREE.py.parse(JSON_SCENE);
    } else {
        scene = new THREE.Scene();
        var textGeom = new THREE.TextGeometry("This is what you get when you don't define window.JSON_SCENE", {size: 0.3, height: 0, font: 'anonymous pro'});
        var textMaterial = new THREE.BasicMaterial({color: 0xeeeb00});
        var textMesh = new THREE.Mesh(textGeom, textMaterial);
        scene.add(textMesh);
        textMesh.position.set(-3, 2, -6);
    }

    scene.add(avatar);

    stats.setMode( 0 ); // 0: fps, 1: ms, 2: mb
    // align top-left
    stats.domElement.style.position = 'absolute';
    stats.domElement.style.left = '0px';
    stats.domElement.style.top = '0px';
    document.body.appendChild( stats.domElement );
    console.log(stats.domElement);

    var toolOptions = {};
    var toolStuff = addTool(avatar, world, toolOptions);
    leapController = toolStuff.leapController;
    animateLeap    = toolStuff.animateLeap;

    function waitForResources(t) {
        if (THREE.py.isLoaded()) {
            vrEffect.setSize(window.innerWidth, window.innerHeight);
            THREE.py.CANNONize(scene, world);
            requestAnimationFrame(animate);
        } else {
            requestAnimationFrame(waitForResources);
        }
    }
    requestAnimationFrame(waitForResources);
}


var animate = ( function () {
    "use strict";
    var lt = 0;
    var lastFrameID;
    function animate(t) {
        stats.begin();

        var dt = 0.001 * (t - lt);
        requestAnimationFrame(animate);
        world.step(1/75, dt, 10);
        if (controls) {
            controls.update(dt);
        }
        for (var i = 0; i < world.bodies.length; i++) {
            var body = world.bodies[i];
            if (body.mass > 0) {
                var mesh = body.mesh;
                if (mesh) {
                    mesh.position.copy(body.position);
                    mesh.quaternion.copy(body.quaternion);
                }
            }
        }
        vrControls.update();
        vrManager.render(scene, camera);
        var frame = leapController.frame();
        if (frame.valid && frame.id !== lastFrameID) {
            animateLeap(frame, dt);
            lastFrameID = frame.id;
        }
        lt = t;

        stats.end();
    }
    return animate;
} )();
