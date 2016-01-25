# three.py

This project provides utilities for integrating Python with [three.js](http://threejs.org).  It's also where I'm throwing random
WebVR-related prototypes / experiments.

The Python package `three` defines classes mirroring those in three.js.  They can be JSON-serialized and (for the most part) loaded with three.js loaders.



## Examples

TODO



## Tests

### Screenshot tests

From the `three.py/test` directory,

```
$ python ./run_tests.py --with-needle-capture --with-needle-cleanup-on-success
```


## Acknowledgements

JavaScript libraries:
  - [three.js](http://threejs.org)
  - [Cannon.js](http://www.cannonjs.org)
  - [Leap Motion JavaScript framework](https://github.com/leapmotion/leapjs)
  - [webvr-boilerplate](https://github.com/borismus/webvr-boilerplate)
  - [Shader Particle Engine](https://github.com/squarefeet/ShaderParticleEngine)

Python packages:
  - [Flask](http://flask.pocoo.org/)
  - [NumPy](http://www.numpy.org)
  - [SciPy](http://www.scipy.org)
  - nose
  - [Needle](https://github.com/bfirsh/needle)
