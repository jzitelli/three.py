var TextGeomUtils = ( function () {
    "use strict";
    const alphas  = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const digits  = "0123456789";
    const symbols = ",./;'[]\\-=<>?:\"{}|_+~!@#$%^&*()";
    const chars   = alphas + digits + symbols;

    function TextGeomCacher(font, options) {
        options = options || {};
        var textGeomParams = {
            font:          font,
            size:          options.size || 0.12,
            height:        options.height || 0,
            curveSegments: options.curveSegments || 2
        };

        this.geometries = {};
        for (var i = 0; i < chars.length; i++) {
            var c = chars[i];
            var geom = new THREE.TextGeometry(c, textGeomParams);
            var bufferGeom = new THREE.BufferGeometry();
            bufferGeom.fromGeometry(geom);
            geom.dispose();
            this.geometries[c] = bufferGeom;
        }

        this.makeObject = function (text, material) {
            var object = new THREE.Object3D();
            for (var j = 0; j < text.length; j++) {
                var c = text[j];
                if (c !== ' ') {
                    var mesh = new THREE.Mesh(this.geometries[c], material);
                    mesh.position.x = 0.8*textGeomParams.size * j;
                    object.add(mesh);
                }
            }
            return object;
        }.bind(this);
    }

    function TextGeomLogger(textGeomCacher, material, nrows, ncols) {
        material = material || new THREE.MeshBasicMaterial({color: 0xff2201});
        nrows = nrows || 20;
        ncols = ncols || 30;

        var lineObjects = {};

        this.root = new THREE.Object3D();

        this.log = function (msg) {
            var lines = msg.split(/\n/);
            // create / clone lines:
            for (var i = 0; i < lines.length; i++) {
                var line = lines[i];
                var lineObject = lineObjects[line];
                if (lineObject) {
                    var clone = lineObject.clone();
                    clone.position.y = 0;
                    this.root.add(clone);
                } else {
                    lineObject = textGeomCacher.makeObject(line, material);
                    this.root.add(lineObject);
                    lineObjects[line] = lineObject;
                }
            }
            // remove rows exceeding max display
            var toRemove = [];
            for (i = lines.length - 1; i < this.root.children.length - nrows; i++) {
                toRemove.push(this.root.children[i]);
            }
            for (i = 0; i < toRemove.length; i++) {
                this.root.remove(toRemove[i]);
            }
            // scroll lines:
            for (i = 0; i < this.root.children.length; i++) {
                var child = this.root.children[i];
                child.position.y = (this.root.children.length - i) * 1.6*textGeomParams.size;
            }
        }.bind(this);

        this.clear = function () {
            var toRemove = [];
            for (var i = 0; i < this.root.children.length; i++) {
                toRemove.push(this.root.children[i]);
            }
            for (i = 0; i < toRemove.length; i++) {
                this.root.remove(toRemove[i]);
            }
        }.bind(this);
    }

    return {
        TextGeomCacher: TextGeomCacher,
        TextGeomLogger: TextGeomLogger
    };

} )();
