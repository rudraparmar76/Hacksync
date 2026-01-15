import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { createChat } from "../utils/chatService";
import ChatSidebar from "../components/chat/ChatSidebar";
import ChatWindow from "../components/chat/ChatWindow";
import "../styles/chat.css";

export default function Chat() {
  const [activeChatId, setActiveChatId] = useState(null);
  const { user } = useAuth();

  const handleCreateChat = async () => {
    if (!user) return;
    try {
      const chatId = await createChat(user.uid);
      setActiveChatId(chatId);
      return chatId;
    } catch (err) {
      console.error("CHAT CREATION FAILED:", err);
    }
  };

  return (
    <div className="chat-layout">
      {/* LEFT 30% */}
      <ChatSidebar
        activeChatId={activeChatId}
        setActiveChatId={setActiveChatId}
      />

      {/* RIGHT 70% */}
      <ChatWindow 
        chatId={activeChatId} 
        onCreateChat={handleCreateChat}
      />
    </div>
  );
}
