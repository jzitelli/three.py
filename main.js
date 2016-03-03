function WebVRApplication(scene, config) {
    "use strict";
    this.scene = scene;

    config = config || {};
    var rendererOptions     = config.rendererOptions;
    var onResetVRSensor     = config.onResetVRSensor;

    var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.camera = camera;

    this.renderer = new THREE.WebGLRenderer(rendererOptions);
    this.renderer.setPixelRatio(window.devicePixelRatio);

    var domElement = this.renderer.domElement;
    document.body.appendChild(domElement);
    domElement.id = 'renderer';

    this.vrEffect = new THREE.VREffect(this.renderer, function(error) { console.error('error creating VREffect: ' + error); });
    this.vrEffect.setSize(window.innerWidth, window.innerHeight);

    this.vrControls = new THREE.VRControls(this.camera, function(error) { console.error('error creating VRControls: ' + error); });

    this.vrManager = new WebVRManager(this.renderer, this.vrEffect, {hideButton: false});


    this.render = function () {
        this.vrControls.update();
        this.vrManager.render(this.scene, this.camera);
    }.bind(this);


    var wireframeMaterial = new THREE.MeshBasicMaterial({color: 0xeeddaa, wireframe: true});
    this.toggleWireframe = function () {
        if (this.scene.overrideMaterial) {
            this.scene.overrideMaterial = null;
        } else {
            this.scene.overrideMaterial = wireframeMaterial;
        }
    }.bind(this);
}


function onLoad() {
    "use strict";

    var rS = new rStats({CSSPath: 'rstats/'});

    var world = new CANNON.World();
    world.gravity.set( 0, -9.8, 0 );
    //world.broadphase = new CANNON.SAPBroadphase( world );
    world.defaultContactMaterial.contactEquationStiffness   = 1e6;
    world.defaultContactMaterial.frictionEquationStiffness  = 1e6;
    world.defaultContactMaterial.contactEquationRelaxation  = 3;
    world.defaultContactMaterial.frictionEquationRelaxation = 3;
    world.solver.iterations = 9;

    var avatar = new THREE.Object3D();

    var app;

    THREE.py.parse(THREEPY_SCENE).then( function (scene) {

        scene.add(avatar);

        app = new WebVRApplication(scene, {rendererOptions: {antialias: !isMobile()}});

        avatar.add(app.camera);

        app.camera.layers.enable(1);
        app.camera.layers.enable(2);

        THREE.py.CANNONize(scene, world);

        var objectLoader = new THREE.ObjectLoader();
        objectLoader.load('models/vrDesk.json', function (object) {
            object.scale.set(0.01, 0.01, 0.01);
            object.position.z -= 1.41;
            object.position.y -= 0.85;
            scene.add(object);
        }, undefined, function (err) {
            console.log('vrDesk.json could not be loaded: ' + JSON.stringify(err, undefined, 2));
        });

        requestAnimationFrame(animate());

    } );

    var animate = function () {
        var lt = 0;

        function animate(t) {
            rS('frame').start();
            rS('raF').tick();
            rS('FPS').frame();

            var dt = 0.001 * (t - lt);

            app.render();

            world.step(Math.min(dt, 1/60), dt, 10);

            for (var i = 0; i < world.bodies.length; i++) {
                var body = world.bodies[i];
                body.mesh.position.copy(body.interpolatedPosition);
                body.mesh.quaternion.copy(body.interpolatedQuaternion);
            }

            lt = t;

            rS('frame').end();
            rS().update();

            requestAnimationFrame(animate);
        }

        return animate;
    };

}
