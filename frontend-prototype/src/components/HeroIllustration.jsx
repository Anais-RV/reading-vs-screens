export default function HeroIllustration() {
  return (
    <svg viewBox="0 0 320 240" className="hero-illustration" aria-hidden="true">
      {/* Background */}
      <rect width="320" height="240" fill="none" />

      {/* PHONE - Left side (negative) */}
      <g opacity="0.6">
        {/* Phone frame */}
        <rect x="20" y="40" width="100" height="160" rx="8" fill="#666" stroke="#333" strokeWidth="2" />
        <rect x="25" y="45" width="90" height="150" fill="#333" />

        {/* Scrolling content - lines */}
        <rect x="30" y="50" width="80" height="3" fill="#888" opacity="0.5" />
        <rect x="30" y="58" width="75" height="2" fill="#888" opacity="0.4" />
        <rect x="30" y="63" width="80" height="3" fill="#888" opacity="0.5" />
        <rect x="30" y="71" width="70" height="2" fill="#888" opacity="0.3" />

        {/* Flickering eyes icon to show addiction */}
        <circle cx="60" cy="120" r="3" fill="#ff6e60" />
        <circle cx="75" cy="120" r="3" fill="#ff6e60" />

        {/* Label */}
        <text x="70" y="210" fontSize="12" fontWeight="600" fill="#666" textAnchor="middle">
          Scroll
        </text>
      </g>

      {/* Arrow in center */}
      <g>
        <line x1="140" y1="120" x2="180" y2="120" stroke="#0b6b67" strokeWidth="3" markerEnd="url(#arrowhead)" />
        <defs>
          <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <polygon points="0 0, 10 3, 0 6" fill="#0b6b67" />
          </marker>
        </defs>
      </g>

      {/* BOOK - Right side (positive) */}
      <g>
        {/* Book cover */}
        <rect x="200" y="40" width="100" height="160" rx="4" fill="#0b6b67" stroke="#084f4c" strokeWidth="2" />

        {/* Book spine effect */}
        <line x1="200" y1="40" x2="195" y2="45" stroke="#084f4c" strokeWidth="2" />
        <line x1="200" y1="200" x2="195" y2="195" stroke="#084f4c" strokeWidth="2" />
        <path d="M 200 40 L 195 45 L 195 195 L 200 200" fill="none" stroke="#084f4c" strokeWidth="1.5" />

        {/* Book title (decorative lines) */}
        <rect x="220" y="70" width="60" height="4" fill="#ffd5c2" rx="2" />
        <rect x="220" y="85" width="50" height="3" fill="#ffd5c2" opacity="0.8" rx="2" />

        {/* Book content (reading indicator) */}
        <rect x="215" y="100" width="70" height="2" fill="#e8d9c8" opacity="0.6" />
        <rect x="215" y="107" width="68" height="2" fill="#e8d9c8" opacity="0.5" />
        <rect x="215" y="114" width="65" height="2" fill="#e8d9c8" opacity="0.4" />
        <rect x="215" y="121" width="70" height="2" fill="#e8d9c8" opacity="0.6" />
        <rect x="215" y="128" width="60" height="2" fill="#e8d9c8" opacity="0.5" />

        {/* Brain icon - thinking */}
        <circle cx="250" cy="160" r="12" fill="none" stroke="#ffd5c2" strokeWidth="2" />
        <path d="M 245 158 Q 250 152 255 158" fill="none" stroke="#ffd5c2" strokeWidth="1.5" />

        {/* Label */}
        <text x="250" y="210" fontSize="12" fontWeight="600" fill="#0b6b67" textAnchor="middle">
          Leer
        </text>
      </g>

      {/* Bottom message */}
      <text x="160" y="235" fontSize="11" fontStyle="italic" fill="#5d5a57" textAnchor="middle">
        Recupera tu tiempo. Criterio regalado.
      </text>
    </svg>
  );
}
