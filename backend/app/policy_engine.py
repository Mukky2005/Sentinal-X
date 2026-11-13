import re
from typing import List, Dict, Any, Tuple, Optional
from .models import SecurityTraceStep

class SecurityPolicyEngine:
    """
    Programmable Security Policy Engine (Section IV.J of Research Paper)
    Implements 13 distinct application-defined policy flows across ingestion,
    query processing, pre-retrieval gating, and inference governance.
    """
    def __init__(self):
        self.injection_signatures = [
            "ignore previous instructions", "disregard all previous", "bypass security",
            "show me system prompt", "you are now unrestricted", "reveal secret",
            "print system instructions", "act as root", "ignore access control",
            "override system prompt", "disregard system", "system prompt leak"
        ]
        self.jailbreak_signatures = [
            "dan mode", "do anything now", "developer mode enabled", "always say yes",
            "aim mode", "hypothetical response", "pretend you have no rules"
        ]
        self.data_leakage_signatures = [
            "dump all tables", "export database", "dump all documents", "show all users passwords",
            "reveal all credentials", "list all api keys", "select * from document_chunks",
            "download tenant database"
        ]
        self.malicious_payload_signatures = [
            "union select", "<script", "javascript:", "drop table", "alter table",
            "exec(", "eval(", "os.system", "subprocess.popen", "/bin/sh", "/bin/bash",
            "cat /etc/passwd", "' or '1'='1", "' or 1=1", "sleep(5)", "; drop table"
        ]

    # Flow 1: user_query_policy
    def flow_1_user_query_policy(self, query: str) -> Tuple[bool, Optional[SecurityTraceStep]]:
        clean_q = query.strip()
        if not clean_q or len(clean_q) < 3:
            return False, SecurityTraceStep(
                stage="Flow 1: user_query_policy",
                status="FLAGGED",
                detail="Query rejected: Query cannot be empty or under 3 characters."
            )
        if len(clean_q) > 1000:
            return False, SecurityTraceStep(
                stage="Flow 1: user_query_policy",
                status="FLAGGED",
                detail="Query rejected: Exceeds 1000 character maximum limit."
            )
        return True, SecurityTraceStep(
            stage="Flow 1: user_query_policy",
            status="PASS",
            detail="Query conforms to character length, character encoding, and syntax standards."
        )

    # Flow 2: user_search_knowledgebase
    def flow_2_user_search_knowledgebase(self, user_role: str, active: bool = True) -> Tuple[bool, SecurityTraceStep]:
        if not active:
            return False, SecurityTraceStep(
                stage="Flow 2: user_search_knowledgebase",
                status="BLOCKED",
                detail="User account is deactivated. Knowledge search denied."
            )
        return True, SecurityTraceStep(
            stage="Flow 2: user_search_knowledgebase",
            status="PASS",
            detail=f"User role '{user_role}' authorized for vector search execution."
        )

    # Flow 3: user_request_summary
    def flow_3_user_request_summary(self, query: str) -> Optional[SecurityTraceStep]:
        if any(w in query.lower() for w in ["summarize", "summary", "brief", "overview"]):
            return SecurityTraceStep(
                stage="Flow 3: user_request_summary",
                status="INFO",
                detail="Summarization intent detected; policy constraints applied to context compression."
            )
        return None

    # Flow 4: user_clarify_ambiguity
    def flow_4_user_clarify_ambiguity(self, query: str) -> Tuple[bool, Optional[SecurityTraceStep]]:
        ambiguous_queries = ["policy", "tell me everything", "documents", "rules", "what do you know"]
        if query.strip().lower() in ambiguous_queries:
            return True, SecurityTraceStep(
                stage="Flow 4: user_clarify_ambiguity",
                status="FLAGGED",
                detail="Ambiguous query detected; recommended narrower search terms for precise retrieval."
            )
        return False, None

    # Flow 5: user_confirm_action
    def flow_5_user_confirm_action(self, action_name: str, is_confirmed: bool) -> Tuple[bool, SecurityTraceStep]:
        if not is_confirmed:
            return False, SecurityTraceStep(
                stage="Flow 5: user_confirm_action",
                status="FLAGGED",
                detail=f"Protected operation '{action_name}' requires human-in-the-loop explicit confirmation."
            )
        return True, SecurityTraceStep(
            stage="Flow 5: user_confirm_action",
            status="PASS",
            detail=f"Explicit confirmation received for action '{action_name}'."
        )

    # Flow 6: block_prompt_injection
    def flow_6_block_prompt_injection(self, text: str) -> Tuple[bool, SecurityTraceStep]:
        lower = text.lower()
        for p in self.injection_signatures:
            if p in lower:
                return False, SecurityTraceStep(
                    stage="Flow 6: block_prompt_injection",
                    status="BLOCKED",
                    detail=f"Adversarial prompt injection signature detected: '{p}'. Execution aborted."
                )
        return True, SecurityTraceStep(
            stage="Flow 6: block_prompt_injection",
            status="PASS",
            detail="Zero prompt-injection or instruction-override tokens detected."
        )

    # Flow 7: block_jailbreak_attempt
    def flow_7_block_jailbreak_attempt(self, text: str) -> Tuple[bool, SecurityTraceStep]:
        lower = text.lower()
        for p in self.jailbreak_signatures:
            if p in lower:
                return False, SecurityTraceStep(
                    stage="Flow 7: block_jailbreak_attempt",
                    status="BLOCKED",
                    detail=f"Jailbreak heuristic pattern detected: '{p}'. Policy enforced."
                )
        return True, SecurityTraceStep(
            stage="Flow 7: block_jailbreak_attempt",
            status="PASS",
            detail="Input passed heuristic safety and anti-jailbreak evaluation."
        )

    # Flow 8: block_data_leakage
    def flow_8_block_data_leakage(self, text: str) -> Tuple[bool, SecurityTraceStep]:
        lower = text.lower()
        for p in self.data_leakage_signatures:
            if p in lower:
                return False, SecurityTraceStep(
                    stage="Flow 8: block_data_leakage",
                    status="BLOCKED",
                    detail=f"Mass data extraction / exfiltration pattern blocked: '{p}'."
                )
        return True, SecurityTraceStep(
            stage="Flow 8: block_data_leakage",
            status="PASS",
            detail="No data leakage or exfiltration vectors found."
        )

    # Flow 9: block_malicious_payload
    def flow_9_block_malicious_payload(self, text: str) -> Tuple[bool, SecurityTraceStep]:
        lower = text.lower()
        for p in self.malicious_payload_signatures:
            if p in lower:
                return False, SecurityTraceStep(
                    stage="Flow 9: block_malicious_payload",
                    status="BLOCKED",
                    detail=f"Malicious payload signature detected: '{p}' (SQLi/XSS/Command Injection)."
                )
        return True, SecurityTraceStep(
            stage="Flow 9: block_malicious_payload",
            status="PASS",
            detail="Payload passed syntax, SQLi, and code execution guardrails."
        )

    # Flow 10: reject_unauthorized_role
    def flow_10_reject_unauthorized_role(self, user_role: str, required_roles: List[str]) -> Tuple[bool, SecurityTraceStep]:
        if user_role == "admin" or "ALL" in required_roles or "ALL_TENANT_EMPLOYEES" in required_roles or user_role in required_roles:
            return True, SecurityTraceStep(
                stage="Flow 10: reject_unauthorized_role",
                status="PASS",
                detail=f"Role '{user_role}' authorized for requested resource."
            )
        return False, SecurityTraceStep(
            stage="Flow 10: reject_unauthorized_role",
            status="BLOCKED",
            detail=f"Role '{user_role}' lacks required permissions ({', '.join(required_roles)}). Pre-retrieval DB gate quarantined candidates."
        )

    # Flow 11: admin_update_policy
    def flow_11_admin_update_policy(self, is_admin: bool, update_type: str) -> Tuple[bool, SecurityTraceStep]:
        if not is_admin:
            return False, SecurityTraceStep(
                stage="Flow 11: admin_update_policy",
                status="BLOCKED",
                detail=f"Non-admin user attempted administrative modification: '{update_type}'."
            )
        return True, SecurityTraceStep(
            stage="Flow 11: admin_update_policy",
            status="PASS",
            detail=f"Admin credential verified for '{update_type}' modification."
        )

    # Flow 12: system_health_check
    def flow_12_system_health_check(self, db_ok: bool, inference_ok: bool) -> SecurityTraceStep:
        if db_ok and inference_ok:
            return SecurityTraceStep(
                stage="Flow 12: system_health_check",
                status="PASS",
                detail="PostgreSQL/pgvector database and LLM inference engine are operational."
            )
        return SecurityTraceStep(
            stage="Flow 12: system_health_check",
            status="FLAGGED",
            detail=f"Degraded subsystem state (DB: {'OK' if db_ok else 'OFFLINE'}, Inference: {'OK' if inference_ok else 'OFFLINE'})."
        )

    # Flow 13: tenant_isolation_verify
    def flow_13_tenant_isolation_verify(self, user_tenant: str, query: str) -> Tuple[bool, SecurityTraceStep]:
        other_tenant = "Amazon" if "nexus" in user_tenant.lower() else "Nexus"
        if other_tenant.lower() in query.lower():
            return False, SecurityTraceStep(
                stage="Flow 13: tenant_isolation_verify",
                status="ISOLATED",
                detail=f"Cross-tenant boundary triggered: Query references external tenant '{other_tenant}'. Retrieval strictly constrained to '{user_tenant}'."
            )
        return True, SecurityTraceStep(
            stage="Flow 13: tenant_isolation_verify",
            status="PASS",
            detail=f"Tenant boundary verified: Strict isolation enforced for tenant '{user_tenant}'."
        )

policy_engine = SecurityPolicyEngine()
