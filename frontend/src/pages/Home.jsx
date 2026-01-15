import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next'; // Added for translation
import Header from '../components/Header';
import Footer from '../components/Footer';
import FeatureCard from '../components/FeatureCard';
import AnimatedSphere from '../components/AnimatedSphere';
import supportImg from "../assets/agent-supportive.jpeg";
import synthImg from "../assets/agent-synthesizer.jpeg";
import challengerImg from "../assets/agent-challenger.jpeg";

export default function Home() {
  const navigate = useNavigate();
  const { t } = useTranslation(); // Initialize translation hook

  const features = [
    {
      icon: '🧠',
      title: t('home.features.opposing.title'),
      description: t('home.features.opposing.desc')
    },
    {
      icon: '🤝',
      title: t('home.features.support.title'),
      description: t('home.features.support.desc')
    },
    {
      icon: '⚖️',
      title: t('home.features.synthesizer.title'),
      description: t('home.features.synthesizer.desc')
    },
    {
      icon: '💡',
      title: t('home.features.collaboration.title'),
      description: t('home.features.collaboration.desc')
    },
    {
      icon: '📊',
      title: t('home.features.analytics.title'),
      description: t('home.features.analytics.desc')
    },
    {
      icon: '🎯',
      title: t('home.features.action.title'),
      description: t('home.features.action.desc')
    }
  ];

  const processSteps = [
    {
      number: '01',
      title: t('home.process.steps.define.title'),
      description: t('home.process.steps.define.desc')
    },
    {
      number: '02',
      title: t('home.process.steps.deliberate.title'),
      description: t('home.process.steps.deliberate.desc')
    },
    {
      number: '03',
      title: t('home.process.steps.synthesize.title'),
      description: t('home.process.steps.synthesize.desc')
    },
    {
      number: '04',
      title: t('home.process.steps.act.title'),
      description: t('home.process.steps.act.desc')
    }
  ];

  return (
    <div>
      <Header />
      
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-badge">
          <span>{t('home.hero.badge')}</span>
        </div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="hero-title">
            {t('home.hero.title_part1')}{' '}
            <span className="gradient-text">{t('home.hero.title_gradient')}</span>
          </h1>
        </motion.div>

        <motion.p
          className="hero-subtitle"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          {t('home.hero.subtitle')}
        </motion.p>

        <motion.div
          className="hero-buttons"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          <button 
            className="btn-primary" 
            onClick={() => navigate('/signup')}
            style={{ cursor: 'pointer' }}
          >
            {t('home.hero.btn_primary')}
          </button>
          <button 
            className="btn-secondary"
            style={{ cursor: 'pointer' }}
          >
            {t('home.hero.btn_secondary')}
          </button>
        </motion.div>

        <div className="agent-connection-wrapper">
          {/* LEFT */}
          <div className="agent left">
            <AnimatedSphere variant="cyan" label={t('home.agents.supportive')} image={supportImg} />
          </div>

          <div className="agent center">
            {/* CONNECTORS ORIGINATE HERE */}
            <span className="connector left-line" />
            <span className="connector right-line" />

            <AnimatedSphere
              variant="purple"
              label={t('home.agents.synthesizer')}
              image={synthImg}
            />
          </div>

          {/* RIGHT */}
          <div className="agent right">
            <AnimatedSphere variant="orange" label={t('home.agents.challenger')} image={challengerImg} />
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works">
        <h2>{t('home.features_section.title')}</h2>
        <p className="section-subtitle">
          {t('home.features_section.subtitle')}
        </p>
        
        <div className="features-grid">
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
              delay={index * 0.1}
            />
          ))}
        </div>
      </section>

      {/* Deliberation Process - Vertical Timeline */}
      <section className="deliberation-process">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true, margin: '-50px' }}
        >
          <h2>{t('home.process_section.title')}</h2>
          <p className="section-subtitle">
            {t('home.process_section.subtitle')}
          </p>
        </motion.div>

        <div className="timeline-container">
          <motion.div 
            className="timeline-line"
            initial={{ scaleY: 0 }}
            whileInView={{ scaleY: 1 }}
            transition={{ duration: 1.5, ease: 'easeInOut' }}
            viewport={{ once: true, margin: '-100px' }}
            style={{ originY: 0 }}
          />
          
          {processSteps.map((step, index) => (
            <motion.div
              key={index}
              className={`timeline-item ${index % 2 === 0 ? 'left' : 'right'}`}
              initial={{
                opacity: 0,
                x: index % 2 === 0 ? -80 : 80
              }}
              whileInView={{
                opacity: 1,
                x: 0
              }}
              transition={{
                duration: 0.7,
                delay: index * 0.15,
                ease: 'easeOut'
              }}
              viewport={{ once: true, margin: '-80px' }}
            >
              <div className="timeline-content">
                <motion.div
                  className="timeline-card"
                  whileHover={{ y: -8, boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)' }}
                  initial={{ scale: 0.95 }}
                  whileInView={{ scale: 1 }}
                  transition={{ duration: 0.5, delay: index * 0.15 + 0.2 }}
                  viewport={{ once: true, margin: '-80px' }}
                >
                  <div className="step-number">{step.number}</div>
                  <h3>{step.title}</h3>
                  <p>{step.description}</p>
                </motion.div>
              </div>
              
              <motion.div
                className="timeline-dot"
                initial={{ scale: 0, opacity: 0 }}
                whileInView={{ scale: 1, opacity: 1 }}
                transition={{
                  duration: 0.5,
                  delay: index * 0.15 + 0.3,
                  ease: 'backOut'
                }}
                viewport={{ once: true, margin: '-80px' }}
                whileHover={{ scale: 1.2 }}
              />
            </motion.div>
          ))}
        </div>

        <motion.div
          className="process-spheres"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          viewport={{ once: true, margin: '-100px' }}
        >
          <motion.div
            className="process-sphere"
            animate={{ y: [0, -20, 0] }}
            transition={{ duration: 4, repeat: Infinity }}
          >
            <AnimatedSphere variant="cyan" label="" delay={0} />
          </motion.div>
          <motion.div
            className="process-sphere"
            animate={{ y: [0, -20, 0] }}
            transition={{ duration: 4, repeat: Infinity, delay: 0.2 }}
          >
            <AnimatedSphere variant="purple" label="" delay={0.2} />
          </motion.div>
          <motion.div
            className="process-sphere"
            animate={{ y: [0, -20, 0] }}
            transition={{ duration: 4, repeat: Infinity, delay: 0.4 }}
          >
            <AnimatedSphere variant="orange" label="" delay={0.4} />
          </motion.div>
        </motion.div>
      </section>

      <Footer />
    </div>
  );
}