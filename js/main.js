var scene;

var camera;
if (window.JSON_CAMERA !== undefined) {
    camera = THREE.py.parse(JSON_CAMERA);
} else {
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
}

var renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

window.addEventListener('resize', function () {
    "use strict";
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.render(scene, camera);
});


var world = new CANNON.World();

function onLoad() {
    "use strict";
    pyserver.log('THREE.REVISION = ' + THREE.REVISION);

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

    THREE.py.CANNONize(scene, world);
    // world.addEventListener("postStep", function () {
    //     this.position.copy(this.body.position);
    //     var ballNum = this.body.ballNum;
    //     var stripeMesh = ballStripeMeshes[ballNum];
    //     if (stripeMesh !== undefined) {
    //         stripeMesh.quaternion.copy(this.body.quaternion);
    //     }
    // }.bind(mesh));

    requestAnimationFrame(animate);
}


var animate = ( function () {
    "use strict";
    var lt = 0;
    function animate(t) {
        var dt = 0.001 * (t - lt);
        requestAnimationFrame(animate);
        world.step(dt, 75, 10);
        renderer.render(scene, camera);
        lt = t;
    }
    return animate;
} )();
