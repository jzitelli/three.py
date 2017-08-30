#!/usr/bin/python
import argparse
import logging


if __name__ == "__main__":
    FORMAT = '  THREE.PY  | %(asctime)s | %(levelname)s -- %(name)s *** %(message)s'
    parser = argparse.ArgumentParser()
    parser.add_argument("--novr", help="non-VR mode", action="store_true")
    parser.add_argument("--use_simple_ball_collisions", help="use simple ball collision model",
                        action="store_true")
    parser.add_argument('-o', "--ode",
                        help="use ODE for physics simulation instead of the default event-based engine",
                        action="store_true")
    parser.add_argument('--multisample', help="set multisampling level for VR rendering",
                        type=int, default=0)
    parser.add_argument('--bb_particles',
                        help='render balls using billboard particle shader instead of polygon meshes',
                        action='store_true')
    parser.add_argument("-v", help="verbose logging", action="store_true")
    args = parser.parse_args()
    if args.v:
        logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    else:
        logging.basicConfig(format=FORMAT, level=logging.WARNING)
    import app
    app.main(novr=args.novr,
             use_simple_ball_collisions=args.use_simple_ball_collisions,
             use_ode=args.ode,
             multisample=args.multisample,
             use_bb_particles=args.bb_particles)
