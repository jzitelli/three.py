#!/usr/bin/python
import argparse
import logging
import numpy as np


from three import Image
from three.materials import MeshLambertMaterial
from three.heightfields import HeightfieldMesh


def main():
    import os.path
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))
    import app
    import gl_rendering
    import primitives
    import techniques
    radius=0.007
    length=1.15
    cylinder = primitives.CylinderPrimitive(radius=radius, height=length)
    cylinder.attributes['a_position'] = cylinder.attributes['vertices']
    heightfield_mesh = add_heightfield()

    app.main(novr=args.novr,
             multisample=args.multisample,
             meshes=[heightfield_mesh],
             controller_meshes=[gl_rendering.Mesh({gl_rendering.Material(techniques.LAMBERT_TECHNIQUE,
                                                                         values={'u_color': [0.5, 0.5, 0.0, 0.0],
                                                                                 'u_lightpos': [1.0, 15.0, 1.5]})
                                                   : [cylinder]}),
                                gl_rendering.Mesh({gl_rendering.Material(techniques.LAMBERT_TECHNIQUE,
                                                                         values={'u_color': [0.5, 0.5, 0.0, 0.0],
                                                                                 'u_lightpos': [1.0, 15.0, 1.5]})
                                                   : [cylinder]})])


def add_heightfield(url='images/heightfield.png'):
    heightfield_image = Image(url=url)
    return HeightfieldMesh(heightfieldImage=heightfield_image,
                           heightfieldScale=64,
                           material=MeshLambertMaterial(color=0x8b6545),
                           rotation=[-0.4*np.pi, 0, 0],
                           position=[0, -18, 0],
                           scale=[0.5, 0.5, 0.5],
                           cannonData={'mass': 0, 'shapes': ['Heightfield']},
                           receiveShadow=True)


if __name__ == "__main__":
    FORMAT = '  THREE.PY  | %(asctime)s | %(levelname)s -- %(name)s *** %(message)s'
    parser = argparse.ArgumentParser()
    parser.add_argument("--novr", help="non-VR mode", action="store_true")
    parser.add_argument('--multisample', help="set multisampling level for VR rendering",
                        type=int, default=0)
    parser.add_argument("-v", help="verbose logging", action="store_true")
    args = parser.parse_args()
    if args.v:
        logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    else:
        logging.basicConfig(format=FORMAT, level=logging.WARNING)
    main()
