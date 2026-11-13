from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import uuid
import time

from .models import (
    Tenant, Role, User, Document, DocumentChunk,
    QueryRequest, QueryResponse, AuditLog, ServiceRequestCreate
)
from .database import db
from .rag_engine import SentinelRAGEngine
from .config import PORT, HOST

app = FastAPI(
    title="Sentinel-X — Enterprise Knowledge Engine",
    description="A Layered Security Framework for Multi-Tenant Enterprise Knowledge Retrieval",
    version="1.0.0"
)

# Enable CORS for local dev frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_engine = SentinelRAGEngine()

# ----------------------------------------------------
# System & Infrastructure Endpoints
# ----------------------------------------------------
@app.get("/api/health")
async def health_check():
    ollama_info = await rag_engine.check_ollama()
    return {
        "status": "HEALTHY",
        "system": "Sentinel-X Enterprise Platform",
        "version": "1.0.0-MVP",
        "architecture": "Layered Multi-Tenant Security Framework",
        "tenants_count": len(db.tenants),
        "total_documents": len(db.documents),
        "total_chunks_indexed": len(db.chunks),
        "vector_engine": "pgvector / Cosine Projection Engine",
        "ollama": ollama_info
    }

@app.get("/api/infrastructure")
async def get_infrastructure_specs():
    ollama_info = await rag_engine.check_ollama()
    return {
        "local_models": [
            {
                "name": "llama3.2:latest",
                "type": "Chat & Reasoning LLM",
                "size": "2.0 GB",
                "status": "Available in Ollama" if ollama_info["online"] else "Configured",
                "description": "Primary local conversational model for authorized context synthesis."
            },
            {
                "name": "nomic-embed-text:latest",
                "type": "High-Dimensional Vector Embeddings",
                "size": "274 MB",
                "status": "Available in Ollama" if ollama_info["online"] else "Configured",
                "description": "Dense passage retriever generating 768-dim embeddings for tenant chunks."
            },
            {
                "name": "gemma4:12b",
                "type": "High-Capacity Reasoning Engine",
                "size": "7.7 GB",
                "status": "Available in Ollama" if ollama_info["online"] else "Configured",
                "description": "Secondary local model for complex policy cross-referencing and summarization."
            }
        ],
        "database": {
            "engine": "PostgreSQL 16 + pgvector",
            "isolation": "Tenant-Isolated Namespaces / Dedicated RLS Schemes",
            "retrieval_rule": "Pre-LLM DB Gate: WHERE tenant_id = ? AND (role = ? OR scope = 'ALL')"
        },
        "standards": [
            "NIST SP 800-207 Zero-Trust Architecture",
            "OAuth 2.0 RFC 9700 Security Best Current Practice",
            "OWASP Top 10 for LLMs (Indirect Prompt Injection Defense)",
            "SafeRAG & PoisonedRAG Adversarial Isolation"
        ]
    }

# ----------------------------------------------------
# Tenant Endpoints
# ----------------------------------------------------
@app.get("/api/tenants", response_model=List[Tenant])
def list_tenants():
    return list(db.tenants.values())

@app.get("/api/tenants/{tenant_id}", response_model=Tenant)
def get_tenant(tenant_id: str):
    if tenant_id not in db.tenants:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db.tenants[tenant_id]

# ----------------------------------------------------
# Roles Endpoints (4 roles per company)
# ----------------------------------------------------
@app.get("/api/roles", response_model=List[Role])
def list_roles(tenant_id: Optional[str] = None):
    if tenant_id:
        return [r for r in db.roles.values() if r.tenant_id == tenant_id]
    return list(db.roles.values())

@app.post("/api/roles", response_model=Role)
def create_role(tenant_id: str, name: str, slug: str, description: str):
    if tenant_id not in db.tenants:
        raise HTTPException(status_code=404, detail="Tenant not found")
    role_id = f"role_{tenant_id}_{slug}_{uuid.uuid4().hex[:4]}"
    new_role = Role(
        id=role_id,
        tenant_id=tenant_id,
        name=name,
        slug=slug,
        description=description,
        is_admin=False
    )
    db.roles[role_id] = new_role
    db.save()
    db.add_audit_log(
        tenant_id=tenant_id,
        user_id="admin",
        user_role="admin",
        action="CREATE_ROLE",
        resource=name,
        decision="ALLOWED",
        reason="Admin provisioned new custom tenant role.",
        metadata={"role_id": role_id, "slug": slug}
    )
    return new_role

