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
    scene.add(DirectionalLight(color=0xef965f,
                               intensity=0.7,
                               position=[23, 100, 56],
                               castShadow=True))
    scene.add(HeightfieldMesh(heightfieldImage=heightfieldImage,
                              heightfieldScale=32,
                              material=MeshLambertMaterial(color=0x8b6545),
                              rotation=[-0.33*np.pi, 0, 0],
                              position=[0, -20, -32],
                              cannonData={'mass': 0, 'shapes': ['Heightfield']},
                              receiveShadow=True))
    scene.add(Mesh(geometry=SphereBufferGeometry(radius=4.5),
                   material=MeshPhongMaterial(color=0xffff00, shading=FlatShading),
                   position=[0, 14, -45],
                   cannonData={'mass': 1, 'shapes': ['Sphere']},
                   castShadow=True))
    scene.add(Mesh(geometry=BoxBufferGeometry(width=4, height=4, depth=5),
                   material=MeshPhongMaterial(color=0xff00ff, shading=FlatShading),
                   position=[4, 13, -45],
                   cannonData={'mass': 1, 'shapes': ['Box']},
                   castShadow=True))
    return render_template('template.html',
                           title='three.py  -  %s test' % __name__,
                           overlay_content=get_overlay_content(),
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(url_prefix="test/"), indent=2))))
