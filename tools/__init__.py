from flask import Blueprint

# Definieer blueprint (slechts één keer!)
tools_bp = Blueprint(
    "tools",
    __name__,
    template_folder="templates"
)

# Laad routes
from . import routes  # noqa: E402,F401
