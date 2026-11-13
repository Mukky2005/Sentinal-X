import React, { useState, useEffect } from 'react';
import { 
  Building2, User, Mail, Phone, Cpu, Database, Shield, CheckCircle2, 
  Send, Sparkles, Server, HardDrive, Lock, FileCheck 
} from 'lucide-react';
import { submitServiceRequest, fetchInfrastructure } from '../api';
import SentinelLogo from '../components/SentinelLogo';

export default function RequestServicePage({ setActiveTab }) {
  const [formData, setFormData] = useState({
    company_name: '',
    contact_name: '',
    contact_email: '',
    contact_phone: '',
    target_users_count: '100-500',
    deployment_type: 'DEDICATED_POSTGRES',
    billing_discussion: 'CUSTOM_ENTERPRISE',
    selected_models: ['llama3.2', 'nomic-embed-text'],
    selected_database: 'PostgreSQL + pgvector',
    requirements_note: ''
  });

  const [infraSpecs, setInfraSpecs] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submissionResult, setSubmissionResult] = useState(null);

  useEffect(() => {
    fetchInfrastructure().then(setInfraSpecs).catch(console.error);
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!formData.company_name || !formData.contact_name || !formData.contact_email) {
      alert('Please complete the required company and contact fields.');
      return;
    }

    setIsSubmitting(true);
    try {
      const res = await submitServiceRequest(formData);
      setSubmissionResult(res);
    } catch (err) {
      alert('Failed to submit service request: ' + err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="bg-black text-white font-sans selection:bg-white selection:text-black py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="border-b border-white/15 pb-10">
        <div className="flex items-center gap-2 font-mono text-xs text-neutral-400 uppercase tracking-widest mb-2">
          <Server size={14} className="text-white" /> Enterprise Architecture Onboarding
        </div>
        <h1 className="text-3xl sm:text-5xl font-bold uppercase tracking-tight text-white max-w-4xl">
          Request a Service / Deploy Sentinel-X
        </h1>
        <p className="mt-3 text-sm text-neutral-300 font-sans max-w-2xl leading-relaxed">
          Request a dedicated, tenant-isolated knowledge platform for your enterprise. Configure on-premise local Ollama inference, private PostgreSQL with pgvector, and custom role-based retrieval policies.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 mt-12 items-start">
        {/* Left: Infrastructure & Local Model Specifications */}
        <div className="lg:col-span-5 space-y-6">
          {/* Models Showcase Card */}
          <div className="boxy-card border-white/20 p-6">
            <div className="flex items-center justify-between pb-3 border-b border-white/10">
              <div className="flex items-center gap-2 font-mono text-xs uppercase font-bold text-white">
                <Cpu size={14} /> Available Local Inference Models
              </div>
              <span className="font-mono text-[10px] bg-white text-black font-bold px-2 py-0.5 uppercase">
                OLLAMA HOSTED
              </span>
            </div>
            <p className="mt-3 text-xs text-neutral-400 font-sans leading-relaxed">
              Sentinel-X runs completely self-contained. The local Ollama instance on your host environment provisions the following foundational engines:
            </p>

            <div className="mt-4 space-y-3 font-mono text-xs">
              {/* Llama 3.2 */}
              <div className="p-3 bg-neutral-900/60 border border-white/10">
                <div className="flex items-center justify-between font-bold text-white mb-1">
                  <span className="flex items-center gap-1.5">
                    <span className="w-2 h-2 bg-emerald-400"></span>
                    llama3.2:latest
                  </span>
                  <span className="text-neutral-400 text-[10px]">2.0 GB &middot; LLM</span>
                </div>
                <p className="font-sans text-[11px] text-neutral-300">
                  Primary local chat and synthesis model. Produces strictly grounded answers using pre-retrieval authorized context only.
                </p>
              </div>

              {/* nomic-embed-text */}
              <div className="p-3 bg-neutral-900/60 border border-white/10">
                <div className="flex items-center justify-between font-bold text-white mb-1">
                  <span className="flex items-center gap-1.5">
                    <span className="w-2 h-2 bg-emerald-400"></span>
                    nomic-embed-text:latest
                  </span>
                  <span className="text-neutral-400 text-[10px]">274 MB &middot; Embeddings</span>
                </div>
                <p className="font-sans text-[11px] text-neutral-300">
                  Dense passage retriever generating 768-dimensional numerical vectors for document chunks and user queries.
                </p>
              </div>

              {/* gemma4:12b */}
              <div className="p-3 bg-neutral-900/60 border border-white/10">
                <div className="flex items-center justify-between font-bold text-white mb-1">
                  <span className="flex items-center gap-1.5">
                    <span className="w-2 h-2 bg-emerald-400"></span>
                    gemma4:12b
                  </span>
                  <span className="text-neutral-400 text-[10px]">7.7 GB &middot; Advanced Reasoning</span>
                </div>
                <p className="font-sans text-[11px] text-neutral-300">
                  High-parameter reasoning engine for complex cross-policy cross-referencing and executive summarization.
                </p>
              </div>
            </div>
          </div>

          {/* Database & Isolation Card */}
          <div className="boxy-card border-white/20 p-6">
            <div className="flex items-center gap-2 pb-3 border-b border-white/10 font-mono text-xs uppercase font-bold text-white">
              <Database size={14} /> Vector Storage Engine
            </div>
            <div className="mt-4 space-y-3 font-mono text-xs">
              <div className="flex items-start gap-3">
                <HardDrive size={16} className="text-white shrink-0 mt-0.5" />
                <div>
                  <strong className="text-white block">PostgreSQL with pgvector</strong>
                  <span className="font-sans text-xs text-neutral-400">
                    Industrial relational persistence with cosine distance (<code className="text-neutral-200">&lt;=&gt;</code>) vector indexing and schema-level isolation.
                  </span>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Shield size={16} className="text-white shrink-0 mt-0.5" />
                <div>
                  <strong className="text-white block">Pre-Retrieval DB Gate</strong>
                  <span className="font-sans text-xs text-neutral-400">
                    Row-Level Security enforces tenant and role predicates before similarity rankings are computed.
                  </span>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Lock size={16} className="text-white shrink-0 mt-0.5" />
                <div>
                  <strong className="text-white block">Zero Cloud Data Exfiltration</strong>
                  <span className="font-sans text-xs text-neutral-400">
                    All document vectors, chat logs, and inference remain 100% inside your private enterprise perimeter.
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Onboarding Request Form */}
        <div className="lg:col-span-7">
          {submissionResult ? (
            <div className="boxy-card border-white/40 p-8 space-y-6">
              <div className="w-12 h-12 bg-white text-black flex items-center justify-center font-mono font-bold text-xl">
                ✓
              </div>
              <div>
                <span className="font-mono text-xs uppercase text-emerald-400 tracking-wider">
                  Request Confirmed & Queued
                </span>
                <h3 className="text-2xl font-bold uppercase tracking-tight text-white mt-1">
                  Deployment Ticket: {submissionResult.request_details?.id}
                </h3>
                <p className="mt-3 text-sm text-neutral-300 font-sans leading-relaxed">
                  {submissionResult.message}
                </p>
              </div>

              <div className="bg-neutral-900 p-4 border border-white/10 font-mono text-xs space-y-2">
                <div>Company: <strong className="text-white">{formData.company_name}</strong></div>
                <div>Contact: <strong className="text-white">{formData.contact_name} ({formData.contact_email})</strong></div>
                <div>Deployment Option: <strong className="text-white">{formData.deployment_type}</strong></div>
                <div>Billing Preference: <strong className="text-white">{formData.billing_discussion}</strong></div>
                <div>Vector Engine: <strong className="text-white">{formData.selected_database}</strong></div>
              </div>

              <button
                onClick={() => {
                  setSubmissionResult(null);
                  setFormData({
                    company_name: '',
                    contact_name: '',
                    contact_email: '',
                    contact_phone: '',
                    target_users_count: '100-500',
                    deployment_type: 'DEDICATED_POSTGRES',
                    billing_discussion: 'CUSTOM_ENTERPRISE',
                    selected_models: ['llama3.2', 'nomic-embed-text'],
                    selected_database: 'PostgreSQL + pgvector',
                    requirements_note: ''
                  });
                }}
                className="boxy-btn py-2.5 px-6 text-xs"
              >
                Submit Another Request
              </button>
            </div>
          ) : (
            <div className="boxy-card border-white/20 p-8">
              <div className="flex items-center gap-2 pb-4 border-b border-white/10 font-mono text-xs uppercase font-bold text-white">
                <FileCheck size={16} /> Enterprise Deployment Questionnaire
              </div>

              <form onSubmit={handleSubmit} className="mt-6 space-y-6">
                {/* Company Name & Scale */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block font-mono text-[11px] uppercase text-neutral-400 mb-1">
                      Company Name *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.company_name}
                      onChange={e => setFormData({ ...formData, company_name: e.target.value })}
                      placeholder="e.g. Apex Global Systems"
                      className="boxy-input text-xs"
                    />
                  </div>

                  <div>
                    <label className="block font-mono text-[11px] uppercase text-neutral-400 mb-1">
                      Target User Count
                    </label>
                    <select
                      value={formData.target_users_count}
                      onChange={e => setFormData({ ...formData, target_users_count: e.target.value })}
                      className="boxy-input text-xs"
                    >
                      <option value="10-100">10 – 100 Employees</option>
                      <option value="100-500">100 – 500 Employees</option>
                      <option value="500-2000">500 – 2,000 Employees</option>
                      <option value="2000+">2,000+ Enterprise Scale</option>
                    </select>
                  </div>
                </div>

                {/* Contact Person Details */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div>
                    <label className="block font-mono text-[11px] uppercase text-neutral-400 mb-1">
                      Contact Person *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.contact_name}
                      onChange={e => setFormData({ ...formData, contact_name: e.target.value })}
                      placeholder="e.g. Rachel Croft"
                      className="boxy-input text-xs"
                    />
                  </div>

                  <div>
                    <label className="block font-mono text-[11px] uppercase text-neutral-400 mb-1">
                      Work Email *
                    </label>
                    <input
                      type="email"
                      required
                      value={formData.contact_email}
                      onChange={e => setFormData({ ...formData, contact_email: e.target.value })}
                      placeholder="rachel@apex.internal"
                      className="boxy-input text-xs"
                    />
                  </div>

                  <div>
                    <label className="block font-mono text-[11px] uppercase text-neutral-400 mb-1">
                      Phone Number
                    </label>
                    <input
                      type="tel"
                      value={formData.contact_phone}
                      onChange={e => setFormData({ ...formData, contact_phone: e.target.value })}
                      placeholder="+1 (555) 019-2834"
                      className="boxy-input text-xs"
                    />
                  </div>
                </div>

                {/* Deployment Architecture */}
                <div>
                  <label className="block font-mono text-[11px] uppercase text-neutral-400 mb-2">
                    Deployment Isolation Topology
                  </label>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    {[
                      { id: 'DEDICATED_POSTGRES', label: 'Dedicated PostgreSQL', desc: 'Isolated database container per tenant with pgvector' },
                      { id: 'AIR_GAPPED_ONPREM', label: 'Air-Gapped On-Premise', desc: '100% self-hosted with local Ollama GPU server' },
                      { id: 'HYBRID_CLOUD', label: 'Governed Hybrid', desc: 'Central control plane with localized data sovereignty' }
                    ].map(opt => (
                      <div
                        key={opt.id}
                        onClick={() => setFormData({ ...formData, deployment_type: opt.id })}
                        className={`p-3 border cursor-pointer rounded-none transition-colors ${
                          formData.deployment_type === opt.id
                            ? 'bg-neutral-900 border-white text-white'
                            : 'border-white/10 text-neutral-400 hover:border-white/30'
                        }`}
                      >
                        <strong className="block font-mono text-xs uppercase mb-1">{opt.label}</strong>
                        <span className="font-sans text-[11px] text-neutral-400">{opt.desc}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Billing Discussion Scope */}
                <div>
                  <label className="block font-mono text-[11px] uppercase text-neutral-400 mb-2">
                    Billing & SLA Discussion Scope
                  </label>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    {[
                      { id: 'CUSTOM_ENTERPRISE', label: 'Custom Enterprise', desc: 'Tiered pricing based on active roles and indexed vectors' },
                      { id: 'DEDICATED_GPU', label: 'Dedicated Hardware Pod', desc: 'Fixed monthly hardware lease for dedicated GPU inference' },
                      { id: 'ANNUAL_SUBSCRIPTION', label: 'Annual Licensing', desc: 'Unlimited tenant workspaces and role-based access tokens' }
                    ].map(opt => (
                      <div
                        key={opt.id}
                        onClick={() => setFormData({ ...formData, billing_discussion: opt.id })}
                        className={`p-3 border cursor-pointer rounded-none transition-colors ${
                          formData.billing_discussion === opt.id
                            ? 'bg-neutral-900 border-white text-white'
                            : 'border-white/10 text-neutral-400 hover:border-white/30'
                        }`}
                      >
                        <strong className="block font-mono text-xs uppercase mb-1">{opt.label}</strong>
                        <span className="font-sans text-[11px] text-neutral-400">{opt.desc}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Special Requirements Note */}
                <div>
                  <label className="block font-mono text-[11px] uppercase text-neutral-400 mb-1">
                    Special Compliance or Security Requirements
                  </label>
                  <textarea
                    rows={3}
                    value={formData.requirements_note}
                    onChange={e => setFormData({ ...formData, requirements_note: e.target.value })}
                    placeholder="e.g. Integration with corporate Okta SAML IdP, custom Colang guardrails, or specific data retention limits..."
                    className="boxy-input text-xs font-mono"
                  />
                </div>

                {/* Submit Boxy Button */}
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="boxy-btn-primary w-full py-3.5 text-xs flex items-center justify-center gap-2"
                >
                  <Send size={14} />
                  <span>
                    {isSubmitting ? 'Transmitting Enterprise Request...' : 'Submit Request & Schedule Architecture Review'}
                  </span>
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
