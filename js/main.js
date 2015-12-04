var scene;
if (window.JSON_SCENE !== undefined) {
    scene = THREE.py.parse(JSON_SCENE);
} else {
    scene = new THREE.Scene();
}

var camera;
if (window.JSON_CAMERA !== undefined) {
    camera = THREE.py.parse(JSON_CAMERA);
} else {
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
}

var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

function onLoad() {
    renderer.render(scene, camera);
}
