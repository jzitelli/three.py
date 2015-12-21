function setupMouse(parent, position, particleTexture, onpointerlockchange) {
    "use strict";
    position = position || new THREE.Vector3(0, 0, -2);
    var numParticles = 50;
    particleTexture = particleTexture || '/images/mouseParticle.png';
    var mouseParticleGroup = new SPE.Group({
        texture: {value: THREE.ImageUtils.loadTexture(particleTexture)},
        maxParticleCount: numParticles
    });
    var mouseParticleEmitter = new SPE.Emitter({
        maxAge: {value: 0.5},
        position: {value: new THREE.Vector3(0, 0, 0),
                   spread: new THREE.Vector3(0, 0, 0)},
        velocity: {value: new THREE.Vector3(0, 0, 0),
                   spread: new THREE.Vector3(0.4, 0.4, 0.4)},
        color: {value: [new THREE.Color('blue'), new THREE.Color('red')]},
        opacity: {value: [1, 0.1]},
        size: {value: 0.1},
        particleCount: numParticles
    });
    mouseParticleGroup.addEmitter(mouseParticleEmitter);

    var mousePointerMesh = mouseParticleGroup.mesh;

    parent.add(mousePointerMesh);
    mousePointerMesh.position.copy(position);

    // mousePointerMesh.visible = true;
    mousePointerMesh.visible = false;

    if ("onpointerlockchange" in document) {
      document.addEventListener('pointerlockchange', lockChangeAlert, false);
    } else if ("onmozpointerlockchange" in document) {
      document.addEventListener('mozpointerlockchange', lockChangeAlert, false);
    } else if ("onwebkitpointerlockchange" in document) {
      document.addEventListener('webkitpointerlockchange', lockChangeAlert, false);
    }
    function lockChangeAlert() {
        if ( document.pointerLockElement || document.mozPointerLockElement || document.webkitPointerLockElement ) {
            pyserver.log('pointer lock status is now locked');
            //mousePointerMesh.visible = true;
            if (onpointerlockchange) {
                onpointerlockchange(true);
            }
        } else {
            pyserver.log('pointer lock status is now unlocked');
            //mousePointerMesh.visible = false;
            if (onpointerlockchange) {
                onpointerlockchange(false);
            }
        }
    }

    var xMax = 2, xMin = -2,
        yMax = 1, yMin = -1;
    window.addEventListener("mousemove", function (evt) {
        if (!mousePointerMesh.visible) return;
        var dx = evt.movementX,
            dy = evt.movementY;
        if (dx) {
            mousePointerMesh.position.x += 0.0004*dx;
            mousePointerMesh.position.y -= 0.0004*dy;
            if      (mousePointerMesh.position.x > xMax) mousePointerMesh.position.x = xMax;
            else if (mousePointerMesh.position.x < xMin) mousePointerMesh.position.x = xMin;
            if      (mousePointerMesh.position.y > yMax) mousePointerMesh.position.y = yMax;
            else if (mousePointerMesh.position.y < yMin) mousePointerMesh.position.y = yMin;
        }
    });


    // function setVisible(visible) {
    //     mousePointerMesh.visible = visible;
    // }


    // var pickables,
    //     picked;
    // function setPickables(p) {
    //     pickables = p;
    // }


    // var origin = new THREE.Vector3();
    // var direction = new THREE.Vector3();
    // var raycaster = new THREE.Raycaster();
    var lt = 0;
    function animateMousePointer(t, camera) {
        var dt = 0.001*(t - lt);
        if (mousePointerMesh.visible) {
            mouseParticleGroup.tick(dt);
            // if (pickables && camera) {
            //     origin.set(0, 0, 0);
            //     direction.set(0, 0, 0);
            //     direction.subVectors(mousePointerMesh.localToWorld(direction), camera.localToWorld(origin)).normalize();
            //     raycaster.set(origin, direction);
            //     var intersects = raycaster.intersectObjects(pickables);
            //     if (intersects.length > 0) {
            //         if (picked != intersects[0].object) {
            //             if (picked) picked.material.color.setHex(picked.currentHex);
            //             picked = intersects[0].object;
            //             picked.currentHex = picked.material.color.getHex();
            //             picked.material.color.setHex(0xff4444); //0x44ff44);
            //         }
            //     } else {
            //         if (picked) picked.material.color.setHex(picked.currentHex);
            //         picked = null;
            //     }
            // }
        }
        lt = t;
    }

    // return {
    //     animateMousePointer: animateMousePointer,
    //     setPickables: setPickables,
    //     setVisible: setVisible
    // };

    return {
        animateMousePointer: animateMousePointer,
        mousePointerMesh: mousePointerMesh
    };
}
