import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { signOut } from "firebase/auth";
import { auth } from "../auth/firebase";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";

export default function Header() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { t, i18n } = useTranslation();

  const [isDark, setIsDark] = useState(true);
  const [showLangMenu, setShowLangMenu] = useState(false);
  const menuRef = useRef(null);

  // Complete language list
  const languages = [
    { code: "en", label: "English", flag: "🇺🇸" },
    { code: "hi", label: "हिंदी", flag: "🇮🇳" },
    { code: "gu", label: "ગુજરાતી", flag: "🇮🇳" },
    { code: "mr", label: "मराठी", flag: "🇮🇳" },
    { code: "ta", label: "தமிழ்", flag: "🇮🇳" },
    { code: "kn", label: "ಕನ್ನಡ", flag: "🇮🇳" },
    { code: "pa", label: "ਪੰਜਾਬੀ", flag: "🇮🇳" }
  ];

  const handleLogout = async () => {
    await signOut(auth);
    navigate("/login");
  };

  const toggleTheme = () => {
    const newTheme = !isDark;
    setIsDark(newTheme);
    if (newTheme) {
      document.documentElement.classList.remove("light-theme");
      document.documentElement.classList.add("dark-theme");
    } else {
      document.documentElement.classList.remove("dark-theme");
      document.documentElement.classList.add("light-theme");
    }
  };

  const changeLanguage = (code) => {
    i18n.changeLanguage(code);
    localStorage.setItem("lang", code);
    setShowLangMenu(false);
  };

  useEffect(() => {
    document.documentElement.classList.add("dark-theme");
    
    // Close dropdown when clicking outside
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setShowLangMenu(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <header className="header">
      <div className="header-container">
        {/* Logo */}
        <div className="logo" onClick={() => navigate("/")} style={{ cursor: "pointer" }}>
          <div className="logo-icon">⚖️</div>
          <span className="logo-text">DeliberateAI</span>
        </div>

        {/* Navigation */}
        <nav className="nav">
          <a onClick={() => navigate("/")} style={{ cursor: "pointer" }}>
            {t("nav.home")}
          </a>
          <a onClick={() => navigate("/chat")} style={{ cursor: "pointer" }}>
            {t("nav.chat")}
          </a>
        </nav>

        {/* Right actions */}
        <div className="auth-buttons">
          
          {/* 🌐 Modern Language Dropdown */}
          <div className="lang-dropdown-wrapper" ref={menuRef}>
            <button 
              className="lang-trigger-btn" 
              onClick={() => setShowLangMenu(!showLangMenu)}
            >
              🌐 {i18n.language ? i18n.language.toUpperCase() : 'EN'}

              <motion.span
                animate={{ rotate: showLangMenu ? 180 : 0 }}
                style={{ display: 'inline-block', fontSize: '10px', marginLeft: '4px' }}
              >
                ▼
              </motion.span>
            </button>
            
            <AnimatePresence>
              {showLangMenu && (
                <motion.div 
                  className="lang-dropdown-menu"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                >
                  {languages.map((lang) => (
                    <button 
                      key={lang.code}
                      className={`lang-menu-item ${i18n.language === lang.code ? "active" : ""}`}
                      onClick={() => changeLanguage(lang.code)}
                    >
                      <span className="flag-icon">{lang.flag}</span>
                      <span className="lang-name">{lang.label}</span>
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {user ? (
            <>
              <span className="welcome-text">
                {user.displayName || user.email}
              </span>
              <button className="btn-secondary" onClick={handleLogout}>
                {t("nav.logout")}
              </button>
              <button className="theme-toggle" onClick={toggleTheme}>
                {isDark ? "🌙" : "☀️"}
              </button>
            </>
          ) : (
            <>
              <button className="btn-secondary" onClick={() => navigate("/login")}>
                {t("nav.login")}
              </button>
              <button className="btn-primary" onClick={() => navigate("/signup")}>
                {t("nav.getStarted")}
              </button>
              <button className="theme-toggle" onClick={toggleTheme}>
                {isDark ? "🌙" : "☀️"}
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}