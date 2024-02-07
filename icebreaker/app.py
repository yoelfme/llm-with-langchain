from flask import Flask, render_template, request, jsonify

from icebreaker import ice_break

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    person_intel, profile_pic_url = ice_break(name)
    return jsonify(
        {
            "summary": person_intel.summary,
            "facts": person_intel.interesting_facts,
            "interests": person_intel.topics_of_interest,
            "ice_breakers": person_intel.ice_breakers,
            "picture_url": profile_pic_url,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
