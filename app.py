from flask import Flask
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

app = Flask(__name__)

# Ambil URL DB dari environment
db_url = os.getenv("DB_URL")
engine = create_engine(db_url)

@app.route('/')
def index():
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT NOW();")
            return f"Database connected! Current time: {list(result)[0][0]}"
    except Exception as e:
        return f"Failed to connect to DB: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
