import React, { useState } from 'react';
import { 
  Shield, Lock, Database, Cpu, Terminal, ArrowRight, CheckCircle2, 
  AlertTriangle, FileText, Layers, Network, Eye, ChevronRight, BookOpen, Key
} from 'lucide-react';
import SentinelLogo from '../components/SentinelLogo';

export default function LandingPage({ setActiveTab }) {
  const [selectedRoadmapTab, setSelectedRoadmapTab] = useState('multi-engine');

  const roadmapItems = [
    {
      id: 'multi-engine',
      title: 'Multi-Engine Inference & Disaggregated GPU Serving',
      section: 'Section VI.A',
      summary: 'Dynamic routing across vLLM, NVIDIA TensorRT-LLM, and NVIDIA Dynamo with disaggregated prefill and decode stages.',
      details: [
        'Decoupled prefill and decode worker pools for maximized GPU cluster efficiency.',
        'Tenant-scoped inference cache boundaries mitigating multi-tenant KV-cache prefix contamination.',
        'Workload-aware routing between shared vLLM clusters and dedicated TensorRT-LLM secure accelerators.'
      ]
    },
    {
      id: 'nemo-rails',
      title: 'Domain-Specific Canonical Intents & NeMo Guardrails',
      section: 'Section VI.B',
      summary: 'Integration with NVIDIA NeMo Guardrails powered by Colang for deep multi-stage conversation policy execution.',
      details: [
        'Normalization of natural-language requests into canonical intent labels (e.g. computeLegalClause vs requestFinancialApproval).',
        'Five-stage rail coverage: input rails, retrieval rails, dialog rails, execution rails, and output verification.',
        'Tenant-specific versioned guardrails configurations with full administrative audit logging.'
      ]
    },
    {
      id: 'persona',
      title: 'Persona-Aware & Role-Adaptive AI Interaction',
      section: 'Section VI.C',
      summary: 'Tailored AI conversational personas designed for distinct enterprise functions without compromising RBAC security.',
      details: [
        'Modular personas: Managerial (concise executive metrics), Engineering (rigorous technical documentation), Legal, Compliance.',
        'Strict separation between persona presentation and underlying authorization boundary.',
        'Audit-tracked profile adjustments ensuring role-based data filtering remains immutable.'
      ]
    },
    {
      id: 'agentic',
      title: 'Agentic Workflows with Human-in-the-Loop Verification',
      section: 'Section VI.D',
      summary: 'Autonomous AI enterprise action execution governed by strict tool authorization policies and mandatory human sign-off.',
      details: [
        'Role-scoped tool invocation logging (e.g., ticket generation, operational summaries, administrative requests).',
        'Mandatory dual-key human review and approval gates for capital disbursements or user permission changes.',
        'NeMo execution rails intercepting model tool calls to prevent unintended infrastructure modifications.'
      ]
    },
    {
      id: 'knowledge-graph',
      title: 'Hybrid Vector + Enterprise Knowledge Graph (Neo4j)',
      section: 'Section VI.E',
      summary: 'Unification of pgvector dense semantic embeddings with relational graph traversals for complex enterprise reasoning.',
      details: [
        'Multi-hop path exploration linking policies, approving authorities, departments, and infrastructure assets.',
        'Graph path blocking preventing implicit alternative access routes to restricted documents.',
        'Combined keyword, dense vector, and graph structure ranking for highly precise technical queries.'
      ]
    },
    {
      id: 'multimodal',
      title: 'Multimodal Ingestion & Cryptographic Media Provenance',
      section: 'Section VI.F',
      summary: 'Extension to engineering blueprints, inspection images, scanned corporate ledgers, and audio records.',
      details: [
        'Apache Tika, OCR engines, and layout analysis parsing complex enterprise document formats.',
        'Inheritance of tenant_id and role metadata across extracted images, audio transcripts, and tabular chunks.',
        'Quarantined ingestion cache preventing untrusted binary exploits from reaching production storage.'
      ]
    },
    {
      id: 'confidential',
      title: 'Confidential Computing & Hardware Enclave (TEE) Isolation',
      section: 'Section VI.H',
      summary: 'Hardware-enforced execution isolation for highly regulated defense and financial environments.',
      details: [
        'Deployment in Confidential Virtual Machines (AMD SEV-SNP / Intel TDX) with encrypted host memory.',
        'Tenant-owned encryption key possession with automated secret and token rotation.',
        'Zero-trust telemetry ensuring operational logs remain scrubbed of sensitive enterprise context.'
      ]
    }
  ];

  return (
    <div className="bg-black text-white selection:bg-white selection:text-black">
      {/* ---------------------------------------------------- */}
      {/* 1. HERO SECTION */}
      {/* ---------------------------------------------------- */}
      <section className="relative border-b border-white/15 pt-16 pb-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        {/* Background Grid Pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#111_1px,transparent_1px),linear-gradient(to_bottom,#111_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-30"></div>

        <div className="relative max-w-7xl mx-auto">
          {/* Header Badges */}
          <div className="flex flex-wrap items-center gap-3 mb-6 font-mono text-xs">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-white text-black font-semibold uppercase tracking-wider rounded-none">
              <Shield size={12} /> Sentinel-X Vision
            </span>
          </div>

          {/* Main Title */}
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-sans font-bold tracking-tight text-white uppercase max-w-5xl leading-tight">
            Tenant-Isolated <br />
            <span className="font-mono text-neutral-400">Knowledge Retrieval</span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-neutral-300 max-w-3xl leading-relaxed font-sans">
            A layered security framework for multi-tenant enterprise RAG. Traditional AI assistants rely on model prompt instructions to hide sensitive documents. <strong className="text-white">Sentinel-X enforces cryptographic and database-level pre-retrieval boundaries</strong> so unauthorized data is never retrieved or passed into the language model.
          </p>

          {/* Action Callouts */}
          <div className="mt-10 flex flex-wrap items-center gap-4">
            <button
              onClick={() => setActiveTab('demo')}
              className="boxy-btn-primary py-3.5 px-7 text-xs flex items-center gap-2"
            >
              <Terminal size={14} />
              <span>Launch Live Multi-Tenant Demo</span>
              <ArrowRight size={14} />
            </button>
            <button
              onClick={() => setActiveTab('request')}
              className="boxy-btn py-3.5 px-7 text-xs flex items-center gap-2"
            >
              <Cpu size={14} />
              <span>Request Enterprise Onboarding</span>
            </button>
          </div>
        </div>
      </section>

      {/* ---------------------------------------------------- */}
      {/* 2. THE FUNDAMENTAL FLAW IN INDUSTRY RAG */}
      {/* ---------------------------------------------------- */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto border-b border-white/15">
        <div className="mb-12">
          <span className="font-mono text-xs text-neutral-400 uppercase tracking-widest block mb-2">
            Section I & III Analysis
          </span>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight uppercase">
            Why Industry RAG Architectures Suffer Critical Data Leakage
          </h2>
          <p className="mt-3 text-neutral-400 max-w-3xl text-sm font-sans leading-relaxed">
            In standard enterprise RAG, documents from different tenants and departments are pooled into a shared vector store. Retrieval is determined solely by cosine vector proximity. This creates severe, unmitigated attack vectors:
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Flawed Industry RAG */}
          <div className="boxy-card border-red-500/30 bg-neutral-950 p-6">
            <div className="flex items-center justify-between pb-4 border-b border-neutral-800">
              <div className="flex items-center gap-2 text-red-400 font-mono text-xs uppercase tracking-wider font-bold">
                <AlertTriangle size={16} />
                <span>Standard Industry RAG (Flawed Baseline)</span>
              </div>
              <span className="font-mono text-[10px] text-red-400/80 uppercase px-2 py-0.5 bg-red-950/40 border border-red-900/50">
                HIGH PRIVACY RISK
              </span>
            </div>

            <ul className="mt-6 space-y-4 font-mono text-xs text-neutral-300">
              <li className="flex items-start gap-2.5">
                <span className="text-red-400 font-bold shrink-0">✕</span>
                <span>
                  <strong className="text-white">Semantic Similarity ≠ Authorization:</strong> If an employee asks for confidential CFO bonuses, vector similarity retrieves the bonus chunk because it is semantically relevant.
                </span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="text-red-400 font-bold shrink-0">✕</span>
                <span>
                  <strong className="text-white">System Prompt is NOT a Security Boundary:</strong> Asking the LLM ("Please do not reveal finance documents to tech users") fails against indirect prompt injections and jailbreak tokens.
                </span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="text-red-400 font-bold shrink-0">✕</span>
                <span>
                  <strong className="text-white">Multi-Tenant KV-Cache Contamination:</strong> Shared inference processes reuse attention key-value caches across concurrent sessions, risking token bleeding between customer tenants.
                </span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="text-red-400 font-bold shrink-0">✕</span>
                <span>
                  <strong className="text-white">Untrusted Client-Supplied Tenant IDs:</strong> Applications accepting tenant headers without server-side validation are vulnerable to tenant impersonation attacks.
                </span>
              </li>
            </ul>
          </div>

          {/* Sentinel-X Solution */}
          <div className="boxy-card border-white/40 bg-neutral-950 p-6">
            <div className="flex items-center justify-between pb-4 border-b border-neutral-800">
              <div className="flex items-center gap-2 text-white font-mono text-xs uppercase tracking-wider font-bold">
                <Shield size={16} />
                <span>Sentinel-X Layered Security Framework</span>
              </div>
              <span className="font-mono text-[10px] text-white uppercase px-2 py-0.5 bg-neutral-800 border border-neutral-600">
                ZERO-TRUST BOUNDARY
              </span>
            </div>

            <ul className="mt-6 space-y-4 font-mono text-xs text-neutral-300">
              <li className="flex items-start gap-2.5">
                <span className="text-white font-bold shrink-0">✓</span>
                <span>
                  <strong className="text-white">Pre-Retrieval DB Gate:</strong> Vector similarity is strictly executed within a pre-filtered candidate set: <code className="text-neutral-300 bg-neutral-900 px-1">WHERE tenant_id = ? AND (role = ? OR scope = 'ALL')</code>.
                </span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="text-white font-bold shrink-0">✓</span>
                <span>
                  <strong className="text-white">Fail-Closed Guarantee:</strong> If 0 authorized chunks match the query, the retrieval terminates immediately. Exactly <strong>0 unauthorized chunks</strong> ever reach the LLM context.
                </span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="text-white font-bold shrink-0">✓</span>
                <span>
                  <strong className="text-white">Untrusted Document Quarantine:</strong> Ingested content is treated as untrusted data, preventing indirect prompt injections from executing system-level instructions.
                </span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="text-white font-bold shrink-0">✓</span>
                <span>
                  <strong className="text-white">Isolated Request-State Inference:</strong> Controlled inference gateway routes requests with dedicated execution contexts and tenant-scoped cache labels.
                </span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* ---------------------------------------------------- */}
      {/* 3. FOUR ARCHITECTURAL LAYERS */}
      {/* ---------------------------------------------------- */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto border-b border-white/15">
        <div className="mb-12">
          <span className="font-mono text-xs text-neutral-400 uppercase tracking-widest block mb-2">
            Section IV System Architecture
          </span>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight uppercase">
            Four Core Architectural Isolation Layers
          </h2>
          <p className="mt-3 text-neutral-400 max-w-3xl text-sm font-sans leading-relaxed">
            Sentinel-X replaces monolithic RAG with an orchestrated defense-in-depth pipeline across client identity, control plane, data storage, and model inference:
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Layer 1 */}
          <div className="boxy-card border-white/15 p-5 flex flex-col justify-between">
            <div>
              <div className="font-mono text-[11px] text-neutral-500 uppercase tracking-wider mb-2">
                Layer 01
              </div>
              <h3 className="font-mono font-bold text-sm uppercase text-white mb-3">
                Client & Trusted Identity Layer
              </h3>
              <p className="text-xs text-neutral-400 font-sans leading-relaxed">
                Server-side identity resolution verifies tenant membership using cryptographic claims (NIST SP 800-207 Zero-Trust). Client headers and natural language prompts are completely untrusted.
              </p>
            </div>
            <div className="mt-6 pt-3 border-t border-white/10 font-mono text-[10px] text-neutral-400">
              OAuth 2.0 RFC 9700 &middot; JWT Server Resolution
            </div>
          </div>

          {/* Layer 2 */}
          <div className="boxy-card border-white/15 p-5 flex flex-col justify-between">
            <div>
              <div className="font-mono text-[11px] text-neutral-500 uppercase tracking-wider mb-2">
                Layer 02
              </div>
              <h3 className="font-mono font-bold text-sm uppercase text-white mb-3">
                Programmable Policy & Control Plane
              </h3>
              <p className="text-xs text-neutral-400 font-sans leading-relaxed">
                Orchestrates 13 reusable security flows including <code className="text-neutral-300">block_prompt_injection</code>, <code className="text-neutral-300">reject_unauthorized_role</code>, and <code className="text-neutral-300">tenant_isolation_verify</code> before any DB lookup occurs.
              </p>
            </div>
            <div className="mt-6 pt-3 border-t border-white/10 font-mono text-[10px] text-neutral-400">
              13 Flow Engine &middot; Real-Time Audit Telemetry
            </div>
          </div>

          {/* Layer 3 */}
          <div className="boxy-card border-white/15 p-5 flex flex-col justify-between">
            <div>
              <div className="font-mono text-[11px] text-neutral-500 uppercase tracking-wider mb-2">
                Layer 03
              </div>
              <h3 className="font-mono font-bold text-sm uppercase text-white mb-3">
                PostgreSQL + pgvector Knowledge Store
              </h3>
              <p className="text-xs text-neutral-400 font-sans leading-relaxed">
                Dedicated database schemas and Row-Level Security (RLS). Chunks inherit immutable tenant and role mappings at ingestion. Cosine similarity executes strictly after role authorization.
              </p>
            </div>
            <div className="mt-6 pt-3 border-t border-white/10 font-mono text-[10px] text-neutral-400">
              pgvector 16 &middot; RBAC / ABAC Predicates
            </div>
          </div>

          {/* Layer 4 */}
          <div className="boxy-card border-white/15 p-5 flex flex-col justify-between">
            <div>
              <div className="font-mono text-[11px] text-neutral-500 uppercase tracking-wider mb-2">
                Layer 04
              </div>
              <h3 className="font-mono font-bold text-sm uppercase text-white mb-3">
                Controlled Inference & Request Isolation
              </h3>
              <p className="text-xs text-neutral-400 font-sans leading-relaxed">
                Model serving gateway (Ollama / vLLM) isolates prompt state, conversation history, and key-value cache memory per tenant request, preventing cross-tenant GPU state leaks.
              </p>
            </div>
            <div className="mt-6 pt-3 border-t border-white/10 font-mono text-[10px] text-neutral-400">
              Request-State Isolation &middot; Fail-Closed Output Gate
            </div>
          </div>
        </div>
      </section>

      {/* ---------------------------------------------------- */}
      {/* 4. FINISHED PRODUCT FUTURE SCOPE & ROADMAP */}
      {/* ---------------------------------------------------- */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto border-b border-white/15">
        <div className="mb-12">
          <span className="font-mono text-xs text-neutral-400 uppercase tracking-widest block mb-2">
            Section VI Research Roadmap
          </span>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight uppercase">
            Finished Product Evolution & Advanced Capabilities
          </h2>
          <p className="mt-3 text-neutral-400 max-w-3xl text-sm font-sans leading-relaxed">
            Based directly on Section VI of the research paper, the finished commercial evolution of Sentinel-X expands into multi-engine disaggregated inference, NVIDIA NeMo Colang Guardrails, autonomous agentic workflows, and Confidential Computing:
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Roadmap Navigation Selector */}
          <div className="lg:col-span-5 space-y-2">
            {roadmapItems.map((item) => {
              const isSelected = selectedRoadmapTab === item.id;
              return (
                <div
                  key={item.id}
                  onClick={() => setSelectedRoadmapTab(item.id)}
                  className={`p-4 border transition-all cursor-pointer rounded-none ${
                    isSelected
                      ? 'bg-white text-black border-white'
                      : 'bg-neutral-950 text-neutral-300 border-white/10 hover:border-white/30 hover:bg-neutral-900'
                  }`}
                >
                  <div className="flex items-center justify-between text-[11px] font-mono uppercase mb-1">
                    <span className={isSelected ? 'text-neutral-800' : 'text-neutral-500'}>
                      {item.section}
                    </span>
                    {isSelected && <span className="font-bold">ACTIVE VIEW</span>}
                  </div>
                  <h4 className="font-mono font-bold text-xs uppercase leading-snug">
                    {item.title}
                  </h4>
                  <p className={`mt-1.5 text-xs font-sans line-clamp-2 ${isSelected ? 'text-neutral-700' : 'text-neutral-400'}`}>
                    {item.summary}
                  </p>
                </div>
              );
            })}
          </div>

          {/* Deep Detail Panel */}
          <div className="lg:col-span-7 boxy-card border-white/20 p-8 min-h-[440px] flex flex-col justify-between">
            {(() => {
              const current = roadmapItems.find((r) => r.id === selectedRoadmapTab);
              return (
                <div>
                  <div className="flex items-center justify-between pb-4 border-b border-white/15">
                    <span className="font-mono text-xs text-neutral-400 uppercase tracking-widest">
                      Architectural Specification &middot; {current.section}
                    </span>
                    <span className="font-mono text-[10px] bg-white text-black px-2 py-0.5 font-bold uppercase">
                      Enterprise Roadmap
                    </span>
                  </div>

                  <h3 className="text-xl font-mono font-bold uppercase text-white mt-6 mb-3">
                    {current.title}
                  </h3>

                  <p className="text-sm text-neutral-300 font-sans leading-relaxed mb-6">
                    {current.summary}
                  </p>

                  <div className="space-y-4">
                    <h5 className="font-mono text-xs uppercase text-neutral-400 tracking-wider">
                      Engineering Implementation Pillars:
                    </h5>
                    <ul className="space-y-3 font-mono text-xs text-neutral-200">
                      {current.details.map((detail, idx) => (
                        <li key={idx} className="flex items-start gap-3 bg-neutral-900/60 border border-white/10 p-3.5 rounded-none">
                          <CheckCircle2 size={16} className="text-white shrink-0 mt-0.5" />
                          <span className="font-sans text-xs leading-relaxed text-neutral-300">
                            {detail}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              );
            })()}

            <div className="mt-8 pt-6 border-t border-white/15 flex items-center justify-between font-mono text-xs">
              <span className="text-neutral-400">Status: In Engineering Development</span>
              <button
                onClick={() => setActiveTab('request')}
                className="boxy-btn text-xs py-2 px-4 flex items-center gap-1.5"
              >
                <span>Request Custom Pipeline</span>
                <ChevronRight size={14} />
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* ---------------------------------------------------- */}
      {/* 5. CALL TO ACTION BAR */}
      {/* ---------------------------------------------------- */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto text-center">
        <div className="border border-white/20 bg-neutral-950 p-10 sm:p-14 rounded-none max-w-4xl mx-auto">
          <SentinelLogo size={44} showText={false} className="justify-center mb-6" />
          <h2 className="text-3xl font-bold uppercase tracking-tight text-white mb-4">
            Test the Multi-Tenant Architecture Live
          </h2>
          <p className="text-neutral-400 text-sm max-w-xl mx-auto font-sans leading-relaxed mb-8">
            Experience real-time role isolation across two pre-seeded corporate tenants (Nexus and Amazon), switch between distinct employee roles, and observe the live pre-retrieval security filter trace.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={() => setActiveTab('demo')}
              className="boxy-btn-primary py-3 px-8 text-xs flex items-center gap-2"
            >
              <Terminal size={14} />
              <span>Enter Interactive Demo</span>
            </button>
            <button
              onClick={() => setActiveTab('request')}
              className="boxy-btn py-3 px-8 text-xs flex items-center gap-2"
            >
              <Cpu size={14} />
              <span>Request Enterprise Onboarding</span>
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
