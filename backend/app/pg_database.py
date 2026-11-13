import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger("SentinelPG")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sentinelx:sentinelx_secure_pass@db:5432/sentinelx_db")

SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS tenants (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description TEXT,
    domain VARCHAR(200),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS roles (
    id VARCHAR(100) PRIMARY KEY,
    tenant_id VARCHAR(100) REFERENCES tenants(id),
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description TEXT,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(100) PRIMARY KEY,
    tenant_id VARCHAR(100) REFERENCES tenants(id),
    name VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    role_id VARCHAR(100) REFERENCES roles(id),
    role_name VARCHAR(200),
    department VARCHAR(100) DEFAULT 'engineering',
    clearance_level INT DEFAULT 1,
    is_admin BOOLEAN DEFAULT FALSE,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS documents (
    id VARCHAR(100) PRIMARY KEY,
    tenant_id VARCHAR(100) REFERENCES tenants(id),
    title VARCHAR(300) NOT NULL,
    description TEXT,
    file_name VARCHAR(300),
    file_type VARCHAR(100),
    uploaded_by VARCHAR(100),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    allowed_role_ids TEXT[] DEFAULT '{}',
    visibility_scope VARCHAR(50) DEFAULT 'ROLE_SCOPED',
    department VARCHAR(100) DEFAULT 'engineering',
    classification_level INT DEFAULT 1,
    version VARCHAR(20) DEFAULT '1.0',
    chunks_count INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'INDEXED'
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id VARCHAR(100) PRIMARY KEY,
    tenant_id VARCHAR(100) REFERENCES tenants(id),
    document_id VARCHAR(100) REFERENCES documents(id) ON DELETE CASCADE,
    document_title VARCHAR(300),
    chunk_index INT,
    content TEXT,
    allowed_role_ids TEXT[] DEFAULT '{}',
    visibility_scope VARCHAR(50) DEFAULT 'ROLE_SCOPED',
    department VARCHAR(100) DEFAULT 'engineering',
    classification_level INT DEFAULT 1,
    embedding vector(768),
    source_reference VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS conversations (
    id VARCHAR(100) PRIMARY KEY,
    tenant_id VARCHAR(100) REFERENCES tenants(id),
    user_id VARCHAR(100) REFERENCES users(id),
    title VARCHAR(300),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS messages (
    id VARCHAR(100) PRIMARY KEY,
    conversation_id VARCHAR(100) REFERENCES conversations(id) ON DELETE CASCADE,
    tenant_id VARCHAR(100) REFERENCES tenants(id),
    user_id VARCHAR(100) REFERENCES users(id),
    sender VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    sources JSONB DEFAULT '[]',
    latency_ms FLOAT DEFAULT 0.0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id VARCHAR(100) PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tenant_id VARCHAR(100),
    user_id VARCHAR(100),
    user_role VARCHAR(100),
    action VARCHAR(100),
    resource VARCHAR(300),
    decision VARCHAR(50),
    reason TEXT,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS service_requests (
    id VARCHAR(100) PRIMARY KEY,
    company_name VARCHAR(200),
    contact_name VARCHAR(200),
    contact_email VARCHAR(200),
    contact_phone VARCHAR(100),
    target_users_count VARCHAR(50),
    deployment_type VARCHAR(100),
    billing_discussion VARCHAR(100),
    selected_models JSONB DEFAULT '[]',
    selected_database VARCHAR(100),
    requirements_note TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw 
ON document_chunks USING hnsw (embedding vector_cosine_ops);
"""

class PostgresVectorDatabase:
    """
    PostgreSQL 16 + pgvector Database Engine with Row-Level Security (RLS)
    (Research Paper Sections IV.B, IV.F, and References [18], [19])
    """
    def __init__(self, db_url: str = DATABASE_URL):
        self.db_url = db_url
        self._pool = None
        self.is_connected = False

    def init_db(self) -> bool:
        """Initialize schema and verify connectivity"""
        try:
            import psycopg2
            conn = psycopg2.connect(self.db_url)
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(SCHEMA_SQL)
                # Enable Row Level Security (RLS)
                cur.execute("ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;")
                cur.execute("ALTER TABLE documents ENABLE ROW LEVEL SECURITY;")
                cur.execute("ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;")
                cur.execute("ALTER TABLE messages ENABLE ROW LEVEL SECURITY;")
            conn.close()
            self.is_connected = True
            logger.info("[PostgresVectorDB] PostgreSQL 16 + pgvector schema initialized with RLS.")
            return True
        except Exception as e:
            logger.warning(f"[PostgresVectorDB] Connection to PostgreSQL unavailable: {e}. Using resilient in-memory fallback.")
            self.is_connected = False
            return False

    def query_vector_similarity(
        self,
        tenant_id: str,
        user_role: str,
        department: str,
        clearance_level: int,
        query_vector: List[float],
        top_k: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Execute pre-retrieval vector similarity query in PostgreSQL with RLS and ABAC
        (Section IV.F Conjunctions of vector similarity with tenant, dept, and role)
        """
        if not self.is_connected:
            return []
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            conn = psycopg2.connect(self.db_url)
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Set transaction-scoped tenant isolation (NIST SP 800-207 Zero-Trust)
                cur.execute("SET LOCAL app.current_tenant = %s;", (tenant_id,))
                
                # Execute conjunction of vector cosine distance and role/dept/clearance filter
                sql = """
                SELECT id, document_id, document_title, chunk_index, content, 
                       visibility_scope, allowed_role_ids, department, classification_level,
                       1 - (embedding <=> %s::vector) AS similarity
                FROM document_chunks
                WHERE tenant_id = %s
                  AND classification_level <= %s
                  AND (visibility_scope = 'ALL_TENANT_EMPLOYEES' OR %s = ANY(allowed_role_ids) OR %s = 'admin')
                  AND (department = 'general' OR department = %s OR %s = 'admin')
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
                """
                vec_str = f"[{','.join(str(x) for x in query_vector)}]"
                cur.execute(sql, (
                    vec_str, tenant_id, clearance_level, user_role, user_role,
                    department, user_role, vec_str, top_k
                ))
                rows = cur.fetchall()
                conn.close()
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"[PostgresVectorDB] Query failed: {e}")
            return []

pg_db = PostgresVectorDatabase()
