from flask import Blueprint

core_bp = Blueprint(
    "core",
    __name__,
    template_folder="templates"
)

from . import routes  # noqa: E402,F401
from flask import session
from .menu import get_all_menus

#@core_bp.app_context_processor
#def inject_menus():
#    logged_in = "user_id" in session
#    username = session.get("username")
#    return {"menus": get_all_menus(logged_in, username)}

@core_bp.app_context_processor
def inject_menus():
    logged_in = False
    username = None

    if "username" in session:
        logged_in = True
        username = session["username"]

    return {"menus": get_all_menus(logged_in, username)}
