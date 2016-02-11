THREE.py = ( function () {
    "use strict";
    var manager = new THREE.LoadingManager();
    var isLoaded_ = true;
    manager.onLoad = function () {
        isLoaded_ = true;
    };
    
    function isLoaded() {
        return isLoaded_;
    }

    var objectLoader = new THREE.ObjectLoader(manager),
        imageLoader = new THREE.ImageLoader(manager),
        textureLoader = new THREE.TextureLoader(manager),
        cubeTextureLoader = new THREE.CubeTextureLoader(manager);

    function load(url, onLoad) {
        // TODO:
    }

    var fontLoader = new THREE.FontLoader();
    var font;
    var fonts = {};
    fontLoader.load('/node_modules/three.js/examples/fonts/helvetiker_regular.typeface.js', function (_font) {
        fonts.helvetiker = _font;
    });
    fontLoader.load('/fonts/Anonymous Pro_Regular.js', function (_font) {
        fonts.anonymous_pro = _font;
    });

    function parse(json, texturePath, onLoad) {

        if (texturePath) {
            objectLoader.setTexturePath(texturePath);
        }

        isLoaded_ = false;
        function onLoad_(obj) {
            loadHeightfields(obj);
            obj.traverse( function (node) {
                if (node instanceof THREE.Mesh) {
                    node.geometry.computeBoundingSphere();
                    node.geometry.computeBoundingBox();
                    if (node.userData && node.userData.visible === false) {
                        node.visible = false;
                    }
                    if (!(node.geometry instanceof THREE.SphereBufferGeometry)) {
                        // makes seams appear on spherebuffergeometries due to doubled vertices at phi=0=2*pi
                        //node.geometry.computeVertexNormals();
                    }
                    if (node.material.shading === THREE.FlatShading)
                        node.geometry.computeFaceNormals();
                }
            } );
            isLoaded_ = true;
            if (onLoad) {
                onLoad(obj);
            }
        }

        // filter out geometries that ObjectLoader doesn't handle, parse the rest:
        var geometries = objectLoader.parseGeometries(json.geometries.filter( function (geom) {
            return geom.type !== "TextGeometry" && geom.type !== 'HeightfieldBufferGeometry';
        } ));

        // construct and insert geometries that ObjectLoader doesn't handle
        json.geometries.forEach( function (geom) {
            if (geom.type === "TextGeometry") {
                geom.parameters.font = fonts[geom.parameters.fontName || 'helvetiker'];
                var textGeometry = new THREE.TextGeometry(geom.text, geom.parameters);
                textGeometry.uuid = geom.uuid;
                if (geom.name !== undefined) textGeometry.name = geom.name;
                geometries[geom.uuid] = textGeometry;
            }
        } );

        if (json.materials) {
            json.materials.forEach( function (mat) {
                if (mat.type.endsWith("ShaderMaterial") && mat.uniforms) {
                    var uniforms = mat.uniforms;
                    for (var key in uniforms) {
                        var uniform = uniforms[key];
                        if (uniform.type === 't') {
                            if (Array.isArray(uniform.value) && uniform.value.length == 6) {
                                // texture cube specified by urls
                                uniform.value = cubeTextureLoader.load(uniform.value);
                            } else if (typeof uniform.value === 'string') {
                                // single texture specified by url
                                uniform.value = textureLoader.load(uniform.value);
                            }
                        }
                    }
                }
            } );
        }

        var images = objectLoader.parseImages(json.images, function () { onLoad_(object); });
        var textures = objectLoader.parseTextures(json.textures, images);
        var materials = objectLoader.parseMaterials(json.materials, textures);

        var object = objectLoader.parseObject(json.object, geometries, materials);
        if (json.images === undefined || json.images.length === 0) {
            onLoad_(object);
        }   

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
                if (node.userData && node.userData.heightfieldImage) {
                    var uuid = node.userData.heightfieldImage;
                    var heightfieldScale = node.userData.heightfieldScale || 1;
                    var image = images[uuid];
                    if (image) {
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
                                attribute.setZ(i++, heightfieldScale * (pixel.r + 256*pixel.g + 256*256*pixel.b) / (256 * 256 * 256));
                            }
                        }
                        attribute.needsUpdate = true;
                        node.geometry.computeFaceNormals();
                        node.geometry.computeVertexNormals();
                        node.geometry.normalsNeedUpdate = true;
                        node.geometry.computeBoundingSphere();
                        node.geometry.computeBoundingBox();
                    }
                }
            });
        }

        return object;
    }

    return {
        load:             load,
        parse:            parse,
        isLoaded:         isLoaded,
        fonts:            fonts
    };
} )();
