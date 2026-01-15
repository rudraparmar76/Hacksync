import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

import { useAuth } from "../context/AuthContext";
import AuthWrapper from "../components/AuthWrapper";
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
} from "firebase/auth";
import { saveUserToFirestore } from "../utils/saveUserToFirestore";
import { auth, googleProvider } from "../auth/firebase";

export default function Auth({ isSignup }) {
  const navigate = useNavigate();
  const { t } = useTranslation();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showSuccessBox, setShowSuccessBox] = useState(false);
  const [passwordVisible, setPasswordVisible] = useState(false);

  // Password validation
  const validatePassword = (pwd) => {
    return {
      hasLength: pwd.length >= 8,
      hasNumber: /\d/.test(pwd),
      hasUppercase: /[A-Z]/.test(pwd),
    };
  };

  const passwordRequirements = isSignup
    ? validatePassword(password)
    : null;

  const isPasswordValid =
    !isSignup ||
    (passwordRequirements?.hasLength &&
      passwordRequirements?.hasNumber &&
      passwordRequirements?.hasUppercase);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (!email || !password) {
        setError(t("auth.errors.required"));
        return;
      }

      if (isSignup && password.length < 8) {
        setError(t("auth.errors.passwordLength"));
        return;
      }

      let userCredential;

      if (isSignup) {
        userCredential = await createUserWithEmailAndPassword(
          auth,
          email,
          password
        );
      } else {
        userCredential = await signInWithEmailAndPassword(
          auth,
          email,
          password
        );
      }

      await saveUserToFirestore(userCredential.user);

      setShowSuccessBox(true);
      setTimeout(() => navigate("/"), 1500);
    } catch (err) {
      if (err.code === "auth/email-already-in-use") {
        setError(t("auth.errors.emailExists"));
      } else if (err.code === "auth/wrong-password") {
        setError(t("auth.errors.wrongPassword"));
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleAuth = async () => {
    setLoading(true);
    setError("");

    try {
      const result = await signInWithPopup(auth, googleProvider);
      await saveUserToFirestore(result.user);

      setShowSuccessBox(true);
      setTimeout(() => navigate("/"), 1500);
    } catch (err) {
      setError(t("auth.errors.googleFail"));
    } finally {
      setLoading(false);
    }
  };

  // Forgot password screen
  if (showForgotPassword) {
    return (
      <AuthWrapper>
        <div className="page">
          <div className="card">
            <header>
              <h1>{t("auth.reset.title")}</h1>
              <p>{t("auth.reset.subtitle")}</p>
            </header>

            <div className="form-set">
              <form
                className="form active"
                onSubmit={(e) => {
                  e.preventDefault();
                  setShowForgotPassword(false);
                  alert(t("auth.reset.sent"));
                }}
              >
                <div className="field">
                  <div className="input-shell">
                    <span className="icon">✉️</span>
                    <input
                      type="email"
                      placeholder={t("auth.placeholders.email")}
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </div>
                </div>

                <motion.button
                  type="submit"
                  className="primary block"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  {t("auth.reset.send")}
                </motion.button>

                <button
                  type="button"
                  className="ghost"
                  onClick={() => setShowForgotPassword(false)}
                  style={{ width: "100%", marginTop: "10px" }}
                >
                  ← {t("auth.reset.back")}
                </button>
              </form>
            </div>
          </div>
        </div>
      </AuthWrapper>
    );
  }

  return (
    <AuthWrapper>
      <div className="page">
        <motion.div
          className="card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="logo-wrap">
            <div className="logo-bg" />
            <div className="auth-logo">
              {isSignup ? "✍️" : "🔐"}
            </div>
          </div>

          <header>
            <h1>
              {isSignup
                ? t("auth.signup.title")
                : t("auth.login.title")}
            </h1>
            <p>
              {isSignup
                ? t("auth.signup.subtitle")
                : t("auth.login.subtitle")}
            </p>
          </header>

          {error && <div className="error">{error}</div>}

          <div className="form-set">
            <form className="form active" onSubmit={handleSubmit}>
              <div className="field">
                <label>{t("auth.labels.email")}</label>
                <div className="input-shell">
                  <span className="icon">✉️</span>
                  <input
                    type="email"
                    placeholder={t("auth.placeholders.email")}
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>
              </div>

              <div className="field">
                <label>{t("auth.labels.password")}</label>
                <div className="input-shell">
                  <span className="icon">🔒</span>
                  <input
                    type={passwordVisible ? "text" : "password"}
                    placeholder={t("auth.placeholders.password")}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                  <button
                    type="button"
                    className="ghost"
                    onClick={() =>
                      setPasswordVisible(!passwordVisible)
                    }
                  >
                    {passwordVisible ? "👁️" : "🙈"}
                  </button>
                </div>
              </div>

              {isSignup && password && (
                <motion.ul
                  className="requirements"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <li
                    className={
                      passwordRequirements.hasLength ? "ok" : ""
                    }
                  >
                    {t("auth.passwordRules.length")}
                  </li>
                  <li
                    className={
                      passwordRequirements.hasNumber ? "ok" : ""
                    }
                  >
                    {t("auth.passwordRules.number")}
                  </li>
                  <li
                    className={
                      passwordRequirements.hasUppercase ? "ok" : ""
                    }
                  >
                    {t("auth.passwordRules.uppercase")}
                  </li>
                </motion.ul>
              )}

              {!isSignup && (
                <div className="row between">
                  <button
                    type="button"
                    className="link"
                    onClick={() => setShowForgotPassword(true)}
                  >
                    {t("auth.forgot")}
                  </button>
                </div>
              )}

              <motion.button
                type="submit"
                className="primary block"
                disabled={loading || (isSignup && !isPasswordValid)}
              >
                {loading
                  ? t("auth.loading")
                  : isSignup
                  ? t("auth.signup.button")
                  : t("auth.login.button")}
              </motion.button>

              <motion.button
                type="button"
                className="secondary block"
                onClick={handleGoogleAuth}
                disabled={loading}
              >
                🔗 {t("auth.google")}
              </motion.button>

              <p className="switch">
                {isSignup
                  ? t("auth.switch.loginText")
                  : t("auth.switch.signupText")}{" "}
                <a
                  className="link"
                  onClick={() =>
                    navigate(isSignup ? "/login" : "/signup")
                  }
                >
                  {isSignup
                    ? t("auth.switch.login")
                    : t("auth.switch.signup")}
                </a>
              </p>
            </form>
          </div>

          {showSuccessBox && (
            <motion.div className="success-box show">
              ✓{" "}
              {isSignup
                ? t("auth.success.signup")
                : t("auth.success.login")}
            </motion.div>
          )}
        </motion.div>
      </div>
    </AuthWrapper>
  );
}
