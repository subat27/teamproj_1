from flask import Blueprint, render_template

bp = Blueprint("overseas", __name__, url_prefix="/overseas")

@bp.route("/graph")
def overseas_graph():

    return render_template("overseas/overseas_graph.html")