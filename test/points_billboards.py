import json

from flask import Blueprint, Markup, render_template, request

from flask_app import WebVRConfig, get_overlay_content

from three import *



blueprint = Blueprint(__name__, __name__)

@blueprint.route('/%s' % __name__)
def points():
    scene = Scene()
    position = [0, 1.3, -2]
    geometry = SphereBufferGeometry(radius=3.2, widthSegments=32, heightSegments=24)
    material = PointsMaterial(color=0xffff00, size=0.6, sizeAttenuation=True,
                              map=Texture(image=Image(url='node_modules/three/examples/textures/sprites/disc.png')),
                              transparent=True, alphaTest=0.5)
    points = Points(geometry=geometry, material=material, position=position)
    scene.add(points);

    geometry = SphereBufferGeometry(radius=1.4, widthSegments=24, heightSegments=18)
    material = PointsMaterial(color=0xbbffbb, size=16, sizeAttenuation=False,
                              map=Texture(image=Image(url='node_modules/three/examples/textures/sprites/disc.png')),
                              transparent=True, alphaTest=0.5)
    points = Points(geometry=geometry, material=material, position=position)
    scene.add(points);

    return render_template('template.html',
                           title='three.py  -  %s test' % __name__,
                           overlay_content=get_overlay_content(),
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(), indent=2))))
