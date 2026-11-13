import json
import os
import uuid
from typing import List, Dict, Any, Optional
from .models import Tenant, Role, User, Document, DocumentChunk, AuditLog, ServiceRequestCreate
from .config import DATABASE_PATH, AUDIT_LOGS_PATH, REQUESTS_PATH

class SentinelDatabase:
    def __init__(self):
        self.tenants: Dict[str, Tenant] = {}
        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}
        self.documents: Dict[str, Document] = {}
        self.chunks: List[DocumentChunk] = []
        self.audit_logs: List[AuditLog] = []
        self.service_requests: List[Dict[str, Any]] = []
        self._load_or_seed()

    def _load_or_seed(self):
        # Force reseed to populate Nexus and Amazon cleanly
        if os.path.exists(DATABASE_PATH):
            try:
                with open(DATABASE_PATH, "r") as f:
                    data = json.load(f)
                    tenants_data = data.get("tenants", [])
                    slugs = [t.get("slug") for t in tenants_data]
                    if "nexus" in slugs and "amazon" in slugs:
                        for t in tenants_data:
                            self.tenants[t["id"]] = Tenant(**t)
                        for r in data.get("roles", []):
                            self.roles[r["id"]] = Role(**r)
                        for u in data.get("users", []):
                            self.users[u["id"]] = User(**u)
                        for d in data.get("documents", []):
                            self.documents[d["id"]] = Document(**d)
                        for c in data.get("chunks", []):
                            self.chunks.append(DocumentChunk(**c))
                        return
            except Exception as e:
                print(f"[SentinelDB] Failed to load cached DB: {e}. Seeding fresh.")
        
        self._seed_default_data()

        # Load audit logs
        if os.path.exists(AUDIT_LOGS_PATH):
            try:
                with open(AUDIT_LOGS_PATH, "r") as f:
                    logs = json.load(f)
                    self.audit_logs = [AuditLog(**l) for l in logs]
            except Exception:
                pass

        # Load service requests
        if os.path.exists(REQUESTS_PATH):
            try:
                with open(REQUESTS_PATH, "r") as f:
                    self.service_requests = json.load(f)
            except Exception:
                pass

    def save(self):
        """Persist state to disk safely"""
        try:
            data = {
                "tenants": [t.dict() for t in self.tenants.values()],
                "roles": [r.dict() for r in self.roles.values()],
                "users": [u.dict() for u in self.users.values()],
                "documents": [d.dict() for d in self.documents.values()],
                "chunks": [c.dict() for c in self.chunks],
            }
            with open(DATABASE_PATH, "w") as f:
                json.dump(data, f, indent=2)

            with open(AUDIT_LOGS_PATH, "w") as f:
                json.dump([l.dict() for l in self.audit_logs], f, indent=2)

            with open(REQUESTS_PATH, "w") as f:
                json.dump(self.service_requests, f, indent=2)
        except Exception as e:
            print(f"[SentinelDB] Error saving data: {e}")

    def add_audit_log(self, tenant_id: str, user_id: str, user_role: str, action: str, resource: str, decision: str, reason: str, metadata: Dict[str, Any] = None):
        log = AuditLog(
            tenant_id=tenant_id,
            user_id=user_id,
            user_role=user_role,
            action=action,
            resource=resource,
            decision=decision,
            reason=reason,
            metadata=metadata or {}
        )
        self.audit_logs.insert(0, log)
        if len(self.audit_logs) > 200:
            self.audit_logs = self.audit_logs[:200]
        self.save()
        return log

    def add_service_request(self, req: ServiceRequestCreate) -> Dict[str, Any]:
        req_id = f"SRV_{uuid.uuid4().hex[:8].upper()}"
        item = req.dict()
        item["id"] = req_id
        item["status"] = "SUBMITTED"
        item["created_at"] = str(uuid.uuid1())
        self.service_requests.insert(0, item)
        self.save()
        return item

    def _seed_default_data(self):
        print("[SentinelDB] Initializing enterprise multi-tenant environment (Nexus & Amazon x 4 Roles)...")
        self.tenants.clear()
        self.roles.clear()
        self.users.clear()
        self.documents.clear()
        self.chunks.clear()

        # ----------------------------------------------------
        # Company 1: Nexus (Enterprise AI & Autonomous Systems)
        # ----------------------------------------------------
        t_nexus = Tenant(
            id="tenant_nexus",
            name="Nexus",
            slug="nexus",
            description="Autonomous AI infrastructure, zero-trust cloud orchestration, and deep-tech security systems.",
            domain="nexus.internal"
        )
        self.tenants[t_nexus.id] = t_nexus

        # 4 Roles for Nexus
        roles_nexus = [
            Role(id="role_nexus_admin", tenant_id=t_nexus.id, name="Tenant Administrator", slug="admin", description="Full administrative authority over Nexus documents, employee memberships, and security policies.", is_admin=True),
            Role(id="role_nexus_tech", tenant_id=t_nexus.id, name="Tech Employee", slug="tech", description="Engineering standards, workstation encryption, SSH key rotation, and production infrastructure.", is_admin=False),
            Role(id="role_nexus_finance", tenant_id=t_nexus.id, name="Finance Employee", slug="finance", description="Nexus corporate expense policy, travel per diem ($120 domestic), and CFO approvals.", is_admin=False),
            Role(id="role_nexus_analyst", tenant_id=t_nexus.id, name="Business Analyst", slug="analyst", description="Market intelligence, enterprise ARR metrics (34.2% YoY), customer churn, and KPIs.", is_admin=False)
        ]
        for r in roles_nexus:
            self.roles[r.id] = r

        # 4 Seed Users for Nexus
        users_nexus = [
            User(id="user_nexus_admin", tenant_id=t_nexus.id, name="Elena Rostova", email="elena.admin@nexus.internal", role_id="role_nexus_admin", role_name="Tenant Administrator", is_admin=True),
            User(id="user_nexus_tech", tenant_id=t_nexus.id, name="Devon Vance", email="devon.tech@nexus.internal", role_id="role_nexus_tech", role_name="Tech Employee", is_admin=False),
            User(id="user_nexus_finance", tenant_id=t_nexus.id, name="Marcus Sterling", email="marcus.finance@nexus.internal", role_id="role_nexus_finance", role_name="Finance Employee", is_admin=False),
            User(id="user_nexus_analyst", tenant_id=t_nexus.id, name="Sarah Chen", email="sarah.analyst@nexus.internal", role_id="role_nexus_analyst", role_name="Business Analyst", is_admin=False)
        ]
        for u in users_nexus:
            self.users[u.id] = u

        # ----------------------------------------------------
        # Company 2: Amazon (Global Cloud & Commerce Infrastructure)
        # ----------------------------------------------------
        t_amazon = Tenant(
            id="tenant_amazon",
            name="Amazon",
            slug="amazon",
            description="Global cloud infrastructure (AWS), enterprise logistics, and hyper-scale distributed services.",
            domain="amazon.internal"
        )
        self.tenants[t_amazon.id] = t_amazon

        # 4 Roles for Amazon
        roles_amazon = [
            Role(id="role_amazon_admin", tenant_id=t_amazon.id, name="Tenant Administrator", slug="admin", description="Full administrative oversight for Amazon corporate tenant, IAM roles, and vector storage.", is_admin=True),
            Role(id="role_amazon_tech", tenant_id=t_amazon.id, name="Tech Employee", slug="tech", description="AWS cloud architecture, hardened Linux AMI deployment, VPC peering, and KMS keys.", is_admin=False),
            Role(id="role_amazon_finance", tenant_id=t_amazon.id, name="Finance Employee", slug="finance", description="Amazon global travel policy ($250 hotel limit, $95/day meal cap), Concur expense submissions.", is_admin=False),
            Role(id="role_amazon_analyst", tenant_id=t_amazon.id, name="Business Analyst", slug="analyst", description="AWS cloud services market share telemetry, fulfillment efficiency, and quarterly margin analysis.", is_admin=False)
        ]
        for r in roles_amazon:
            self.roles[r.id] = r

        # 4 Seed Users for Amazon
        users_amazon = [
            User(id="user_amazon_admin", tenant_id=t_amazon.id, name="David Miller", email="david.admin@amazon.internal", role_id="role_amazon_admin", role_name="Tenant Administrator", is_admin=True),
            User(id="user_amazon_tech", tenant_id=t_amazon.id, name="Kaelen Ross", email="kaelen.tech@amazon.internal", role_id="role_amazon_tech", role_name="Tech Employee", is_admin=False),
            User(id="user_amazon_finance", tenant_id=t_amazon.id, name="Chloe Dupont", email="chloe.finance@amazon.internal", role_id="role_amazon_finance", role_name="Finance Employee", is_admin=False),
            User(id="user_amazon_analyst", tenant_id=t_amazon.id, name="Tariq Mansoor", email="tariq.analyst@amazon.internal", role_id="role_amazon_analyst", role_name="Business Analyst", is_admin=False)
        ]
        for u in users_amazon:
            self.users[u.id] = u

        # ----------------------------------------------------
        # Seed Documents for Nexus
        # ----------------------------------------------------
        doc_nexus_tech = Document(
            id="doc_nexus_tech_01",
            tenant_id=t_nexus.id,
            title="Nexus Tech: Workstation Encryption & SSH Security Protocol",
            description="Mandatory 256-bit AES disk encryption, Ed25519 SSH hardware keys, and non-root Docker host requirements.",
            file_name="nexus_workstation_security_protocol.pdf",
            file_type="application/pdf",
            uploaded_by="user_nexus_admin",
            allowed_role_ids=["role_nexus_tech", "tech"],
            visibility_scope="ROLE_SCOPED",
            status="INDEXED"
        )
        self.documents[doc_nexus_tech.id] = doc_nexus_tech

        doc_nexus_fin = Document(
            id="doc_nexus_fin_02",
            tenant_id=t_nexus.id,
            title="Nexus Finance: Corporate Expense & Travel Reimbursement Policy",
            description="Daily meal per diem rate ($120.00 USD domestic, $160.00 international), receipt submission within 30 days, CFO sign-off for expenses over $5,000.",
            file_name="nexus_corporate_reimbursement_2026.docx",
            file_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            uploaded_by="user_nexus_admin",
            allowed_role_ids=["role_nexus_finance", "finance"],
            visibility_scope="ROLE_SCOPED",
            status="INDEXED"
        )
        self.documents[doc_nexus_fin.id] = doc_nexus_fin

        doc_nexus_analyst = Document(
            id="doc_nexus_ba_03",
            tenant_id=t_nexus.id,
            title="Nexus Business: Q3 Enterprise ARR Growth & Market Retentions",
            description="Enterprise ARR expanded by 34.2% YoY to $48.5M, customer churn dropped to 1.8%, APAC payment expansion targets.",
            file_name="nexus_q3_market_analysis.pdf",
            file_type="application/pdf",
            uploaded_by="user_nexus_admin",
            allowed_role_ids=["role_nexus_analyst", "analyst"],
            visibility_scope="ROLE_SCOPED",
            status="INDEXED"
        )
        self.documents[doc_nexus_analyst.id] = doc_nexus_analyst

        doc_nexus_all = Document(
            id="doc_nexus_all_04",
            tenant_id=t_nexus.id,
            title="Nexus General: Enterprise Code of Conduct & Workplace Protocol",
            description="Core working hours (09:00 - 17:00), equal opportunity workplace, and 24/7 confidential ethics hotline (800-555-NEXUS-ETHICS).",
            file_name="nexus_code_of_conduct_global.pdf",
            file_type="application/pdf",
            uploaded_by="user_nexus_admin",
            allowed_role_ids=["ALL_TENANT_EMPLOYEES"],
            visibility_scope="ALL_TENANT_EMPLOYEES",
            status="INDEXED"
        )
        self.documents[doc_nexus_all.id] = doc_nexus_all

        # ----------------------------------------------------
        # Seed Documents for Amazon
        # ----------------------------------------------------
        doc_amz_tech = Document(
            id="doc_amazon_tech_01",
            tenant_id=t_amazon.id,
            title="Amazon Tech: AWS Cloud Architecture & Zero-Trust IAM Policy",
            description="Least-privilege IAM policies, mutual TLS across VPC peering connections, Amazon Linux 2023 hardened images, and HashiCorp Vault secrets.",
            file_name="amazon_aws_architecture_standards.pdf",
            file_type="application/pdf",
            uploaded_by="user_amazon_admin",
            allowed_role_ids=["role_amazon_tech", "tech"],
            visibility_scope="ROLE_SCOPED",
            status="INDEXED"
        )
        self.documents[doc_amz_tech.id] = doc_amz_tech

        doc_amz_fin = Document(
            id="doc_amazon_fin_02",
            tenant_id=t_amazon.id,
            title="Amazon Finance: Corporate Travel & Concur Expense Guidelines",
            description="Amazon daily hotel rate cap ($250.00 USD/night), daily meal reimbursement limit ($95.00 USD/day), Director approval for expenses exceeding $10,000, 14-day Concur filing window.",
            file_name="amazon_global_travel_policy_2026.docx",
            file_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            uploaded_by="user_amazon_admin",
            allowed_role_ids=["role_amazon_finance", "finance"],
            visibility_scope="ROLE_SCOPED",
            status="INDEXED"
        )
        self.documents[doc_amz_fin.id] = doc_amz_fin

        doc_amz_analyst = Document(
            id="doc_amazon_ba_03",
            tenant_id=t_amazon.id,
            title="Amazon Business: Cloud Services Market Share & Fulfillment Metrics",
            description="AWS cloud computing revenue grew 19.4% YoY with an operating margin of 31.2%. Customer commitments in generative AI compute clusters accounted for $4.2B in annualized backlog growth.",
            file_name="amazon_cloud_market_share_q3.pdf",
            file_type="application/pdf",
            uploaded_by="user_amazon_admin",
            allowed_role_ids=["role_amazon_analyst", "analyst"],
            visibility_scope="ROLE_SCOPED",
            status="INDEXED"
        )
        self.documents[doc_amz_analyst.id] = doc_amz_analyst

        doc_amz_all = Document(
            id="doc_amazon_all_04",
            tenant_id=t_amazon.id,
            title="Amazon General: Leadership Principles & Workplace Safety Manual",
            description="Customer Obsession, Ownership, Frugality, fulfillment center safety rules, and confidential employee helpline (800-AMZ-ETHIC).",
            file_name="amazon_leadership_principles_safety.pdf",
            file_type="application/pdf",
            uploaded_by="user_amazon_admin",
            allowed_role_ids=["ALL_TENANT_EMPLOYEES"],
            visibility_scope="ALL_TENANT_EMPLOYEES",
            status="INDEXED"
        )
        self.documents[doc_amz_all.id] = doc_amz_all

        # ----------------------------------------------------
        # Seed Chunks for All Documents
        # ----------------------------------------------------
        seed_chunks_definitions = [
            # Nexus Tech
            (doc_nexus_tech, 1, "Nexus Laptop Security: All employee workstations must run full-disk encryption (FileVault on macOS or BitLocker on Windows) with 256-bit AES. Screen lock timeout is mandatory after 3 minutes of inactivity. USB mass storage devices are strictly disabled by endpoint management agent."),
            (doc_nexus_tech, 2, "Nexus Engineering Infrastructure: SSH keys for cloud instances must use Ed25519 with hardware security keys (YubiKey). Direct root login to production servers is strictly forbidden. All Docker containers must run as unprivileged non-root users."),
            # Nexus Finance
            (doc_nexus_fin, 1, "Nexus Corporate Expense Policy: The business travel daily meal per diem rate is set at $120.00 USD for domestic travel and $160.00 USD for international trips. Alcohol is non-reimbursable without explicit director pre-authorization."),
            (doc_nexus_fin, 2, "Nexus Reimbursement Submission: Expense reports must be submitted within 30 calendar days of expense occurrence via the finance portal with itemized digital receipts attached. Expenses exceeding $5,000 require written CFO sign-off prior to reimbursement."),
            # Nexus Analyst
            (doc_nexus_analyst, 1, "Nexus Market Intelligence Q3: Enterprise annual recurring revenue (ARR) grew by 34.2% YoY, reaching $48.5M. Customer churn decreased from 2.4% to 1.8% following the deployment of automated payment reconciliation tools."),
            (doc_nexus_analyst, 2, "Nexus Expansion Strategy: Target verticals for Q4 include Tier-2 commercial banks and enterprise neo-brokers. Projected TAM in APAC payment infrastructure is estimated at $12.4B over the next 36 months."),
            # Nexus All
            (doc_nexus_all, 1, "Nexus Enterprise Code of Conduct: Core working hours are 09:00 to 17:00 local time with flexible lunch breaks. The company strictly enforces zero tolerance for discrimination, workplace bullying, or sexual harassment."),
            (doc_nexus_all, 2, "Nexus Whistleblower Protection: Employees can report ethical violations, financial misconduct, or compliance breaches confidentially 24/7 via the anonymous hotline (800-555-NEXUS-ETHICS) without fear of reprisal."),

            # Amazon Tech
            (doc_amz_tech, 1, "Amazon AWS Cloud Architecture: All cloud resources must enforce strict IAM least privilege. Cross-account access requires AWS STS AssumeRole with external ID verification. Interservice VPC traffic without mutual TLS (mTLS) is rejected at the security group ingress."),
            (doc_amz_tech, 2, "Amazon Production Security: All EC2 instances must boot from signed Amazon Linux 2023 hardened AMIs. SSH access is prohibited; all node diagnostics are performed via AWS Systems Manager Session Manager with cryptographic session audit trails."),
            # Amazon Finance
            (doc_amz_fin, 1, "Amazon Global Travel Policy: Hotel lodging reimbursements are strictly capped at $250.00 USD per night for standard tier cities ($320 for high-cost metros). The maximum allowable daily meal reimbursement is $95.00 USD per day with itemized receipts."),
            (doc_amz_fin, 2, "Amazon Expense Approvals: All expense reports must be submitted through Concur within 14 business days of trip conclusion. Any cumulative expense report exceeding $10,000.00 USD requires Senior Director and VP of Finance approval prior to disbursement."),
            # Amazon Analyst
            (doc_amz_analyst, 1, "Amazon Cloud Market Share Q3: AWS cloud revenue grew 19.4% YoY with an operating margin of 31.2%. Customer commitments in generative AI compute clusters accounted for $4.2B in annualized backlog growth."),
            (doc_amz_analyst, 2, "Amazon Fulfillment Logistics: Regionalized fulfillment network optimization delivered a 14% improvement in same-day delivery throughput while reducing per-unit transportation costs across North America."),
            # Amazon All
            (doc_amz_all, 1, "Amazon Leadership Principles: Leaders have conviction and are tenacious. They do not compromise for the sake of social cohesion. Customer Obsession: Leaders start with the customer and work backwards."),
            (doc_amz_all, 2, "Amazon Workplace Safety & Integrity: Zero tolerance for workplace hazards or retaliatory conduct. Concerns can be escalated 24/7 through the anonymous Ethics & Compliance Helpline at 800-AMZ-ETHIC.")
        ]

        for doc, idx, text in seed_chunks_definitions:
            chunk = DocumentChunk(
                id=f"chk_{doc.id}_{idx}",
                tenant_id=doc.tenant_id,
                document_id=doc.id,
                document_title=doc.title,
                chunk_index=idx,
                content=text,
                allowed_role_ids=doc.allowed_role_ids,
                visibility_scope=doc.visibility_scope,
                source_reference=f"Section {idx}.0"
            )
            self.chunks.append(chunk)

        # Update chunk counts on documents
        for d in self.documents.values():
            d.chunks_count = len([c for c in self.chunks if c.document_id == d.id])

        # Initial audit logs
        self.add_audit_log(
            tenant_id=t_nexus.id,
            user_id="user_nexus_admin",
            user_role="admin",
            action="INGEST_DOCUMENT",
            resource=doc_nexus_tech.title,
            decision="INGESTED",
            reason="Nexus workstation security standards indexed for 'tech' role.",
            metadata={"chunks": 2, "scope": "ROLE_SCOPED"}
        )
        self.add_audit_log(
            tenant_id=t_amazon.id,
            user_id="user_amazon_admin",
            user_role="admin",
            action="INGEST_DOCUMENT",
            resource=doc_amz_tech.title,
            decision="INGESTED",
            reason="Amazon AWS security standards indexed for 'tech' role.",
            metadata={"chunks": 2, "scope": "ROLE_SCOPED"}
        )

        self.save()
        print(f"[SentinelDB] Seed complete. {len(self.tenants)} tenants (Nexus, Amazon), {len(self.roles)} roles, {len(self.users)} users, {len(self.documents)} documents, {len(self.chunks)} chunks.")

db = SentinelDatabase()
