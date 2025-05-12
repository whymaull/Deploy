import os
from urllib.parse import urlparse

url = urlparse(os.environ.get("DATABASE_URL", "mysql://root@localhost/railway"))

DB_CONFIG = {
    "host": url.hostname,
    "user": url.username,
    "password": url.password,
    "database": url.path[1:], 
    "port": url.port or 3306
}
