var fs = require('fs');
var THREE = require('three.js');
fs.writeFile("shaderlib/ShaderLib.json", JSON.stringify(THREE.ShaderLib, undefined, 2), function (err) {
    if (err) {
        return console.log(err);
    }
    console.log("wrote shaderlib/ShaderLib.json");
});
fs.writeFile("shaderlib/ShaderChunk.json", JSON.stringify(THREE.ShaderChunk, undefined, 2), function (err) {
    if (err) {
        return console.log(err);
    }
    console.log("wrote shaderlib/ShaderChunk.json");
});
fs.writeFile("shaderlib/UniformsLib.json", JSON.stringify(THREE.UniformsLib, undefined, 2), function (err) {
    if (err) {
        return console.log(err);
    }
    console.log("wrote shaderlib/UniformsLib.json");
});
