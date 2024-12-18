from flask import Flask
from flask import render_template

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.config['DEBUG'] = True

    # Register blueprints (routes)
    from .routes import main
    app.register_blueprint(main)


    @app.route('/')
    def home():
        return render_template('index.html')
    
    return app


