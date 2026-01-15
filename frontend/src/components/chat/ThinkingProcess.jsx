
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTranslation } from 'react-i18next';

const AgentIcon = ({ agent }) => {
  switch (agent) {
    case 'Summarizer': return <span title="Summarizer">📝</span>;
    case 'FactorAgent': return <span title="Factor Agent">🔍</span>;
    case 'DebateEngine': return <span title="Debate Engine">⚖️</span>;
    case 'SynthesizerAgent': return <span title="Synthesizer">✨</span>;
    default: return <span>🤖</span>;
  }
};

const DebateStep = ({ step }) => {
  const { output } = step;
  if (!output) return null;

  const isApproved = output.status === 'APPROVED';
  // Use a fallback for score if it's missing or not a number
  const score = typeof output.score === 'number' ? output.score : 0;
  
  return (
    <div className="debate-card">
      <div className="debate-header">
        <span className={`status-badge ${isApproved ? 'approved' : 'rejected'}`}>
          {isApproved ? '✅ APPROVED' : '❌ REJECTED'}
        </span>
        <span className="debate-score">Score: {score.toFixed(1)}</span>
      </div>
      
      {/* Score Bar */}
      <div className="score-track">
        <motion.div 
          className="score-fill"
          initial={{ width: 0 }}
          animate={{ width: `${Math.min(score * 10, 100)}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          style={{ 
            backgroundColor: isApproved ? '#4ade80' : '#f87171'
          }}
        />
      </div>

      {output.winning_argument && (
        <div className="winning-argument">
          <strong>🏆 Winning Argument:</strong>
          <p>{output.winning_argument}</p>
        </div>
      )}
    </div>
  );
};

export default function ThinkingProcess({ steps }) {
  const [isOpen, setIsOpen] = useState(false);
  const { t } = useTranslation();

  if (!steps || steps.length === 0) return null;

  return (
    <div className="thinking-process-container">
      <button 
        className="thinking-toggle"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className="brain-icon">🧠</span>
        <span className="thinking-label">
          Thinking Process
          <span className="step-count">({steps.length} steps)</span>
        </span>
        <motion.span 
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
          className="chevron"
        >
          ▼
        </motion.span>
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="thinking-content"
          >
            <div className="timeline-line" />
            
            {steps.map((step, idx) => (
              <motion.div 
                key={idx}
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: idx * 0.05 }}
                className="thinking-step"
              >
                <div className="step-icon-wrapper">
                  <div className="step-icon">
                    <AgentIcon agent={step.agent} />
                  </div>
                </div>

                <div className="step-details">
                  <div className="step-header">
                    <span className="agent-name">{step.agent}</span>
                    <span className="step-stage">{step.stage}</span>
                    <span className="step-time">{step.elapsed_ms}ms</span>
                  </div>

                  {step.factor_name && (
                    <div className="factor-tag">
                      Factor: {step.factor_name}
                    </div>
                  )}

                  {/* Render specialized cards based on agent */}
                  {step.agent === 'DebateEngine' ? (
                    <DebateStep step={step} />
                  ) : (
                    // Default minimal output for other agents
                    step.output && (
                      <div className="step-output-json">
                        {/* Only show small summary if available, usually logic is hidden */}
                        {step.output.summary_length && <span>Synthesized {step.output.summary_length} chars</span>}
                        {step.output.factor_count && <span>Extracted {step.output.factor_count} factors</span>}
                        {step.output.report_generated && <span>Report Generated</span>}
                      </div>
                    )
                  )}
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
