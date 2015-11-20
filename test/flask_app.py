import os
import logging
_logger = logging.getLogger(__name__)

from flask import Flask, render_template
TEMPLATE_FOLDER = os.path.join(os.getcwd(), "templates")
app = Flask(__name__,
            template_folder=TEMPLATE_FOLDER)


