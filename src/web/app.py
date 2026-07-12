from pathlib import Path
from flask import Flask, render_template

project_root = Path(__file__).resolve().parent.parent.parent

app = Flask(
    __name__,
    template_folder=str(project_root / "templates"),
    static_folder=str(project_root / "static"),
)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)