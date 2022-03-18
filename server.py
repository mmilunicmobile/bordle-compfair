import comparison
import json
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("main_page.html")


@app.route("/api/v1", methods=["POST"])
def api_call():
    data = request.get_json()
    if "random" == data["type"]:
        return json.dumps(comparison.random_country_index())
    if "compare" == data["type"]:
        border = data["geometry"]
        index = data["index"]
        shape = comparison.coordinates_to_geoseries(border)
        # this now done on the site
        # shape = shape.scale(20037508.342789244, 10018754.171394622)
        shape.set_crs("+proj=wintri", inplace=True)
        shape = shape.to_crs("+proj=cea")
        original_shape = comparison.get_geoseries_singular(index)
        original_shape.set_crs("+proj=cea", inplace=True)
        comparison_score = comparison.calculate_score(shape, original_shape)
        return json.dumps(comparison_score)
    if "fetch" == data["type"]:
        index = data["index"]
        return_data = {}
        return_data["name"] = comparison.get_country_info(index, "ADMIN")
        return_data["area"] = comparison.get_country_info(index, "area")
        return_data["iso"] = comparison.get_country_info(index, "ISO_A3")
        return_data["index"] = index
        return json.dumps(return_data)
    if "border" == data["type"]:
        index = data["index"]
        return_data = comparison.get_geometry_coordinates(index)
        return json.dumps(return_data)
