import os

DB_CONFIG = {
    "host": os.environ.get("MYSQLHOST", "mysql.railway.internal"),
    "user": os.environ.get("MYSQLUSER", "root"),
    "password": os.environ.get("MYSQLPASSWORD", "SNLPJJsJpjsDEuYxTtTikbUGuIaoNcSy"),
    "database": os.environ.get("MYSQLDATABASE", "railway"),
    "port": int(os.environ.get("MYSQLPORT", 3306))
}
