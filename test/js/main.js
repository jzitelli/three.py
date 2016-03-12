function onLoad() {
    "use strict";

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
    avatar.position.y = 4*12*0.0254

    var app;

    THREE.py.parse(THREEPY_SCENE).then( function (scene) {

        scene.add(avatar);

        app = new WebVRApplication(scene, {
            canvasId: 'webgl-canvas',
            rendererOptions: {antialias: !isMobile()}
        });

        avatar.add(app.camera);

        app.camera.layers.enable(1);
        app.camera.layers.enable(2);

        THREE.py.CANNONize(scene, world);

        if (URL_PARAMS.model) {
            var url = URL_PARAMS.model
            var objectLoader = new THREE.ObjectLoader();
            objectLoader.load(url, function (object) {
                object.scale.set(0.01, 0.01, 0.01);
                object.position.z -= 1.41;
                object.position.y = avatar.position.y - 0.85;
                scene.add(object);
            }, undefined, function (err) {
                console.error(url + ' could not be loaded: ' + JSON.stringify(err, undefined, 2));
            });
        }

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
