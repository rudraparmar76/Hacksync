import React from "react";
import "@fortawesome/fontawesome-free/css/all.min.css";
import { useTranslation } from "react-i18next";

export default function Footer() {
  const { t } = useTranslation();

  return (
    <footer className="footer">
      <div className="footer-container">
        {/* BRAND */}
        <div className="footer-col brand">
          <div className="logo">
            <div className="logo-icon">🎯</div>
            <span>DeliberateAI</span>
          </div>
          <p className="brand-desc">
            {t("footer.brand.description")}
          </p>
        </div>

        {/* PRODUCT */}
        <div className="footer-col">
          <h4>{t("footer.product.title")}</h4>
          <ul>
            <li>
              <a href="#features">
                {t("footer.product.features")}
              </a>
            </li>
            <li>
              <a href="#pricing">
                {t("footer.product.pricing")}
              </a>
            </li>
            <li>
              <a href="#docs">
                {t("footer.product.documentation")}
              </a>
            </li>
            <li>
              <a href="#api">
                {t("footer.product.api")}
              </a>
            </li>
          </ul>
        </div>

        {/* COMPANY */}
        <div className="footer-col">
          <h4>{t("footer.company.title")}</h4>
          <ul>
            <li>
              <a href="#about">
                {t("footer.company.about")}
              </a>
            </li>
            <li>
              <a href="#blog">
                {t("footer.company.blog")}
              </a>
            </li>
            <li>
              <a href="#careers">
                {t("footer.company.careers")}
              </a>
            </li>
            <li>
              <a href="#contact">
                {t("footer.company.contact")}
              </a>
            </li>
          </ul>
        </div>
      </div>

      {/* BOTTOM */}
      <div className="footer-bottom">
        <p>
          © {new Date().getFullYear()} DeliberateAI.{" "}
          {t("footer.rights")}
        </p>

        <div className="social-icons">
          <a
            href="https://twitter.com"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Twitter"
            title="Twitter"
          >
            <i className="fa-brands fa-x-twitter"></i>
          </a>

          <a
            href="https://linkedin.com"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="LinkedIn"
            title="LinkedIn"
          >
            <i className="fa-brands fa-linkedin-in"></i>
          </a>

          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="GitHub"
            title="GitHub"
          >
            <i className="fa-brands fa-github"></i>
          </a>
        </div>
      </div>
    </footer>
  );
}
