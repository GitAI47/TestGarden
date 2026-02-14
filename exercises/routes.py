from flask import render_template, session
from . import exercises_bp
from core.menu import get_all_menus
from users.utils import login_required

# ================================================================
#  Onderwerp mapnaam – OVERVIEW 
# ================================================================

@exercises_bp.route("/een/overview")
@login_required
def een_overview():
    steps = [
    {"nr": 1, "title": "Exploratory Bug Hunting", "endpoint": "exercises.een_module1", "status": "done"},
    {"nr": 2, "title": "Bug Triage & Kwaliteit", "endpoint": "exercises.een_module2", "status": "progress"},
    {"nr": 3, "title": "Teststrategie & Risicodenken", "endpoint": "exercises.een_module3", "status": "not"},
    {"nr": 4, "title": "Regression, Evidence & Testsystemen", "endpoint": "exercises.een_module4", "status": "not"},
    {"nr": 5, "title": "Automatisering & Bewuste Keuzes", "endpoint": "exercises.een_module5", "status": "not"},
    {"nr": 6, "title": "Ethiek, Macht & Verantwoordelijkheid", "endpoint": "exercises.een_module6", "status": "not"},
    {"nr": 7, "title": "AI & Testen", "endpoint": "exercises.een_module7", "status": "not"},
    #{"nr": 8, "title": "Titel module 8", "endpoint": "instructions.mapnaam_module8", "status": "not"},
    #{"nr": 9, "title": "Titel module 9", "endpoint": "instructions.mapnaam_module9", "status": "not"},
]

    # Alleen zichtbaar voor docent
    if session.get("role") == "teacher":
        steps.append({
            "nr": "★",
            "title": "Docentpaneel",
            "endpoint": "exercises.een_teacher_panel",
            "status": "teacher"
        })

    return render_template("een/overview.html", steps=steps)


# ================================================================
#  Onderwerp mapnaam – INDIVIDUELE MODULES
# ================================================================
@exercises_bp.route("/een/module1")
def een_module1():
    return render_template("een/module1_Exploratory Bug Hunting.html")


@exercises_bp.route("/een/module2")
def een_module2():
    return render_template("een/module2_Bug Triage & Kwaliteit.html")


@exercises_bp.route("/een/module3")
def een_module3():
    return render_template("een/module3_Teststrategie & Risicodenken.html")


@exercises_bp.route("/een/module4")
def een_module4():
    return render_template("een/module4_Regression, Evidence & Testsystemen.html")


@exercises_bp.route("/een/module5")
def een_module5():
    return render_template("een/module5_Automatisering & Bewuste Keuzes.html")


@exercises_bp.route("/een/module6")
def een_module6():
    return render_template("een/module6_Ethiek, Macht & Verantwoordelijkheid.html")


@exercises_bp.route("/een/module7")
def een_module7():
    return render_template("een/module7_AI & Testen.html")



from users.roles import role_required


# ================================================================
#  DOCENT
# ================================================================
@exercises_bp.route("/een/teacher")
@role_required("teacher")
def een_teacher_panel():
    return render_template("een/teacher_panel.html")
