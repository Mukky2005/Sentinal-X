import os

# Port configuration: Defaults to 8001 to prevent conflicts with other projects
PORT = int(os.getenv("PORT", "8001"))
HOST = os.getenv("HOST", "0.0.0.0")

# Ollama local inference settings
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama3.2")
FALLBACK_CHAT_MODEL = os.getenv("FALLBACK_CHAT_MODEL", "gemma4:12b")

# JWT & Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "sentinelx_enterprise_master_key_9823487214981724")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# Data storage path (Persistent SQLite database for zero-conflict portability)
DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "sentinelx_data.json"))
AUDIT_LOGS_PATH = os.getenv("AUDIT_LOGS_PATH", os.path.join(os.path.dirname(__file__), "audit_logs.json"))
REQUESTS_PATH = os.getenv("REQUESTS_PATH", os.path.join(os.path.dirname(__file__), "service_requests.json"))
