# Testgarden/instructions/routes.py
from flask import render_template
from . import instructions_bp
from core.menu import get_all_menus
from users.utils import login_required


# ================================================================
#  SOFTWARETESTEN – OVERVIEW
# ================================================================
@instructions_bp.route("/testen/overview")
def testen_overview():
    steps = [
    {"nr": 1, "title": "Wat is testen?", "endpoint": "instructions.testen_module1", "status": "done"},
    {"nr": 2, "title": "Testsoorten", "endpoint": "instructions.testen_module2", "status": "progress"},
    {"nr": 3, "title": "Testplan maken", "endpoint": "instructions.testen_module3", "status": "not"},
    {"nr": 4, "title": "Testtechnieken", "endpoint": "instructions.testen_module4", "status": "not"},
    {"nr": 5, "title": "Exploratory Testing", "endpoint": "instructions.testen_module5", "status": "not"},
    {"nr": 6, "title": "Bug Reporting", "endpoint": "instructions.testen_module6", "status": "not"},
    {"nr": 7, "title": "API's testen", "endpoint": "instructions.testen_module7", "status": "not"},
    {"nr": 8, "title": "Testautomatisering", "endpoint": "instructions.testen_module8", "status": "not"},
    {"nr": 9, "title": "Eindproject", "endpoint": "instructions.testen_module9", "status": "not"},
]

    return render_template("testen/overview.html", steps=steps)


# ================================================================
#  SOFTWARETESTEN – INDIVIDUELE MODULES
# ================================================================
@instructions_bp.route("/testen/module1")
def testen_module1():
    return render_template("testen/module1_intro_testing.html")


@instructions_bp.route("/testen/module2")
def testen_module2():
    return render_template("testen/module2_testlevels_smoketests.html")


@instructions_bp.route("/testen/module3")
def testen_module3():
    return render_template("testen/module3_testplan_risico.html")


@instructions_bp.route("/testen/module4")
def testen_module4():
    return render_template("testen/module4_testtechnieken.html")


@instructions_bp.route("/testen/module5")
def testen_module5():
    return render_template("testen/module5_exploratory.html")


@instructions_bp.route("/testen/module6")
def testen_module6():
    return render_template("testen/module6_bugreporting.html")


@instructions_bp.route("/testen/module7")
def testen_module7():
    return render_template("testen/module7_api_testing.html")


@instructions_bp.route("/testen/module8")
def testen_module8():
    return render_template("testen/module8_automatisering_ai.html")


@instructions_bp.route("/testen/module9")
def testen_module9():
    return render_template("testen/module9_eindproject.html")


# ================================================================
#  Onderwerp B mapnaam – OVERVIEW 
# ================================================================

@instructions_bp.route("/git/overview")
def git_overview():
    steps = [
    {"nr": 1, "title": "Intro", "endpoint": "instructions.git_module1", "status": "done"},
    {"nr": 2, "title": "Basis", "endpoint": "instructions.git_module2", "status": "progress"},
    {"nr": 3, "title": "Samenwerken", "endpoint": "instructions.git_module3", "status": "not"},
    {"nr": 4, "title": "Titel module 4", "endpoint": "instructions.git_module4", "status": "not"},
    #{"nr": 5, "title": "Titel module 5", "endpoint": "instructions.mapnaam_module5", "status": "not"},
    #{"nr": 6, "title": "Titel module 6", "endpoint": "instructions.mapnaam_module6", "status": "not"},
    #{"nr": 7, "title": "Titel module 7", "endpoint": "instructions.mapnaam_module7", "status": "not"},
    #{"nr": 8, "title": "Titel module 8", "endpoint": "instructions.mapnaam_module8", "status": "not"},
    #{"nr": 9, "title": "Titel module 9", "endpoint": "instructions.mapnaam_module9", "status": "not"},
]

    return render_template("git/overview.html", steps=steps)


# ================================================================
#  Onderwerp B mapnaam – INDIVIDUELE MODULES
# ================================================================
@instructions_bp.route("/git/module1")
def git_module1():
    return render_template("git/module1_intro.html")


@instructions_bp.route("/git/module2")
def git_module2():
    return render_template("git/module2_basis.html")


@instructions_bp.route("/git/module3")
def git_module3():
    return render_template("git/module3_samenwerken.html")


@instructions_bp.route("/git/module4")
def git_module4():
    return render_template("git/module4_module4naam.html")
