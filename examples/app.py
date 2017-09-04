import sys
import os.path
import logging
import OpenGL
OpenGL.ERROR_CHECKING = False
OpenGL.ERROR_LOGGING = False
OpenGL.ERROR_ON_COPY = True
import OpenGL.GL as gl
import cyglfw3 as glfw


_logger = logging.getLogger(__name__)

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, os.path.pardir))
from gl_rendering import OpenGLRenderer
try:
   from pyopenvr_renderer import OpenVRRenderer
except ImportError as err:
    _logger.warning('could not import pyopenvr_renderer:\n%s', err)
    _logger.warning('\n\n\n**** VR FEATURES ARE NOT AVAILABLE! ****\n\n\n')
    OpenVRRenderer = None

BG_COLOR = (0.0, 0.0, 0.0, 0.0)

TEXTURES_DIR = os.path.join(_HERE, os.path.pardir, 'textures')


def setup_glfw(width=800, height=600, double_buffered=False, title="poolvr.py 0.0.1", multisample=0):
    if not glfw.Init():
        raise Exception('failed to initialize glfw')
    if not double_buffered:
        glfw.WindowHint(glfw.DOUBLEBUFFER, False)
        glfw.SwapInterval(0)
    glfw.WindowHint(glfw.SAMPLES, 2)
    glfw.WindowHint(glfw.AUX_BUFFERS, 1)
    window = glfw.CreateWindow(width, height, title)
    if not window:
        glfw.Terminate()
        raise Exception('failed to create glfw window')
    glfw.MakeContextCurrent(window)
    _logger.info('GL_VERSION: %s', gl.glGetString(gl.GL_VERSION))
    renderer = OpenGLRenderer(window_size=(width, height), znear=0.1, zfar=1000)
    def on_resize(window, width, height):
        gl.glViewport(0, 0, width, height)
        renderer.window_size = (width, height)
        renderer.update_projection_matrix()
    glfw.SetWindowSizeCallback(window, on_resize)
    return window, renderer


def add_heightfield(url='examples/heightfield.png'):
    from three import Image
    from three.heightfields import HeightfieldMesh
    heightfieldImage = Image(url=url)
    return HeightfieldMesh(heightfieldImage=heightfieldImage,
                           heightfieldScale=64,
                           material=MeshLambertMaterial(color=0x8b6545),
                           rotation=[-0.4*np.pi, 0, 0],
                           position=[0, -18, 0],
                           scale=[0.5, 0.5, 0.5],
                           cannonData={'mass': 0, 'shapes': ['Heightfield']},
                           receiveShadow=True)


def main(window_size=(800,600),
         novr=False,
         use_simple_ball_collisions=False,
         use_ode=False,
         multisample=0,
         use_bb_particles=False,
         meshes=None,
         controller_meshes=None):
    """
    The main routine.

    Performs initializations, setups, kicks off the render loop.
    """
    _logger.info('HELLO')
    window, fallback_renderer = setup_glfw(width=window_size[0], height=window_size[1], double_buffered=novr, multisample=multisample)
    if not novr and OpenVRRenderer is not None:
        try:
            renderer = OpenVRRenderer(window_size=window_size, multisample=multisample)
        except Exception as err:
            renderer = fallback_renderer
            _logger.error('could not initialize OpenVRRenderer: %s', err)
    else:
        renderer = fallback_renderer
    camera_world_matrix = fallback_renderer.camera_matrix
    camera_position = camera_world_matrix[3,:3]
    def process_input(dt):
        glfw.PollEvents()
    if controller_meshes is None:
        controller_meshes = []
    if meshes is None:
        meshes = [] + controller_meshes
    for mesh in meshes:
        mesh.init_gl()
    gl.glViewport(0, 0, window_size[0], window_size[1])
    gl.glClearColor(*BG_COLOR)
    gl.glEnable(gl.GL_DEPTH_TEST)


    _logger.info('entering render loop...')


    sys.stdout.flush()
    nframes = 0
    max_frame_time = 0.0
    lt = glfw.GetTime()
    while not glfw.WindowShouldClose(window):
        t = glfw.GetTime()
        dt = t - lt
        lt = t
        process_input(dt)
        with renderer.render(meshes=meshes) as frame_data:
            if isinstance(renderer, OpenVRRenderer) and frame_data:
                ####################
                ##### VR mode: #####
                ####################
                renderer.process_input()
                hmd_pose = frame_data['hmd_pose']
                camera_position[:] = hmd_pose[:,3]
                for i, pose in enumerate(frame_data['controller_poses'][:2]):
                    if i < len(controller_meshes):
                        controller_meshes[i].matrix[:3,:3] = pose[:,:3].T
                        x,y,z = controller_meshes[i].matrix[1,:3]
                        controller_meshes[i].matrix[1,:3] = controller_meshes[i].matrix[2,:3]
                        controller_meshes[i].matrix[2,:3] = x,-z,-y
                        controller_meshes[i].matrix[3,:3] = pose[:,3]
                        controller_meshes[i].update_world_matrices()
            elif isinstance(renderer, OpenGLRenderer):
                #########################
                ##### desktop mode: #####
                #########################
                pass
        max_frame_time = max(max_frame_time, dt)
        if nframes == 0:
            st = glfw.GetTime()
        nframes += 1
        glfw.SwapBuffers(window)
    if nframes > 1:
        _logger.info('...exited render loop: average FPS: %f, maximum frame time: %f, average frame time: %f',
                     (nframes - 1) / (t - st), max_frame_time, (t - st) / (nframes - 1))
    renderer.shutdown()
    _logger.info('...shut down renderer')
    glfw.DestroyWindow(window)
    glfw.Terminate()
    _logger.info('GOODBYE')
