function WebVRApplication(scene, config) {
    this.scene = scene;

    config = config || {};
    var rendererOptions     = config.rendererOptions || {antialias: true, alpha: true};
    var onResetVRSensor     = config.onResetVRSensor;
    var useWebVRBoilerplate = config.useWebVRBoilerplate;

    var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.camera = camera;

    var renderer = new THREE.WebGLRenderer(rendererOptions);
    this.renderer = renderer;
    this.renderer.setPixelRatio(window.devicePixelRatio);

    var domElement = this.renderer.domElement;
    document.body.appendChild(domElement);
    domElement.id = 'renderer';

    var vrEffect = new THREE.VREffect(this.renderer, function(errorMsg) { console.log('error creating VREffect: ' + errorMsg); });
    this.vrEffect = vrEffect;
    this.vrEffect.setSize(window.innerWidth, window.innerHeight);

    this.vrControls = new THREE.VRControls(this.camera, function(errorMsg) { console.log('error creating VRControls: ' + errorMsg); });
    this.vrControls.enabled = true;

    if (useWebVRBoilerplate) {

        this.vrManager = new WebVRManager(this.renderer, this.vrEffect, {
            hideButton: false
        });

        this.enterVR = function () {};

    } else {

        // bare bones webvr-manager, suitable for desktop VR devices

        var vrMode = 0;

        window.addEventListener("resize", function () {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            vrEffect.setSize(window.innerWidth, window.innerHeight);
        });

        this.enterVR = function () {
            if (vrMode === 0) {
                this.vrEffect.setFullScreen(true);
            }
        }.bind(this);

        this.vrManager = ( function () {
            var onFullscreenChange = function () {
                if (vrMode === 0) {
                    vrMode = 1;
                    vrEffect.setSize(window.innerWidth, window.innerHeight);
                } else {
                    vrMode = 0;
                }
            };
            document.addEventListener('webkitfullscreenchange', onFullscreenChange);
            document.addEventListener('mozfullscreenchange', onFullscreenChange);
            return {
                isVRMode: function () {
                    return vrMode === 1;
                },
                render: function (scene, camera, t) {
                    if (vrMode === 1) vrEffect.render(scene, camera);
                    else renderer.render(scene, camera);
                }
            };
        }.bind(this) )();

        this.enterFullscreen = function () {
            // Primrose function:
            function requestFullScreen ( elem, vrDisplay ) {
                var fullScreenParam;
                // if ( window.HMDVRDevice && vrDisplay && vrDisplay instanceof HMDVRDevice) {
                //     fullScreenParam = {vrDisplay: vrDisplay};
                // }
                if ( elem.webkitRequestFullscreen && fullScreenParam ) {
                    elem.webkitRequestFullscreen( fullScreenParam );
                }
                else if ( elem.webkitRequestFullscreen && !fullScreenParam ) {
                    elem.webkitRequestFullscreen( window.Element.ALLOW_KEYBOARD_INPUT );
                }
                else if ( elem.mozRequestFullScreen && fullScreenParam ) {
                    elem.mozRequestFullScreen( fullScreenParam );
                }
                else if ( elem.mozRequestFullScreen && !fullScreenParam ) {
                    elem.mozRequestFullScreen( );
                }
                else if ( elem.requestFullscreen ) {
                    elem.requestFullscreen();
                }
                else if ( elem.msRequestFullscreen ) {
                    elem.msRequestFullscreen();
                }
            }
            requestFullScreen(domElement);
        };

    }


    this.toggleVRControls = function () {
        if (this.vrControls.enabled) {
            this.vrControls.enabled = false;
            this.camera.position.set(0, 0, 0);
            this.camera.quaternion.set(0, 0, 0, 1);
        } else {
            this.vrControls.enabled = true;
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
                requestAnimationFrame(animate);
            } else {
                requestAnimationFrame(waitForResources);
            }
        }
        waitForResources(0);
    };

}
