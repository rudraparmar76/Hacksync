import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import { Globe, Check } from "lucide-react"; // Optional: icons for better UI

const LanguageSwitcher = () => {
  const { i18n } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);

  const languages = [
    { code: "en", label: "English", flag: "🇺🇸" },
    { code: "hi", label: "हिंदी", flag: "🇮🇳" },
    { code: "gu", label: "ગુજરાતી", flag: "🇮🇳" },
    { code: "mr", label: "मराठी", flag: "🇮🇳" },
    { code: "ta", label: "தமிழ்", flag: "🇮🇳" },
    { code: "kn", label: "ಕನ್ನಡ", flag: "🇮🇳" },
    { code: "pa", label: "ਪੰਜਾਬੀ", flag: "🇮🇳" }
  ];

  const handleSelect = (code) => {
    i18n.changeLanguage(code);
    localStorage.setItem("lang", code);
    setIsOpen(false);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.9, y: 10, originX: 1, originY: 1 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 10 }}
            className="mb-2 w-48 overflow-hidden rounded-2xl border border-gray-200 bg-white/90 p-2 shadow-xl backdrop-blur-md dark:border-gray-700 dark:bg-gray-900/90"
          >
            <div className="grid grid-cols-1 gap-1">
              {languages.map((lang) => (
                <button 
                  key={lang.code}
                  onClick={() => handleSelect(lang.code)}
                  className={`flex items-center justify-between rounded-lg px-3 py-2 text-sm transition-colors
                    ${i18n.language === lang.code 
                      ? "bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400" 
                      : "text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800"}`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-lg">{lang.flag}</span> 
                    <span className="font-medium">{lang.label}</span>
                  </div>
                  {i18n.language === lang.code && <Check size={14} strokeWidth={3} />}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 rounded-full bg-blue-600 px-4 py-3 font-semibold text-white shadow-lg transition-transform hover:scale-105 active:scale-95 dark:bg-blue-500"
      >
        <Globe size={20} />
        <span className="uppercase">{i18n.language}</span>
      </button>
    </div>
  );
};

export default LanguageSwitcher;