var scene;
if (window.JSON_SCENE !== undefined) {
    scene = THREE.py.parse(JSON_SCENE);
} else {
    scene = new THREE.Scene();
    textGeom = new THREE.TextGeometry("This is what you get when you don't define window.JSON_SCENE", {size: 0.3, height: 0, font: 'anonymous pro'});
    textMaterial = new THREE.BasicMaterial({color: 0xeeeb00});
    textMesh = new THREE.Mesh(textGeom, textMaterial);
}

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


function onLoad() {
    "use strict";
    pyserver.log('THREE.REVISION = ' + THREE.REVISION);

    renderer.render(scene, camera);
    extractShaderLib();
}
