WebVRApplication = ( function () {
    function WebVRApplication(scene, config) {
        this.scene = scene;

        config = config || {};
        var rendererOptions     = config.rendererOptions || {antialias: true, alpha: true};
        var useShadowMap        = config.useShadowMap;
        var onResetVRSensor     = config.onResetVRSensor;
        var useWebVRBoilerplate = config.useWebVRBoilerplate;

        var world = config.world;
        if (!world) {
            var worldConfig = config.worldConfig || {};
            worldConfig.gravity                    = worldConfig.gravity || 9.8;
            worldConfig.contactEquationStiffness   = worldConfig.contactEquationStiffness || 1e7;
            worldConfig.frictionEquationStiffness  = worldConfig.frictionEquationStiffness || 1e7;
            worldConfig.contactEquationRelaxation  = worldConfig.contactEquationRelaxation || 3;
            worldConfig.frictionEquationRelaxation = worldConfig.frictionEquationRelaxation || 3;
            worldConfig.iterations                 = worldConfig.iterations || 8;

            world = new CANNON.World();
            world.gravity.set( 0, -worldConfig.gravity, 0 );
            world.broadphase = new CANNON.SAPBroadphase( world );
            world.defaultContactMaterial.contactEquationStiffness   = worldConfig.contactEquationStiffness;
            world.defaultContactMaterial.frictionEquationStiffness  = worldConfig.frictionEquationStiffness;
            world.defaultContactMaterial.contactEquationRelaxation  = worldConfig.contactEquationRelaxation;
            world.defaultContactMaterial.frictionEquationRelaxation = worldConfig.frictionEquationRelaxation;
            world.solver.iterations = worldConfig.iterations;
        }
        this.world = world;

        var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera = camera;

        var renderer = new THREE.WebGLRenderer(rendererOptions);
        this.renderer = renderer;
        this.renderer.setPixelRatio(window.devicePixelRatio);
        if (useShadowMap) {
            this.renderer.shadowMap.enabled = true;
            this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        }
        var domElement = this.renderer.domElement;
        document.body.appendChild(domElement);
        domElement.id = 'renderer';

        var vrEffect = new THREE.VREffect(this.renderer);
        this.vrEffect = vrEffect;
        this.vrEffect.setSize(window.innerWidth, window.innerHeight);

        this.vrControls = new THREE.VRControls(this.camera);

        if (useWebVRBoilerplate) {
            this.vrManager = new WebVRManager(this.renderer, this.vrEffect, {
                hideButton: false
            });
        } else {
            this.vrManager = ( function () {
                var mode = 0;
                var onFullscreenChange = function () {
                    vrEffect.setSize(window.innerWidth, window.innerHeight);
                };
                document.addEventListener('webkitfullscreenchange', onFullscreenChange);
                document.addEventListener('mozfullscreenchange', onFullscreenChange);
                window.addEventListener('keydown', function (evt) {
                    if (evt.keyCode === 70) { // F
                        mode = 1 - mode;
                        vrEffect.setFullScreen((mode === 1));
                    }
                });
                return {
                    isVRMode: function () {
                        return mode === 1;
                    },
                    render: function (scene, camera, t) {
                        if (mode === 1) vrEffect.render(scene, camera);
                        else renderer.render(scene, camera);
                    }
                };
            } )();
        }

        this.toggleVRControls = function () {
            if (this.vrControls.enabled) {
                this.vrControls.enabled = false;
                this.camera.position.set(0, 0, 0);
                this.camera.quaternion.set(0, 0, 0, 1);
            } else {
                this.vrControls.enabled = true;
                // this.vrControls.update();
            }
        }.bind(this);


        var lastPosition = new THREE.Vector3();
        this.resetVRSensor = function () {
            lastPosition.copy(this.camera.position);
            var lastRotation = this.camera.rotation.y;
            this.vrControls.resetSensor();
            this.vrControls.update();
            if (onResetVRSensor) {
                onResetVRSensor(lastRotation, lastPosition);
            }
        }.bind(this);


        var wireframeMaterial = new THREE.MeshBasicMaterial({color: 0xeeddaa, wireframe: true});
        this.toggleWireframe = function () {
            if (this.scene.overrideMaterial) {
                this.scene.overrideMaterial = null;
            } else {
                this.scene.overrideMaterial = wireframeMaterial;
            }
        }.bind(this);


        renderer.domElement.requestPointerLock = renderer.domElement.requestPointerLock || renderer.domElement.mozRequestPointerLock || renderer.domElement.webkitRequestPointerLock;
        function requestPointerLock() {
            if (renderer.domElement.requestPointerLock) {
                renderer.domElement.requestPointerLock();
            }
        }
        function releasePointerLock() {
            document.exitPointerLock = document.exitPointerLock || document.mozExitPointerLock || document.webkitExitPointerLock;
            if (document.exitPointerLock) {
                document.exitPointerLock();
            }
        }
        var fullscreenchange = this.renderer.domElement.mozRequestFullScreen ? 'mozfullscreenchange' : 'webkitfullscreenchange';
        document.addEventListener(fullscreenchange, function ( event ) {
            if (this.vrManager.isVRMode()) {
                this.vrControls.enabled = true;
            }
            var fullscreen = !(document.webkitFullscreenElement === null || document.mozFullScreenElement === null);
            if (!fullscreen) {
                releasePointerLock();
            } else {
                requestPointerLock();
            }
        }.bind(this));


        this.start = function(animate) {
            function waitForResources(t) {
                if (THREE.py.isLoaded()) {
                    THREE.py.CANNONize(scene, world);
                    for (var i = 0; i < 240*2; i++) {
                        world.step(1/240);
                    }
                    requestAnimationFrame(animate);
                } else {
                    requestAnimationFrame(waitForResources);
                }
            }
            waitForResources(0);
        };

    }

    return WebVRApplication;
} )();
