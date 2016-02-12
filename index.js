var app;

function onLoad() {
    "use strict";

    var rS = new rStats();

    var avatar = new THREE.Object3D();

    THREE.py.parse(THREEPY_SCENE).then( function (scene) {

        scene.add(avatar);
        app = new WebVRApplication(scene, {useWebVRBoilerplate: true});
        avatar.add(app.camera);
        app.camera.layers.enable(1);
        app.camera.layers.enable(2);
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

            lt = t;

            rS('frame').end();
            rS().update();

            requestAnimationFrame(animate);
        }

        return animate;
    };

}
