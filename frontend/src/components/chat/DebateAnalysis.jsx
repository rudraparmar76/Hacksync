
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const SectionHeader = ({ icon, title, color = "#8ef3ff" }) => (
  <h3 style={{ 
    display: 'flex', 
    alignItems: 'center', 
    gap: '10px', 
    color: color, 
    margin: '24px 0 16px', 
    fontSize: '1.1em',
    borderBottom: `1px solid ${color}40`,
    paddingBottom: '8px'
  }}>
    <span style={{ fontSize: '1.4em' }}>{icon}</span> 
    {title}
  </h3>
);

const Card = ({ children, className = "" }) => (
  <div className={`analysis-card ${className}`} style={{
    background: 'rgba(255, 255, 255, 0.03)',
    borderRadius: '12px',
    padding: '16px',
    border: '1px solid rgba(142, 243, 255, 0.1)',
    marginBottom: '16px'
  }}>
    {children}
  </div>
);

const DebateFlow = ({ debate }) => {
  const [isOpen, setIsOpen] = useState(false);
  
  const { factor, claim, attack, defense, counter, decision } = debate;

  return (
    <div className="debate-flow-container" style={{ marginBottom: '20px' }}>
      <motion.div 
        className="debate-factor-header"
        onClick={() => setIsOpen(!isOpen)}
        style={{
          background: 'linear-gradient(90deg, rgba(142, 243, 255, 0.1), transparent)',
          padding: '12px 16px',
          borderRadius: '8px',
          cursor: 'pointer',
          borderLeft: '4px solid #8ef3ff',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <div>
          <div style={{ color: '#8ef3ff', fontWeight: 'bold', fontSize: '1.1em' }}>{factor.name}</div>
          <div style={{ color: '#a7adbf', fontSize: '0.9em', marginTop: '4px' }}>{factor.description}</div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span className={`status-badge ${decision.status === 'ACCEPTED' ? 'approved' : 'rejected'}`}>
             {decision.status} ({decision.score}/10)
          </span>
          <motion.span animate={{ rotate: isOpen ? 180 : 0 }}>▼</motion.span>
        </div>
      </motion.div>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            style={{ overflow: 'hidden' }}
          >
            <div style={{ padding: '16px 8px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
              
              <div className="debate-exchange-grid">
                {/* Round 1 */}
                <div className="exchange-row">
                  <div className="speech-bubble blue">
                    <div className="bubble-label">🔵 CLAIM</div>
                    {claim}
                  </div>
                  <div className="vs-connector">⚡</div>
                  <div className="speech-bubble red">
                    <div className="bubble-label">🔴 ATTACK</div>
                    {attack}
                  </div>
                </div>

                {/* Round 2 */}
                <div className="exchange-row">
                  <div className="speech-bubble blue">
                    <div className="bubble-label">🔵 DEFENSE</div>
                    {defense}
                  </div>
                  <div className="vs-connector">⚡</div>
                  <div className="speech-bubble red">
                    <div className="bubble-label">🔴 COUNTER</div>
                    {counter}
                  </div>
                </div>
              </div>

              {/* Verdict */}
              <div className="verdict-box" style={{
                background: decision.status === 'ACCEPTED' ? 'rgba(74, 222, 128, 0.1)' : 'rgba(248, 113, 113, 0.1)',
                border: `1px solid ${decision.status === 'ACCEPTED' ? '#4ade80' : '#f87171'}`,
                borderRadius: '8px',
                padding: '16px',
                marginTop: '8px'
              }}>
                <div style={{ 
                  color: decision.status === 'ACCEPTED' ? '#4ade80' : '#f87171',
                  fontWeight: 'bold',
                  marginBottom: '8px',
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '8px'
                }}>
                  ⚖️ MARSHAL'S VERDICT
                </div>
                <div style={{ color: '#e2e8f0', marginBottom: '8px' }}>
                  {decision.verdict}
                </div>
                <div style={{ 
                  fontSize: '0.9em', 
                  background: 'rgba(0,0,0,0.2)', 
                  padding: '8px', 
                  borderRadius: '6px',
                  borderLeft: `2px solid ${decision.status === 'ACCEPTED' ? '#4ade80' : '#f87171'}`
                }}>
                  <strong>🏆 Winning Point:</strong> {decision.winning_argument}
                </div>
              </div>

            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default function DebateAnalysis({ analysisData }) {
  if (!analysisData) return null;

  const { final_report, debates, decision_path } = analysisData;

  return (
    <div className="debate-analysis-view" style={{ fontFamily: 'Inter, sans-serif' }}>
      
      {/* 1. EXECUTIVE SUMMARY */}
      <Card className="executive-summary">
        <SectionHeader icon="📑" title="Executive Summary" />
        <p style={{ lineHeight: '1.6', fontSize: '1.05em' }}>
          {final_report.executive_summary}
        </p>
        <div style={{ marginTop: '16px', fontSize: '0.95em', color: '#a7adbf', fontStyle: 'italic' }}>
          <strong>Why: </strong> {final_report.why_this_decision}
        </div>
      </Card>

      {/* 2. KEY INSIGHTS & RISKS */}
      <div className="insights-grid" style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '16px' }}>
        <Card>
          <SectionHeader icon="💡" title="Key Insights" color="#fbbf24" />
          <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {final_report.key_insights.map((insight, i) => (
              <li key={i}>{insight}</li>
            ))}
          </ul>
        </Card>
        
        {final_report.risk_assessment && (
           <Card>
            <SectionHeader icon="⚠️" title="Risk Assessment" color="#f87171" />
            <p>{final_report.risk_assessment}</p>
           </Card>
        )}
      </div>

      {/* 3. RECOMMENDATIONS */}
      {final_report.strategic_recommendations && final_report.strategic_recommendations.length > 0 && (
         <Card>
            <SectionHeader icon="🚀" title="Strategic Recommendations" color="#a78bfa" />
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {final_report.strategic_recommendations.map((rec, i) => (
                <div key={i} style={{ 
                  background: 'rgba(167, 139, 250, 0.1)', 
                  padding: '12px', 
                  borderRadius: '8px',
                  borderLeft: '3px solid #a78bfa'
                }}>
                  <div style={{ fontWeight: 'bold', color: '#ddd' }}>{rec.strategy}</div>
                  <div style={{ marginTop: '4px', color: '#a7adbf' }}>→ {rec.action}</div>
                  {rec.rationale && <div style={{ marginTop: '6px', fontSize: '0.9em', opacity: 0.8 }}>Justification: {rec.rationale}</div>}
                </div>
              ))}
            </div>
         </Card>
      )}

      {/* 4. DEBATE DETAILS */}
      {debates && debates.length > 0 && (
        <div className="debates-section" style={{ marginTop: '32px' }}>
          <h2 style={{ 
            textAlign: 'center', 
            marginBottom: '24px', 
            color: '#fff', 
            textTransform: 'uppercase', 
            letterSpacing: '2px', 
            fontSize: '1em',
            opacity: 0.8 
          }}>
            Detailed Factor Analysis
          </h2>
          
          {debates.map((debate, index) => (
            <DebateFlow key={index} debate={debate} />
          ))}
        </div>
      )}

    </div>
  );
}
