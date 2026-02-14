from flask import Blueprint

feedback_bp = Blueprint(
    "feedback",
    __name__,
    template_folder="templates"
)

from . import routes  # noqa: E402,F401
