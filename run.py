from app import create_app
from app.config import Config

# Running the app:
# flask --app run:app run
app = create_app(Config)

if __name__ == '__main__': 
    app.run(debug=True)