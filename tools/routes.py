# tools/routes.py
from flask import request, Response, render_template, url_for
import io
import qrcode
from . import tools_bp
from users.utils import login_required


@tools_bp.route("/")
@login_required
def tools_qrcode():
    return render_template("tools/index.html")


@tools_bp.route("/qrcode")
@login_required
def qrcode_page():
    default_url = request.url_root.rstrip("/") + url_for("core.index")
    return render_template(
        "tools/qrcode.html",
        default_url=default_url)


@tools_bp.route("/qrcode.png")
@login_required
def qrcode_png():
    data = request.args.get("data", "")
    if not data:
        return Response("Missing ?data=", status=400)

    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return Response(buf.getvalue(), mimetype="image/png")
