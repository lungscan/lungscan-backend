import os

from dotenv import load_dotenv
from src import create_app

load_dotenv()

app = create_app(os.getenv("FLASK_ENV") or "development")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))