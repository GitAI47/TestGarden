from flask import session, render_template, request, redirect, url_for, flash
from . import scripts_bp
from users.roles import role_required
from database.models import (
    db,
    TestCase, TestStep, Precondition,
    TestRun, TestResult, StepResult
)



@scripts_bp.route("/cases")
@role_required("teacher")  # voorlopig alleen docenten
def cases_list():
    cases = TestCase.query.order_by(TestCase.created_at.desc()).all()
    return render_template("cases_list.html", cases=cases)


@scripts_bp.route("/cases/new", methods=["GET", "POST"])
@role_required("teacher")
def cases_new():
    if request.method == "POST":
        key = (request.form.get("key") or "").strip()
        title = (request.form.get("title") or "").strip()
        module = (request.form.get("module") or "").strip() or None
        description = (request.form.get("description") or "").strip() or None
        tags = (request.form.get("tags") or "").strip() or None
        priority = (request.form.get("priority") or "").strip() or None

        if not key or not title:
            flash("Key en titel zijn verplicht.", "warning")
            return render_template("cases_new.html", form=request.form)

        if TestCase.query.filter_by(key=key).first():
            flash("Deze key bestaat al. Kies een unieke key.", "warning")
            return render_template("cases_new.html", form=request.form)

        tc = TestCase(
            key=key,
            title=title,
            module=module,
            description=description,
            tags=tags,
            priority=priority,
        )
        db.session.add(tc)
        db.session.flush()  # tc.id beschikbaar zonder commit

        # Preconditions: meerdere inputvelden met name="precondition"
        preconditions = [p.strip() for p in request.form.getlist("precondition") if p.strip()]
        for text in preconditions:
            db.session.add(Precondition(test_case_id=tc.id, text=text))

        # Steps: meerdere blokken met step_no/action/expected (zelfde name per veld)
        step_nos = request.form.getlist("step_no")
        actions = request.form.getlist("action")
        expecteds = request.form.getlist("expected")

        # We lopen veilig over de kortste lijst
        n = min(len(step_nos), len(actions), len(expecteds))
        steps_to_add = []
        for i in range(n):
            no_raw = (step_nos[i] or "").strip()
            action = (actions[i] or "").strip()
            expected = (expecteds[i] or "").strip()

            # Lege regels overslaan
            if not no_raw and not action and not expected:
                continue

            # Minimale validatie: action verplicht als er een step is
            if not action:
                flash("Elke stap moet minimaal een actie hebben.", "warning")
                return render_template("cases_new.html", form=request.form)

            try:
                step_no = int(no_raw) if no_raw else (len(steps_to_add) + 1)
            except ValueError:
                flash("Stapnummer moet een getal zijn.", "warning")
                return render_template("cases_new.html", form=request.form)

            steps_to_add.append(TestStep(
                test_case_id=tc.id,
                step_no=step_no,
                action=action,
                expected=expected or None
            ))

        # Als je wil: eis minimaal 1 stap
        if len(steps_to_add) == 0:
            flash("Voeg minimaal één stap toe.", "warning")
            return render_template("cases_new.html", form=request.form)

        for s in steps_to_add:
            db.session.add(s)

        db.session.commit()
        flash("Testcase opgeslagen ✅", "success")
        return redirect(url_for("scripts.cases_detail", case_id=tc.id))

    # GET
    return render_template("cases_new.html", form=None)


@scripts_bp.route("/cases/<int:case_id>")
@role_required("teacher")
def cases_detail(case_id):
    tc = TestCase.query.get_or_404(case_id)
    # Zorg dat steps gesorteerd zijn
    steps = sorted(tc.steps, key=lambda s: s.step_no)
    return render_template("cases_detail.html", tc=tc, steps=steps)


# route TestRun lijst cases, status kiezen en opslaan

@scripts_bp.route("/runs/start")
@role_required("teacher")
def run_start():
    run = TestRun(user_id=session["user_id"])
    db.session.add(run)
    db.session.commit()

    return redirect(url_for("scripts.run_execute", run_id=run.id))


# route TestResult


@scripts_bp.route("/runs/<int:run_id>", methods=["GET", "POST"])
@role_required("teacher")
def run_execute(run_id):
    run = TestRun.query.get_or_404(run_id)
    cases = TestCase.query.order_by(TestCase.key).all()

    if request.method == "POST":
        # Oude results weg (zodat je opnieuw kunt opslaan)
        TestResult.query.filter_by(run_id=run.id).delete()
        db.session.commit()

        for case in cases:
            steps_sorted = sorted(case.steps, key=lambda s: s.step_no)
            if not steps_sorted:
                continue

            step_statuses = []
            step_results_to_add = []

            for step in steps_sorted:
                status = (request.form.get(f"step_status_{case.id}_{step.step_no}") or "").strip()
                comment = (request.form.get(f"step_comment_{case.id}_{step.step_no}") or "").strip()

                if not status:
                    continue

                step_statuses.append(status)
                step_results_to_add.append({
                    "step_no": step.step_no,
                    "action_text": step.action,
                    "expected_text": step.expected,
                    "status": status,
                    "comment": comment or None
                })

            # niets ingevuld voor deze testcase -> geen resultaat opslaan
            if not step_statuses:
                continue

            # testcase-status afleiden
            if "fail" in step_statuses:
                tc_status = "fail"
            elif "note" in step_statuses:
                tc_status = "note"
            elif all(s == "pass" for s in step_statuses):
                tc_status = "pass"
            else:
                tc_status = "skip"

            result = TestResult(
                run_id=run.id,
                test_case_id=case.id,
                status=tc_status,
                comment=None
            )
            db.session.add(result)
            db.session.flush()  # result.id beschikbaar

            for sr in step_results_to_add:
                db.session.add(StepResult(
                    result_id=result.id,
                    step_no=sr["step_no"],
                    action_text=sr["action_text"],
                    expected_text=sr["expected_text"],
                    status=sr["status"],
                    comment=sr["comment"],
                ))

        db.session.commit()
        flash("Resultaten opgeslagen ✅", "success")
        return redirect(url_for("scripts.cases_list"))

    # GET
    return render_template("run_execute.html", run=run, cases=cases)