# ----------------------------------------------------
# Employee / User Endpoints
# ----------------------------------------------------
@app.get("/api/employees", response_model=List[User])
def list_employees(tenant_id: Optional[str] = None):
    if tenant_id:
        return [u for u in db.users.values() if u.tenant_id == tenant_id]
    return list(db.users.values())

@app.post("/api/employees", response_model=User)
def create_employee(tenant_id: str, name: str, email: str, role_id: str):
    if tenant_id not in db.tenants:
        raise HTTPException(status_code=404, detail="Tenant not found")
    role = db.roles.get(role_id)
    if not role or role.tenant_id != tenant_id:
        raise HTTPException(status_code=400, detail="Invalid role for this tenant")
    
    user_id = f"user_{tenant_id}_{uuid.uuid4().hex[:6]}"
    user = User(
        id=user_id,
        tenant_id=tenant_id,
        name=name,
        email=email,
        role_id=role.id,
        role_name=role.name,
        is_admin=role.is_admin,
        active=True
    )
    db.users[user_id] = user
    db.save()
    db.add_audit_log(
        tenant_id=tenant_id,
        user_id="admin",
        user_role="admin",
        action="INVITE_EMPLOYEE",
        resource=email,
        decision="ALLOWED",
        reason=f"Assigned to role '{role.name}'.",
        metadata={"user_id": user_id, "role": role.slug}
    )
    return user

@app.put("/api/employees/{user_id}/role", response_model=User)
def update_employee_role(user_id: str, new_role_id: str):
    user = db.users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_role = db.roles.get(new_role_id)
    if not new_role or new_role.tenant_id != user.tenant_id:
        raise HTTPException(status_code=400, detail="Invalid role for user's tenant")
    
    old_role_name = user.role_name
    user.role_id = new_role.id
    user.role_name = new_role.name
    user.is_admin = new_role.is_admin
    db.save()
    db.add_audit_log(
        tenant_id=user.tenant_id,
        user_id=user.id,
        user_role="admin",
        action="UPDATE_USER_ROLE",
        resource=user.name,
        decision="ALLOWED",
        reason=f"Role changed from '{old_role_name}' to '{new_role.name}'. Immediate retrieval filter update applied.",
        metadata={"old_role": old_role_name, "new_role": new_role.name}
    )
    return user

# ----------------------------------------------------
# Document Ingestion & Management Endpoints
# ----------------------------------------------------
@app.get("/api/documents", response_model=List[Document])
def list_documents(tenant_id: Optional[str] = None):
    if tenant_id:
        return [d for d in db.documents.values() if d.tenant_id == tenant_id]
    return list(db.documents.values())

@app.post("/api/documents")
async def upload_document(
    tenant_id: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    allowed_roles: str = Form(...), # comma-separated or "ALL"
    uploaded_by: str = Form("admin")
):
    if tenant_id not in db.tenants:
        raise HTTPException(status_code=404, detail="Tenant not found")

    file_name = file.filename if file else f"{title.lower().replace(' ', '_')[:30]}.txt"
    file_type = file.content_type if file and file.content_type else "text/plain"

    if not content and file:
        file_bytes = await file.read()
        try:
            content = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            content = file_bytes.decode("latin-1", errors="ignore")

    if not content or not content.strip():
        raise HTTPException(status_code=400, detail="Document file content cannot be empty")

    roles_list = [r.strip() for r in allowed_roles.split(",") if r.strip()]
    visibility_scope = "ALL_TENANT_EMPLOYEES" if "ALL" in roles_list or "ALL_TENANT_EMPLOYEES" in roles_list else "ROLE_SCOPED"

    doc_id = f"doc_{tenant_id}_{uuid.uuid4().hex[:8]}"
    doc = Document(
        id=doc_id,
        tenant_id=tenant_id,
        title=title,
        description=description,
        file_name=file_name,
        file_type=file_type,
        uploaded_by=uploaded_by,
        allowed_role_ids=roles_list,
        visibility_scope=visibility_scope,
        status="INDEXED"
    )

    # Deterministic chunking
    chunks_text = rag_engine.chunk_text(content)
    new_chunks = []
    for idx, c_text in enumerate(chunks_text, start=1):
        emb = await rag_engine.get_embedding(c_text)
        chunk = DocumentChunk(
            id=f"chk_{doc_id}_{idx}",
            tenant_id=tenant_id,
            document_id=doc_id,
            document_title=title,
            chunk_index=idx,
            content=c_text,
            allowed_role_ids=roles_list,
            visibility_scope=visibility_scope,
            embedding=emb,
            source_reference=f"Section {idx}.0"
        )
        new_chunks.append(chunk)

    doc.chunks_count = len(new_chunks)
    db.documents[doc_id] = doc
    db.chunks.extend(new_chunks)
    db.save()

    db.add_audit_log(
        tenant_id=tenant_id,
        user_id=uploaded_by,
        user_role="admin",
        action="INGEST_DOCUMENT",
        resource=title,
        decision="INGESTED",
        reason=f"Document chunked into {len(new_chunks)} vectors with scope: {visibility_scope}.",
        metadata={"doc_id": doc_id, "roles": roles_list, "chunks": len(new_chunks)}
    )

    return {"status": "SUCCESS", "document": doc, "chunks_created": len(new_chunks)}

