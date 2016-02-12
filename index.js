
function onLoad() {
    "use strict";

    var rS = new rStats();

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

        app = new WebVRApplication(scene);

        avatar.add(app.camera);

        app.camera.layers.enable(1);
        app.camera.layers.enable(2);

        THREE.py.CANNONize(scene, world);

        var objectLoader = new THREE.ObjectLoader();
        objectLoader.load('models/vrDesk.json', function (object) {
            object.scale.set(0.01, 0.01, 0.01);
            object.position.z -= 1.41;
            object.position.y -= 0.83;
            scene.add(object);
        }, undefined, function (err) {
            pyserver.log('vrDesk.json could not be loaded: ' + JSON.stringify(err, undefined, 2));
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

            app.vrControls.update();
            app.vrManager.render(app.scene, app.camera, t);

            world.step(1/60, dt, 5);
            world.bodies.forEach( function (body) {
                body.mesh.position.copy(body.interpolatedPosition);
                body.mesh.quaternion.copy(body.interpolatedQuaternion);
            } );

            lt = t;

            rS('frame').end();
            rS().update();

            requestAnimationFrame(animate);
        }

        return animate;
    };

}
