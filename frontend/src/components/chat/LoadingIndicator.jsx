
import { motion } from 'framer-motion';

export default function LoadingIndicator() {
  return (
    <div className="loading-indicator">
      <div className="message ai">
        <div className="message-bubble loading-bubble">
          <div className="loading-content">
            <motion.div 
              className="loading-dots"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ repeat: Infinity, duration: 1.5 }}
            >
              {[0, 1, 2].map(i => (
                <motion.span 
                  key={i}
                  className="dot"
                  animate={{ y: [0, -6, 0] }}
                  transition={{ 
                    duration: 0.6, 
                    repeat: Infinity, 
                    delay: i * 0.2,
                    ease: "easeInOut" 
                  }}
                />
              ))}
            </motion.div>
            <span className="loading-text">Analyzing Request...</span>
          </div>
        </div>
      </div>
    </div>
  );
}
