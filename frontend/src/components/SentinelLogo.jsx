import React from 'react';

/**
 * SentinelX Layered Logo
 * A layered, architectural 'X' composed of multiple precision isolation tiers,
 * representing the multi-layered security framework of tenant-isolated RAG.
 */
export default function SentinelLogo({ size = 32, showText = true, className = '' }) {
  return (
    <div className={`flex items-center gap-3 select-none ${className}`}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="shrink-0"
      >
        {/* Layer 0: Subtle Outer Grid & Corner Registration Marks */}
        <path d="M5 15 V5 H15" stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.4" />
        <path d="M85 5 H95 V15" stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.4" />
        <path d="M5 85 V95 H15" stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.4" />
        <path d="M85 95 H95 V85" stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.4" />

        {/* Layer 1: Outermost Isolation Shield (Diagonal Perimeter Brackets) */}
        <polygon
          points="20,10 32,10 50,32 68,10 80,10 58,38 80,64 68,64 50,42 32,64 20,64 42,38"
          fill="currentColor"
          fillOpacity="0.15"
          stroke="currentColor"
          strokeWidth="1.2"
        />

        {/* Layer 2: Middle Authorization Gate (Stepped Diamond Chevron Planes) */}
        <polygon
          points="26,18 36,18 50,34 64,18 74,18 56,40 76,64 64,64 50,47 36,64 24,64 44,40"
          fill="currentColor"
          fillOpacity="0.35"
          stroke="currentColor"
          strokeWidth="1.5"
        />

        {/* Layer 3: Inner Core Cryptographic Barrier (High-contrast Sharp Core 'X') */}
        <polygon
          points="32,24 42,24 50,34 58,24 68,24 54,42 70,60 60,60 50,48 40,60 30,60 46,42"
          fill="#ffffff"
          stroke="#000000"
          strokeWidth="0.8"
        />

        {/* Layer 4: Central Nexus Core Kernel */}
        <rect
          x="46"
          y="38"
          width="8"
          height="8"
          transform="rotate(45 50 42)"
          fill="#000000"
          stroke="#ffffff"
          strokeWidth="1.5"
        />
        <circle cx="50" cy="42" r="1.5" fill="#ffffff" />

        {/* Horizontal Security Boundary Baseline */}
        <line x1="12" y1="82" x2="88" y2="82" stroke="currentColor" strokeWidth="1" strokeDasharray="3 3" strokeOpacity="0.4" />
      </svg>

      {showText && (
        <div className="flex flex-col leading-none">
          <div className="flex items-center font-mono font-bold tracking-tight text-white text-base">
            <span>SENTINEL-</span>
            <span className="bg-white text-black px-1.5 py-0.5 text-xs font-black tracking-widest">X</span>
          </div>
        </div>
      )}
    </div>
  );
}
