from flask import Flask
from flask_cors import CORS # type: ignore
from models.schema import init_db, import_symbols
from routes.kode_saham import symbol_bp # type: ignore
from routes.prediksi import predict_bp # type: ignore

app = Flask(__name__)
CORS(app)

app.register_blueprint(symbol_bp)
app.register_blueprint(predict_bp)

init_db()
import_symbols()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
