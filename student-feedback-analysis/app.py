from flask import Flask, render_template
from config import Config
from models.feedback_model import init_db
from routes.feedback_routes import feedback_bp
from routes.dashboard_routes import dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app.config)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(dashboard_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
