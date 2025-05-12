from flask import Flask
from flask_cors import CORS 
from models.schema import init_db, import_symbols
from routes.kode_saham import symbol_bp 
from routes.prediksi import predict_bp 
from routes.auth import auth_bp 
from routes.riwayat import riwayat_bp 
import os

app = Flask(__name__)
CORS(app)

app.register_blueprint(symbol_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(riwayat_bp)

init_db()
import_symbols()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
