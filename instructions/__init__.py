from flask import Blueprint

# Definieer blueprint (slechts één keer!)
instructions_bp = Blueprint(
    "instructions",
    __name__,
    template_folder="templates"
)

# Laad routes
from . import routes  # noqa: E402,F401
