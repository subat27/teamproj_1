from flask import Blueprint, render_template

bp = Blueprint("overseas", __name__, url_prefix="/overseas")

@bp.route("/imglink")
def imglink():

    return render_template("overseas/overseas_graph.html")