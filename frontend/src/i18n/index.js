import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import all JSON files
import enTrans from './locales/en.json';
import hiTrans from './locales/hi.json';
import guTrans from './locales/gu.json';
import mrTrans from './locales/mr.json';
import taTrans from './locales/ta.json';
import knTrans from './locales/kn.json';
import paTrans from './locales/pa.json';

i18n
  .use(LanguageDetector) 
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: enTrans },
      hi: { translation: hiTrans },
      gu: { translation: guTrans },
      mr: { translation: mrTrans },
      ta: { translation: taTrans },
      kn: { translation: knTrans },
      pa: { translation: paTrans }
    },
    // Priority: LocalStorage -> Detected Lang -> Default 'en'
    lng: localStorage.getItem("lang") || undefined, 
    fallbackLng: 'en',
    debug: true, 
    interpolation: {
      escapeValue: false,
    },
    react: {
      useSuspense: false 
    }
  });

export default i18n;