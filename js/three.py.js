THREE.py = ( function () {
    "use strict";
    var manager = new THREE.LoadingManager();
    var isLoaded_ = true;
    manager.onLoad = function () {
        isLoaded_ = true;
    };
    var objectLoader = new THREE.ObjectLoader(manager),
        imageLoader = new THREE.ImageLoader(manager),
        textureLoader = new THREE.TextureLoader(manager),
        cubeTextureLoader = new THREE.CubeTextureLoader(manager);

    function isLoaded() {
        return isLoaded_;
    }

    function load(url, onLoad) {
        // TODO:
    }


    function parse(json, texturePath) {
        if (texturePath) {
            objectLoader.setTexturePath(texturePath);
        }
        // TODO: convert all to BufferGeometry?
        function onLoad(obj) {
            obj.traverse( function (node) {
                if (node instanceof THREE.Mesh) {
                    node.geometry.computeBoundingSphere();
                    node.geometry.computeBoundingBox();
                    if (node.userData && node.userData.visible === false) {
                        node.visible = false;
                    }
                    if (!(node.geometry instanceof THREE.SphereBufferGeometry)) {
                        // makes seams appear on spherebuffergeometries due to doubled vertices at phi=0=2*pi
                        node.geometry.computeVertexNormals();
                    }
                    if (node.material.shading === THREE.FlatShading)
                        node.geometry.computeFaceNormals();
                }
            } );
            loadHeightfields(obj);
        }
        if (json.materials) {
            json.materials.forEach( function (mat) {
                if (mat.type.endsWith("ShaderMaterial") && mat.uniforms) {
                    var uniforms = mat.uniforms;
                    for (var key in uniforms) {
                        var uniform = uniforms[key];
                        if (uniform.type === 't') {
                            if (Array.isArray(uniform.value) && uniform.value.length == 6) {
                                isLoaded_ = false;
                                // texture cube specified by urls
                                uniform.value = cubeTextureLoader.load(uniform.value);
                            } else
                            if (typeof uniform.value === 'string') {
                                isLoaded_ = false;
                                // single texture specified by url
                                uniform.value = textureLoader.load(uniform.value);
                            }
                        }
                    }
                }
            } );
        }

        // filter out geometries that ObjectLoader doesn't handle:
        var geometries = objectLoader.parseGeometries(json.geometries.filter(function (geom) {
            return geom.type !== "TextGeometry";
        }));
        // construct and insert geometries that ObjectLoader doesn't handle
        json.geometries.forEach( function (geom) {
            if (geom.type == "TextGeometry") {
                var geometry = new THREE.TextGeometry(geom.text, geom.parameters);
                geometry.uuid = geom.uuid;
                if (geom.name !== undefined) geometry.name = geom.name;
                geometries[geom.uuid] = geometry;
            }
        } );
        var images = objectLoader.parseImages(json.images, function () {
            onLoad(object);
        });
        var textures = objectLoader.parseTextures(json.textures, images);
        var materials = objectLoader.parseMaterials(json.materials, textures);

        var object = objectLoader.parseObject(json.object, geometries, materials);
        if (json.images === undefined || json.images.length === 0) {
            onLoad(object);
        }
        return object;
    }

    function CANNONize(obj, world) {
        obj.updateMatrixWorld();
        obj.traverse(function(node) {
            if (node.userData && node.userData.cannonData) {
                var body = makeCANNON(node, node.userData.cannonData);
                if (world) {
                    if (body instanceof CANNON.Body) {
                        world.addBody(body);
                    } else {
                        // assumed to be array
                        body.forEach(function (b) { world.addBody(b); });
                    }
                }
            }
        });

        function makeCANNON(node, cannonData) {
            var body;
            var bodies;
            if (node.body) {
                return node.body;
            }
            if (node instanceof THREE.Mesh) {
                var params = {mass: cannonData.mass,
                              position: node.position,
                              quaternion: node.quaternion};
                if (cannonData.linearDamping !== undefined) {
                    params.linearDamping = cannonData.linearDamping;
                }
                if (cannonData.angularDamping !== undefined) {
                    params.angularDamping = cannonData.angularDamping;
                }
                body = new CANNON.Body(params);
                body.mesh = node;
                cannonData.shapes.forEach(function(e) {
                    var shape,
                        quaternion,
                        position,
                        array;
                    switch (e) {
                        case 'Plane':
                            shape = new CANNON.Plane();
                            break;
                        case 'Box':
                            var halfExtents = new CANNON.Vec3();
                            node.geometry.computeBoundingBox();
                            halfExtents.x = node.scale.x * (node.geometry.boundingBox.max.x - node.geometry.boundingBox.min.x) / 2;
                            halfExtents.y = node.scale.y * (node.geometry.boundingBox.max.y - node.geometry.boundingBox.min.y) / 2;
                            halfExtents.z = node.scale.z * (node.geometry.boundingBox.max.z - node.geometry.boundingBox.min.z) / 2;
                            shape = new CANNON.Box(halfExtents);
                            break;
                        case 'Sphere':
                            node.geometry.computeBoundingSphere();
                            shape = new CANNON.Sphere(node.geometry.boundingSphere.radius);
                            break;
                        case 'ConvexPolyhedron':
                            var points = [];
                            var faces = [];
                            if (node.geometry instanceof THREE.BufferGeometry) {
                                array = node.geometry.getAttribute('position').array;
                                for (var i = 0; i < array.length; i += 3) {
                                    points.push(new CANNON.Vec3(array[i], array[i+1], array[i+2]));
                                }
                                array = node.geometry.index.array;
                                for (i = 0; i < array.length; i += 3) {
                                    var face = [array[i], array[i+1], array[i+2]];
                                    faces.push(face);
                                }
                            } else if (node.geometry instanceof THREE.Geometry) {
                                // TODO
                            }
                            shape = new CANNON.ConvexPolyhedron(points, faces);
                            break;
                        case 'Cylinder':
                            shape = new CANNON.Cylinder(node.geometry.parameters.radiusTop,
                                node.geometry.parameters.radiusBottom,
                                node.geometry.parameters.height,
                                node.geometry.parameters.radialSegments);
                            var quaternion = new CANNON.Quaternion();
                            quaternion.setFromEuler(-Math.PI/2, 0, 0, 'XYZ');
                            break;
                        case 'Heightfield':
                            // TODO: use new CANNON routine
                            array = node.geometry.getAttribute('position').array;
                            if (node.geometry.type !== 'PlaneBufferGeometry') {
                                alert('uh oh!');
                            }
                            var gridX1 = node.geometry.parameters.widthSegments + 1;
                            var gridY1 = node.geometry.parameters.heightSegments + 1;
                            var dx = node.geometry.parameters.width / node.geometry.parameters.widthSegments;
                            var data = [];
                            for (var ix = 0; ix < gridX1; ++ix) {
                                data.push(new Float32Array(gridY1));
                                for (var iy = 0; iy < gridY1; ++iy) {
                                    data[ix][iy] = array[3 * (gridX1 * (gridY1 - iy - 1) + ix) + 2];
                                }
                            }
                            shape = new CANNON.Heightfield(data, {
                                elementSize: dx
                            });
                            // center to match THREE.PlaneBufferGeometry:
                            position = new CANNON.Vec3();
                            position.x = -node.geometry.parameters.width / 2;
                            position.y = -node.geometry.parameters.height / 2;
                            break;
                        case 'Trimesh':
                            var vertices;
                            var indices;
                            if (node.geometry instanceof THREE.BufferGeometry) {
                                vertices = node.geometry.getAttribute('position').array;
                                indices = node.geometry.index.array;
                            } else {
                                vertices = [];
                                for (var iv = 0; iv < node.geometry.vertices.length; iv++) {
                                    var vert = node.geometry.vertices[iv];
                                    vertices.push(vert.x, vert.y, vert.z);
                                }
                                indices = [];
                                for (var iface = 0; iface < node.geometry.faces.length; iface++) {
                                    var face = node.geometry.faces[iface];
                                    indices.push(face.a, face.b, face.c);
                                }
                            }
                            shape = new CANNON.Trimesh(vertices, indices);
                            break;
                        case 'Ellipsoid':
                            // TODO
                            console.log('TODO');
                            break;
                        default:
                            console.log("unknown shape type: " + e);
                            break;
                    }
                    body.addShape(shape, position, quaternion);
                });
                node.body = body;
                return body;
            } else if (node instanceof THREE.Object3D) {
                bodies = [];
                node.children.forEach(function (c) { bodies.push(makeCANNON(c, cannonData)); });
                return bodies;
            } else {
                console.log("makeCANNON error");
            }
        }
    }

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


    function loadHeightfields(obj) {
        function getPixel(imagedata, x, y) {
            var position = (x + imagedata.width * y) * 4,
                data = imagedata.data;
            return {
                r: data[position],
                g: data[position + 1],
                b: data[position + 2],
                a: data[position + 3]
            };
        }
        obj.traverse( function (node) {
            if (node.userData && node.userData.heightfield) {
                console.log(node);
                isLoaded_ = false;
                imageLoader.load(node.userData.heightfield, function(image) {
                    var canvas = document.createElement('canvas');
                    canvas.width = image.width;
                    canvas.height = image.height;
                    var context = canvas.getContext('2d');
                    context.drawImage(image, 0, 0);
                    var imageData = context.getImageData(0, 0, image.width, image.height);
                    var attribute = node.geometry.getAttribute('position');
                    var gridX1 = node.geometry.parameters.widthSegments + 1;
                    var gridY1 = node.geometry.parameters.heightSegments + 1;
                    var i = 0;
                    for (var iy = 0; iy < gridY1; ++iy) {
                        for (var ix = 0; ix < gridX1; ++ix) {
                            var pixel = getPixel(imageData, ix, iy);
                            attribute.setZ(i++, 0.01 * (pixel.r + pixel.g + pixel.b));
                        }
                    }
                    attribute.needsUpdate = true;
                    node.geometry.computeFaceNormals();
                    node.geometry.computeVertexNormals();
                    node.geometry.normalsNeedUpdate = true;
                    node.geometry.computeBoundingSphere();
                    node.geometry.computeBoundingBox();
                });
            }
        });
    }


    return {
        load:           load,
        parse:          parse,
        CANNONize:      CANNONize,
        isLoaded:       isLoaded,
        TextGeomMesher: TextGeomMesher,
        config:         window.THREE_PY_CONFIG || {}
    };
} )();
