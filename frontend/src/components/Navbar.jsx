import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import SentinelLogo from './SentinelLogo';
import { Shield, Cpu, Terminal } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();

  const navItems = [
    { id: 'landing', path: '/', label: 'Sentinel-X Vision', icon: Shield },
    { id: 'demo', path: '/demo', label: 'Live Multi-Tenant Demo', icon: Terminal },
    { id: 'request', path: '/request', label: 'Request a Service', icon: Cpu },
  ];

  const getActiveTab = () => {
    if (location.pathname.startsWith('/demo')) return 'demo';
    if (location.pathname.startsWith('/request')) return 'request';
    return 'landing';
  };

  const activeTab = getActiveTab();

  return (
    <header className="border-b border-white/15 bg-black sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        <div className="flex items-center justify-between h-20">
          {/* Logo with clean breathing room */}
          <div
            onClick={() => navigate('/')}
            className="cursor-pointer transition-opacity hover:opacity-85 py-2"
          >
            <SentinelLogo size={36} showText={true} />
          </div>

          {/* Navigation Tabs with balanced, comfortable spacing & clean minimalist buttons */}
          <nav className="flex items-center gap-3 sm:gap-4">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => navigate(item.path)}
                  className={`relative px-4 py-2.5 text-xs font-mono uppercase tracking-wider transition-all duration-150 flex items-center gap-2.5 rounded-none border ${
                    isActive
                      ? 'bg-white text-black border-white font-semibold shadow-sm'
                      : 'bg-black text-neutral-400 border-white/10 hover:text-white hover:border-white/30 hover:bg-neutral-950'
                  }`}
                >
                  <Icon size={14} className={isActive ? 'text-black' : 'text-neutral-400'} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
}
