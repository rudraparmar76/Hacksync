import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { createChat, listenToUserChats, deleteChat } from "../../utils/chatService";
import { useTranslation } from "react-i18next";

export default function ChatSidebar({ activeChatId, setActiveChatId }) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [chats, setChats] = useState([]);
  const { t } = useTranslation();

  useEffect(() => {
    if (!user) return;
    
    // Use real-time listener instead of one-time load
    const unsub = listenToUserChats(user.uid, (data) => {
      setChats(data);
    });

    return () => unsub();
  }, [user]);

  const handleNewChat = async () => {
    if (!user) return;
    try {
      const chatId = await createChat(user.uid, t("sidebar.newChat"));
      setActiveChatId(chatId);
    } catch (err) {
      console.error("CHAT CREATION FAILED:", err);
    }
  };

  // ADD DELETE FUNCTION
  const handleDeleteChat = async (chatId) => {
    if (!user || !confirm(t("sidebar.deleteConfirm"))) return;
    
    try {
      await deleteChat(user.uid, chatId);
      
      // Reset active chat if deleted
      if (activeChatId === chatId) {
        setActiveChatId(null);
      }
    } catch (err) {
      console.error("DELETE FAILED:", err);
      alert(t("sidebar.deleteFailed"));
    }
  };

  return (
    <aside className="chat-sidebar">
      <div className="sidebar-top">
        <button className="btn-primary full" onClick={handleNewChat}>
          {t("sidebar.newChat")}
        </button>

        {chats.map((chat) => (
          <div 
            key={chat.id}
            className={`chat-item ${chat.id === activeChatId ? "active" : ""}`}
            onClick={() => setActiveChatId(chat.id)}
          >
            <div className="chat-content">
              {chat.title || t("sidebar.untitledChat")}
            </div>
            
            {/* DELETE ICON - HOVER ONLY */}
            <button
              className="delete-chat-btn"
              onClick={(e) => {
                e.stopPropagation(); // Prevent chat selection
                handleDeleteChat(chat.id);
              }}
              title={t("chat.deleteChat")}
            >
              🗑️
            </button>
          </div>
        ))}
      </div>

      <div className="sidebar-bottom">
        <button
          className="btn-secondary full"
          style={{ marginBottom: "12px" }}
          onClick={() => navigate("/")}
        >
          {t("sidebar.exitChat")}
        </button>

        <div className="user-info">
          <div className="avatar">{user?.email?.[0]?.toUpperCase()}</div>
          <div>
            <div className="username">{user?.email}</div>
            <div
              className="settings"
              style={{ cursor: "pointer" }}
              onClick={() => navigate("/settings")}
            >
              ⚙ {t("sidebar.settings")}
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}