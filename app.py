import os
from flask import Flask, send_from_directory
from config.config import Config
from config.database import init_db_teardown

# Import Blueprints
from routes.auth      import auth_bp
from routes.dashboard import dashboard_bp
from routes.club      import club_bp
from routes.players   import players_bp
from routes.squad     import squad_bp
from routes.training  import training_bp
from routes.matches   import matches_bp
from routes.finances  import finances_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure the uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register database teardown
    init_db_teardown(app)

    # Register all blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(club_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(squad_bp)
    app.register_blueprint(training_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(finances_bp)

    # Serve uploaded files (club logos)
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