@app.delete("/api/documents/{doc_id}")
def delete_document(doc_id: str):
    doc = db.documents.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Invalidate chunks
    db.chunks = [c for c in db.chunks if c.document_id != doc_id]
    del db.documents[doc_id]
    db.save()

    db.add_audit_log(
        tenant_id=doc.tenant_id,
        user_id="admin",
        user_role="admin",
        action="DELETE_DOCUMENT",
        resource=doc.title,
        decision="ALLOWED",
        reason="Document removed; all associated vector chunks immediately purged from retrieval index.",
        metadata={"doc_id": doc_id}
    )
    return {"status": "DELETED", "document_id": doc_id}

# ----------------------------------------------------
# Role-Constrained RAG Query Endpoint
# ----------------------------------------------------
@app.post("/api/chat/query", response_model=QueryResponse)
async def query_knowledge_base(req: QueryRequest):
    # Verify tenant & user exist (Server-side validation)
    tenant = db.tenants.get(req.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant does not exist")
    
    user = db.users.get(req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User account not found")
    
    if user.tenant_id != req.tenant_id:
        db.add_audit_log(
            tenant_id=req.tenant_id,
            user_id=user.id,
            user_role="unknown",
            action="CROSS_TENANT_ATTEMPT",
            resource="KnowledgeBase",
            decision="BLOCKED",
            reason="User attempted to query a tenant they are not registered to.",
            metadata={"user_tenant": user.tenant_id, "queried_tenant": req.tenant_id}
        )
        raise HTTPException(status_code=403, detail="Cross-tenant access violation blocked by Sentinel-X Gate.")

    # Determine role slug (e.g., 'tech', 'finance', 'analyst', 'admin')
    role_record = db.roles.get(user.role_id)
    user_role_slug = role_record.slug if role_record else "tech"
    if user.is_admin:
        user_role_slug = "admin"

    # Execute RAG query with strict DB gate
    response = await rag_engine.execute_query(
        query=req.query,
        user_id=user.id,
        user_role=user_role_slug,
        user_tenant=user.tenant_id,
        all_chunks=db.chunks
    )

    # Structured audit logging
    decision = "ALLOWED" if response.status == "SUCCESS" else ("BLOCKED" if "BLOCKED" in response.status else "FILTERED")
    db.add_audit_log(
        tenant_id=user.tenant_id,
        user_id=user.id,
        user_role=user_role_slug,
        action="KNOWLEDGE_QUERY",
        resource=req.query[:60],
        decision=decision,
        reason=f"Status: {response.status}. Evaluated {response.total_tenant_chunks_evaluated} tenant chunks: {response.authorized_chunks_count} authorized, {response.denied_chunks_count} quarantined.",
        metadata={
            "status": response.status,
            "latency_ms": response.latency_ms,
            "sources_count": len(response.sources),
            "model": response.model_used
        }
    )

    return response

# ----------------------------------------------------
# Audit Logs Endpoints
# ----------------------------------------------------
@app.get("/api/audit/logs", response_model=List[AuditLog])
def get_audit_logs(tenant_id: Optional[str] = None):
    if tenant_id:
        return [l for l in db.audit_logs if l.tenant_id == tenant_id]
    return db.audit_logs

# ----------------------------------------------------
# Request a Service Endpoints
# ----------------------------------------------------
@app.post("/api/service/request")
def submit_service_request(req: ServiceRequestCreate):
    result = db.add_service_request(req)
    return {
        "status": "RECEIVED",
        "message": f"Deployment request received for {req.company_name}. A Sentinel-X Solutions Architect will contact {req.contact_name} ({req.contact_email}) within 24 business hours.",
        "request_details": result
    }

@app.get("/api/service/requests")
def list_service_requests():
    return db.service_requests

# ----------------------------------------------------
# Direct Run Entrypoint
# ----------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
