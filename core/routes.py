from flask import render_template
from . import core_bp


@core_bp.route("/")
def index():
    return render_template("index.html")



@core_bp.route("/about")
def about():
    return render_template("about.html")


