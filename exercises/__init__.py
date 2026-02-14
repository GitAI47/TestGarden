from flask import Blueprint

exercises_bp = Blueprint(
    "exercises",
    __name__,
    template_folder="templates"
)

from . import routes  # noqa: E402,F401
