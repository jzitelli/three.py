# three.py

This project provides utilities for integrating Python with [three.js](http://threejs.org).

The Python package `three` defines classes mirroring those in three.js.  They can be JSON-serialized
and (for the most part) loaded with three.js loaders.



## Examples

TODO



## Tests

### Client screenshot test

First, start a local server:

```bash
.../three.py $ python ./pyserver/flask_app.py
```

When the server is running:

```bash
.../three.py/test $ nosetests ./test_js.py
```



## Acknowledgements

JavaScript libraries:
  - [three.js](http://threejs.org)
  - [Cannon.js](http://www.cannonjs.org)

Python packages:
  - [Flask](http://flask.pocoo.org/)
  - [NumPy](http://www.numpy.org)
  - [SciPy](http://www.scipy.org)
