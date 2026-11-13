import React from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import DemoPage from './pages/DemoPage';
import RequestServicePage from './pages/RequestServicePage';

export default function App() {
  const navigate = useNavigate();

  // Backward compatible helper for child callbacks
  const handleTabChange = (tab) => {
    if (tab === 'demo') navigate('/demo');
    else if (tab === 'request') navigate('/request');
    else navigate('/');
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col font-sans selection:bg-white selection:text-black">
      <Navbar />
      
      <main className="flex-1">
        <Routes>
          {/* Landing / Architecture Vision Dashboard */}
          <Route path="/" element={<LandingPage setActiveTab={handleTabChange} />} />
          <Route path="/architecture" element={<LandingPage setActiveTab={handleTabChange} />} />

          {/* Multi-Tenant Demo & Company Dashboards */}
          <Route path="/demo" element={<DemoPage setActiveTab={handleTabChange} />} />
          <Route path="/demo/:tenantSlug" element={<DemoPage setActiveTab={handleTabChange} />} />
          <Route path="/demo/:tenantSlug/:roleSlug" element={<DemoPage setActiveTab={handleTabChange} />} />
          <Route path="/demo/:tenantSlug/:roleSlug/:tabSlug" element={<DemoPage setActiveTab={handleTabChange} />} />

          {/* Alias /dashboard paths */}
          <Route path="/dashboard" element={<Navigate to="/demo" replace />} />
          <Route path="/dashboard/:tenantSlug" element={<DemoPage setActiveTab={handleTabChange} />} />
          <Route path="/dashboard/:tenantSlug/:roleSlug" element={<DemoPage setActiveTab={handleTabChange} />} />
          <Route path="/dashboard/:tenantSlug/:roleSlug/:tabSlug" element={<DemoPage setActiveTab={handleTabChange} />} />

          {/* Direct Administrator Dashboards */}
          <Route path="/admin" element={<Navigate to="/demo/nexus/admin/documents" replace />} />
          <Route path="/admin/:tenantSlug" element={<DemoPage defaultRole="admin" setActiveTab={handleTabChange} />} />
          <Route path="/admin/:tenantSlug/:tabSlug" element={<DemoPage defaultRole="admin" setActiveTab={handleTabChange} />} />

          {/* Direct Security Audit Log Dashboards */}
          <Route path="/audit" element={<Navigate to="/demo/nexus/admin/audit" replace />} />
          <Route path="/audit/:tenantSlug" element={<DemoPage defaultRole="admin" defaultTab="audit" setActiveTab={handleTabChange} />} />

          {/* Request a Service / Onboarding Dashboards */}
          <Route path="/request" element={<RequestServicePage setActiveTab={handleTabChange} />} />
          <Route path="/request-service" element={<Navigate to="/request" replace />} />
          <Route path="/onboarding" element={<Navigate to="/request" replace />} />

          {/* Catch-all fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>

      {/* Boxy Minimalist Enterprise Footer */}
      <footer className="border-t border-white/15 bg-black py-8 px-4 sm:px-6 lg:px-8 mt-auto">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 font-mono text-xs text-neutral-500">
          <div className="flex items-center gap-3">
            <span className="text-white font-bold tracking-wider">SENTINEL-X</span>
            <span>&middot;</span>
            <span>ENTERPRISE PLATFORM</span>
            <span>&middot;</span>
            <span className="text-neutral-400">MVP 1.0 (2026)</span>
          </div>

          <div className="flex items-center gap-6">
            <button
              onClick={() => navigate('/')}
              className="hover:text-white transition-colors uppercase"
            >
              Sentinel-X Vision
            </button>
            <button
              onClick={() => navigate('/demo')}
              className="hover:text-white transition-colors uppercase"
            >
              Live Demo
            </button>
            <button
              onClick={() => navigate('/request')}
              className="hover:text-white transition-colors uppercase"
            >
              Request Service
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}
