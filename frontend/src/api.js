// SentinelX API Client
const API_BASE = '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function fetchInfrastructure() {
  const res = await fetch(`${API_BASE}/infrastructure`);
  return res.json();
}

export async function fetchTenants() {
  const res = await fetch(`${API_BASE}/tenants`);
  return res.json();
}

export async function fetchRoles(tenantId) {
  const url = tenantId ? `${API_BASE}/roles?tenant_id=${tenantId}` : `${API_BASE}/roles`;
  const res = await fetch(url);
  return res.json();
}

export async function createRole(tenantId, name, slug, description) {
  const res = await fetch(`${API_BASE}/roles?tenant_id=${tenantId}&name=${encodeURIComponent(name)}&slug=${encodeURIComponent(slug)}&description=${encodeURIComponent(description)}`, {
    method: 'POST'
  });
  return res.json();
}

export async function fetchEmployees(tenantId) {
  const url = tenantId ? `${API_BASE}/employees?tenant_id=${tenantId}` : `${API_BASE}/employees`;
  const res = await fetch(url);
  return res.json();
}

export async function updateEmployeeRole(userId, newRoleId) {
  const res = await fetch(`${API_BASE}/employees/${userId}/role?new_role_id=${newRoleId}`, {
    method: 'PUT'
  });
  return res.json();
}

export async function createEmployee(tenantId, name, email, roleId) {
  const res = await fetch(`${API_BASE}/employees?tenant_id=${tenantId}&name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&role_id=${roleId}`, {
    method: 'POST'
  });
  return res.json();
}

export async function fetchDocuments(tenantId) {
  const url = tenantId ? `${API_BASE}/documents?tenant_id=${tenantId}` : `${API_BASE}/documents`;
  const res = await fetch(url);
  return res.json();
}

export async function uploadDocument(formData) {
  const res = await fetch(`${API_BASE}/documents`, {
    method: 'POST',
    body: formData
  });
  return res.json();
}

export async function deleteDocument(docId) {
  const res = await fetch(`${API_BASE}/documents/${docId}`, {
    method: 'DELETE'
  });
  return res.json();
}

export async function queryChat(tenantId, userId, query) {
  const res = await fetch(`${API_BASE}/chat/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      tenant_id: tenantId,
      user_id: userId,
      query: query
    })
  });
  return res.json();
}

export async function fetchAuditLogs(tenantId) {
  const url = tenantId ? `${API_BASE}/audit/logs?tenant_id=${tenantId}` : `${API_BASE}/audit/logs`;
  const res = await fetch(url);
  return res.json();
}

export async function submitServiceRequest(payload) {
  const res = await fetch(`${API_BASE}/service/request`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return res.json();
}
