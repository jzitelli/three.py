import json

from flask import Blueprint, Markup, render_template, request

from flask_app import WebVRConfig, get_overlay_content

from three import *



blueprint = Blueprint(__name__, __name__)

@blueprint.route('/%s' % __name__)
def heightfield():
    url = request.args.get('url', 'images/terrain128.png')
    heightfieldImage = Image(url=url)
    scene = Scene()
    scene.add(PointLight(color=0xffffff, intensity=1, distance=800,
                         position=[10, 0, 0]))
    scene.add(HeightfieldMesh(heightfieldImage=heightfieldImage,
                              heightfieldScale=32,
                              material=MeshLambertMaterial(color=0xff0000),
                              rotation=[-0.33*np.pi, 0, 0],
                              position=[0, -20, -32],
                              cannonData={'mass': 0, 'shapes': ['Heightfield']}))
    scene.add(Mesh(geometry=SphereBufferGeometry(radius=2),
                   material=MeshPhongMaterial(color=0xffff00, shading=FlatShading),
                   position=[0, 14, -45],
                   cannonData={'mass': 1, 'shapes': ['Sphere']}))
    scene.add(Mesh(geometry=BoxGeometry(width=2, height=2, depth=2),
                   material=MeshPhongMaterial(color=0xff00ff, shading=FlatShading),
                   position=[4, 13, -45],
                   cannonData={'mass': 1, 'shapes': ['Box']}))
    return render_template('template.html',
                           title='three.py  -  %s test' % __name__,
                           overlay_content=get_overlay_content(),
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(url_prefix="test/"), indent=2))))
