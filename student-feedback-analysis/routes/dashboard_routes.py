from flask import Blueprint, current_app, render_template, Response, flash, redirect, url_for
from models.feedback_model import fetch_feedback_rows
from analysis.analytics import build_summary, create_charts, summary_csv

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    rows = fetch_feedback_rows(current_app.config)
    summary = build_summary(rows)
    create_charts(rows)
    return render_template("dashboard.html", summary=summary, row_count=len(rows))

@dashboard_bp.route("/export")
def export():
    rows = fetch_feedback_rows(current_app.config)
    csv_data = summary_csv(rows)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=feedback_summary.csv"}
    )
