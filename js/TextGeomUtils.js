var TextGeomMesher = ( function () {

    var alphas = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var digits = "0123456789";
    var symbols = ",./;'[]\\-=<>?:\"{}|_+~!@#$%^&*()";
    var chars = alphas + digits + symbols;

    function TextGeomMesher(material, parameters) {
        this.material = material || new THREE.MeshBasicMaterial({color: 0xff2201});
        this.geometries = {};
        this.meshes = {};
        parameters = parameters || {size: 0.2, height: 0, font: 'anonymous pro', curveSegments: 2};
        for (var i = 0; i < chars.length; i++) {
            var c = chars[i];
            var geom = new THREE.TextGeometry(c, parameters);
            var bufferGeom = new THREE.BufferGeometry();
            bufferGeom.fromGeometry(geom);
            geom.dispose();
            this.geometries[c] = bufferGeom;
            this.meshes[c] = new THREE.Mesh(geom, this.material);
        }
        var lineMeshBuffer = {};
        this.makeMesh = function (text, material) {
            material = material || this.material;
            var mesh = new THREE.Object3D();
            var lines = text.split(/\n/);
            for (var i = 0; i < lines.length; i++) {
                var line = lines[i];
                var lineMesh = lineMeshBuffer[line];
                if (lineMesh) {
                    var clone = lineMesh.clone();
                    clone.position.y = 0;
                    mesh.add(clone);
                }
                else {
                    lineMesh = new THREE.Object3D();
                    mesh.add(lineMesh);
                    lineMeshBuffer[line] = lineMesh;
                    for (var j = 0; j < line.length; j++) {
                        var c = line[j];
                        if (c !== ' ') {
                            var letterMesh = this.meshes[c].clone();
                            letterMesh.position.x = 0.8*textGeomParams.size * j;
                            lineMesh.add(letterMesh);
                        }
                    }
                }
            }
            // scroll lines:
            for (i = 0; i < mesh.children.length; i++) {
                var child = mesh.children[i];
                child.position.y = (mesh.children.length - i) * 1.6*parameters.size;
            }
            return mesh;
        }.bind(this);
    }

    return TextGeomMesher;
} )();
