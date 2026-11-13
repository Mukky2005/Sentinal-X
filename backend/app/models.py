from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class Tenant(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    domain: str
    active: bool = True

class Role(BaseModel):
    id: str
    tenant_id: str
    name: str
    slug: str
    description: str
    is_admin: bool = False
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class User(BaseModel):
    id: str
    tenant_id: str
    name: str
    email: str
    role_id: str
    role_name: str
    department: str = "engineering" # ABAC Department attribute
    clearance_level: int = 1         # ABAC Clearance level (1=Public, 2=Internal, 3=Confidential, 4=Restricted)
    is_admin: bool = False
    active: bool = True

class DocumentChunk(BaseModel):
    id: str = Field(default_factory=lambda: f"chunk_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    document_id: str
    document_title: str
    chunk_index: int
    content: str
    allowed_role_ids: List[str]
    visibility_scope: str # "ROLE_SCOPED" or "ALL_TENANT_EMPLOYEES"
    department: str = "general" # ABAC Department attribute
    classification_level: int = 1 # ABAC Classification level
    embedding: Optional[List[float]] = None
    source_reference: Optional[str] = None

class Document(BaseModel):
    id: str
    tenant_id: str
    title: str
    description: str
    file_name: str
    file_type: str
    uploaded_by: str
    uploaded_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    allowed_role_ids: List[str]
    visibility_scope: str # "ROLE_SCOPED" or "ALL_TENANT_EMPLOYEES"
    department: str = "general" # ABAC Department attribute
    classification_level: int = 1 # ABAC Classification level
    version: str = "1.0"
    chunks_count: int = 0
    status: str = "INDEXED" # "PENDING", "PROCESSING", "INDEXED", "FAILED"

class ConversationMessage(BaseModel):
    id: str = Field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:10]}")
    conversation_id: str
    tenant_id: str
    user_id: str
    sender: str # "user" or "assistant"
    content: str
    sources: List[Dict[str, Any]] = []
    latency_ms: float = 0.0
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: f"conv_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    user_id: str
    title: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    messages: List[ConversationMessage] = []

class QueryRequest(BaseModel):
    tenant_id: str
    user_id: str
    query: str
    conversation_id: Optional[str] = None

class SecurityTraceStep(BaseModel):
    stage: str
    status: str # "PASS", "FLAGGED", "BLOCKED", "INFO", "ISOLATED"
    detail: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class QueryResponse(BaseModel):
    answer: str
    status: str # "SUCCESS", "REJECTED_UNAUTHORIZED", "BLOCKED_INJECTION", "NO_AUTHORIZED_EVIDENCE"
    sources: List[Dict[str, Any]] = []
    authorized_chunks_count: int = 0
    total_tenant_chunks_evaluated: int = 0
    denied_chunks_count: int = 0
    security_traces: List[SecurityTraceStep] = []
    model_used: str
    latency_ms: float
    conversation_id: Optional[str] = None

class AuditLog(BaseModel):
    id: str = Field(default_factory=lambda: f"audit_{uuid.uuid4().hex[:12]}")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    tenant_id: str
    user_id: str
    user_role: str
    action: str
    resource: str
    decision: str # "ALLOWED", "DENIED", "BLOCKED", "INGESTED"
    reason: str
    metadata: Dict[str, Any] = {}

class ServiceRequestCreate(BaseModel):
    company_name: str
    contact_name: str
    contact_email: str
    contact_phone: Optional[str] = ""
    target_users_count: Optional[str] = "100-500"
    deployment_type: str = "DEDICATED_POSTGRES"
    billing_discussion: str = "CUSTOM_ENTERPRISE"
    selected_models: List[str] = ["llama3.2", "nomic-embed-text"]
    selected_database: str = "PostgreSQL + pgvector"
    requirements_note: Optional[str] = ""

class AuthLoginRequest(BaseModel):
    email: str
    tenant_id: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User
