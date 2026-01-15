import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { signOut } from "firebase/auth";
import { auth } from "../auth/firebase";
import { useTranslation } from "react-i18next";

export default function Settings() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { t } = useTranslation();

  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate("/login");
    } catch (err) {
      console.error("Logout failed:", err);
    }
  };

  return (
    <div className="settings-page">
      {/* 🔝 HEADER */}
      <div className="settings-header">
        <button
          className="btn-secondary"
          onClick={() => navigate(-1)}
        >
          ← {t("settings.back")}
        </button>
        <h2>{t("settings.title")}</h2>
      </div>

      {/* 👤 PROFILE */}
      <div className="settings-section">
        <h3>{t("settings.profile.title")}</h3>

        <div className="profile-card">
          <div className="profile-avatar">
            {user?.email?.[0]?.toUpperCase()}
          </div>

          <div className="profile-info">
            <p className="profile-email">{user?.email}</p>
            <p className="profile-meta">
              {t("settings.profile.signedIn")}
            </p>
          </div>
        </div>
      </div>

      {/* ⚙️ PREFERENCES */}
      <div className="settings-section">
        <h3>{t("settings.preferences.title")}</h3>

        <div className="settings-row">
          <span>{t("settings.preferences.theme")}</span>
          <button className="btn-secondary small">
            {t("settings.preferences.dark")}
          </button>
        </div>

        <div className="settings-row">
          <span>{t("settings.preferences.notifications")}</span>
          <button className="btn-secondary small">
            {t("settings.preferences.enabled")}
          </button>
        </div>
      </div>

      {/* 🔐 ACCOUNT */}
      <div className="settings-section danger">
        <h3>{t("settings.account.title")}</h3>

        <button
          className="btn-danger"
          onClick={handleLogout}
        >
          {t("settings.account.logout")}
        </button>
      </div>
    </div>
  );
}
