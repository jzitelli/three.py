function extractShaderLib() {
    "use strict";

    pyserver.writeFile('ShaderLib.json', JSON.stringify(THREE.ShaderLib, undefined, 2));
    pyserver.writeFile('ShaderChunk.json', JSON.stringify(THREE.ShaderChunk, undefined, 2));
    pyserver.writeFile('UniformsLib.json', JSON.stringify(THREE.UniformsLib, undefined, 2));
}
