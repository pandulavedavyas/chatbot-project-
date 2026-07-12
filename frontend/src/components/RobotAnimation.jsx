import { motion } from 'framer-motion';

const RobotAnimation = ({ size = 'large' }) => {
  const sizeClasses = {
    small: 'w-16 h-16',
    medium: 'w-24 h-24',
    large: 'w-32 h-32',
  };

  return (
    <motion.div
      className={`${sizeClasses[size]} relative`}
      animate={{ y: [0, -10, 0] }}
      transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
    >
      <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-lg">
        <defs>
          <linearGradient id="robotGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#3b82f6" />
            <stop offset="100%" stopColor="#1d4ed8" />
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        {/* Head */}
        <rect x="25" y="20" width="50" height="40" rx="10" fill="url(#robotGradient)" filter="url(#glow)" />

        {/* Eyes */}
        <motion.circle cx="38" cy="38" r="5" fill="white" animate={{ scale: [1, 1.1, 1] }} transition={{ duration: 2, repeat: Infinity }} />
        <motion.circle cx="62" cy="38" r="5" fill="white" animate={{ scale: [1, 1.1, 1] }} transition={{ duration: 2, repeat: Infinity, delay: 0.5 }} />
        <circle cx="38" cy="38" r="2" fill="#0f172a" />
        <circle cx="62" cy="38" r="2" fill="#0f172a" />

        {/* Mouth */}
        <path d="M 38 50 Q 50 56 62 50" stroke="white" strokeWidth="2" fill="none" />

        {/* Body */}
        <rect x="30" y="62" width="40" height="25" rx="6" fill="url(#robotGradient)" filter="url(#glow)" />

        {/* Arms */}
        <motion.rect x="15" y="65" width="12" height="16" rx="4" fill="#3b82f6" animate={{ rotate: [0, -5, 0] }} transition={{ duration: 2, repeat: Infinity }} style={{ transformOrigin: '27px 65px' }} />
        <motion.rect x="73" y="65" width="12" height="16" rx="4" fill="#3b82f6" animate={{ rotate: [0, 5, 0] }} transition={{ duration: 2, repeat: Infinity, delay: 0.5 }} style={{ transformOrigin: '73px 65px' }} />

        {/* Chest Light */}
        <motion.circle cx="50" cy="74" r="3.5" fill="white" animate={{ opacity: [0.5, 1, 0.5] }} transition={{ duration: 1.5, repeat: Infinity }} />
      </svg>
    </motion.div>
  );
};

export default RobotAnimation;
