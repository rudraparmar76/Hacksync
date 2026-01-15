import { useEffect, useState, useRef } from "react";
import { collection, onSnapshot, orderBy, query } from "firebase/firestore";
import { db } from "../../auth/firebase";
import { sendMessage } from "../../utils/chatService";
import { sendToOpenAI } from "../../utils/openAiService";
import { useTranslation } from "react-i18next";
import { analyzePrompt } from "../../utils/backendService";
import ThinkingProcess from "./ThinkingProcess";
import DebateAnalysis from "./DebateAnalysis";
import LoadingIndicator from "./LoadingIndicator";

export default function ChatWindow({ chatId, onCreateChat }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [uploadedFileUrls, setUploadedFileUrls] = useState([]);
  const [hasStarted, setHasStarted] = useState(false);
  const [pendingMessage, setPendingMessage] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const [isUploading, setIsUploading] = useState(false); 
  const fileInputRef = useRef(null);
  const recognitionRef = useRef(null);
  const { t } = useTranslation();

  useEffect(() => {
    if (!chatId) return;

    const q = query(
      collection(db, `chats/${chatId}/messages`),
      orderBy("createdAt")
    );

    const unsub = onSnapshot(q, snap => {
      setMessages(snap.docs.map(doc => doc.data()));
    });

    return () => unsub();
  }, [chatId]);

  // Send pending message after chat is created
  useEffect(() => {
    if (chatId && pendingMessage) {
      const sendPending = async () => {
        try {
          // User message
          await sendMessage(chatId, "user", pendingMessage.text, pendingMessage.files);

          // AI response
          setTimeout(async () => {
            await sendMessage(chatId, "ai", t("chat.aiDefaultResponse"));
            setSending(false);
            setPendingMessage(null);
          }, 500);
        } catch (error) {
          console.error("Failed to send pending message:", error);
          setSending(false);
          setPendingMessage(null);
        }
      };
      sendPending();
    }
  }, [chatId, pendingMessage, t]);
  const handleSend = async () => {
    try {
      if (!input.trim() || sending || isUploading) return; 

      const text = input;
      const files = uploadedFiles.map((file, index) => ({
        name: file.name,
        type: file.type,
        size: file.size,
        url: uploadedFileUrls[index] || null
      }));

      setInput("");
      setSending(true);
      setHasStarted(true);

      let currentChatId = chatId;
      if (!currentChatId && onCreateChat) {
        currentChatId = await onCreateChat();
      }

      if (!currentChatId) {
        console.error("Failed to create or get chat ID");
        setSending(false);
        return;
      }

      try {
        await sendMessage(currentChatId, "user", text, files);
        setUploadedFiles([]);
        setUploadedFileUrls([]);

        // Call Backend API
        const result = await analyzePrompt(text);
        
        // Helper to format the structured report
        const formatReport = (report) => {
          if (!report) return "Analysis complete.";
          if (typeof report === 'string') return report;
          return report.executive_summary || "Analysis complete.";
        };

        const finalReport = formatReport(result.final_report);
        const traceData = result.trace || [];

        // Pass full result as the last argument
        await sendMessage(currentChatId, "ai", finalReport, [], traceData, result);
      } catch (err) {
        console.error("Backend Error:", err);
        await sendMessage(currentChatId, "ai", "Sorry, I encountered an error analyzing your request. " + err.message, []);
      } finally {
        setSending(false);
      }
    } catch (error) {
      console.error("Failed to send message:", error);
      setSending(false);
    }
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    if (e.currentTarget === e.target) {
      setIsDragging(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length === 0) return;

    setUploadedFiles(prev => [...prev, ...files]);
    setIsUploading(true);
    try {
      const formData = new FormData();
      files.forEach(file => formData.append('files', file));

      const response = await fetch(
        `${import.meta.env.VITE_UPLOAD_API_BASE_URL || 'http://localhost:5000'}/api/upload`,
        {
        method: 'POST',
        body: formData,
        }
      );

      const result = await response.json();
      if (result.success && result.files) {
        setUploadedFileUrls(prev => [...prev, ...result.files]);
      }
    } catch (error) {
      console.error('File upload failed:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const removeFile = (index) => {
    setUploadedFiles(uploadedFiles.filter((_, i) => i !== index));
    setUploadedFileUrls(uploadedFileUrls.filter((_, i) => i !== index));
  };

  const handleFileInputChange = async (e) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;

    setUploadedFiles(prev => [...prev, ...files]);
    setIsUploading(true);
    try {
      const formData = new FormData();
      files.forEach(file => formData.append('files', file));

      const response = await fetch(
        `${import.meta.env.VITE_UPLOAD_API_BASE_URL || 'http://localhost:5000'}/api/upload`,
        {
        method: 'POST',
        body: formData,
        }
      );

      const result = await response.json();
      if (result.success && result.files) {
        setUploadedFileUrls(prev => [...prev, ...result.files]);
      }
    } catch (error) {
      console.error('File upload failed:', error);
    } finally {
      setIsUploading(false);
    }

    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(prev => prev + (prev ? ' ' : '') + transcript);
        setIsListening(false);
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  }, []);

  const handleVoiceInput = () => {
    if (!recognitionRef.current) {
      alert(t("chat.speechNotSupported"));
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (error) {
        console.error('Failed to start speech recognition:', error);
      }
    }
  };

  const hasMessages = messages.length > 0;

  return (
    <div 
      className={`chat-window ${hasMessages ? 'with-messages' : 'empty'} centered ${isDragging ? 'dragging' : ''}`}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <button
        className="mobile-menu-btn"
        onClick={() =>
          document.querySelector(".chat-sidebar")?.classList.toggle("open")
        }
      >
        ☰
      </button>

      {hasMessages && uploadedFiles.length > 0 && (
        <div className="document-banner">
          <div className="document-banner-content">
            <div className="document-icon">📄</div>
            <div className="document-info">
              <div className="document-title">{uploadedFiles[0].name}</div>
              <div className="document-meta">
                {uploadedFiles.length > 1 && t(uploadedFiles.length - 1 > 1 ? "chat.moreFilesPlural" : "chat.moreFiles", { count: uploadedFiles.length - 1 })}
              </div>
            </div>
            <button className="document-close" onClick={() => setUploadedFiles([])}>×</button>
          </div>
        </div>
      )}

      {hasMessages && (
        <div className="chat-messages">
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              <div className="message-bubble">
                <div className="message-text">
                  {msg.thinking && msg.thinking.length > 0 && (
                    <ThinkingProcess steps={msg.thinking} />
                  )}
                  {/* If we have rich analysis data, render that instead of plain text */
                    msg.analysisData ? (
                      <DebateAnalysis analysisData={msg.analysisData} />
                    ) : (
                      msg.text
                  )}
                </div>
                {msg.files && msg.files.length > 0 && (
                  <div className="message-files">
                    {msg.files.map((file, idx) => (
                      <div key={idx} className="message-file-chip">
                        📄 {file.name}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          {sending && <LoadingIndicator />}
        </div>
      )}

      <div className="centered-prompt">
        {!hasMessages && <h1 className="prompt-title">{t("chat.welcome")}</h1>}
        
        <div className="centered-input-wrapper">
          <button 
            className="input-add-btn" 
            onClick={handleUploadClick}
            title={t("chat.attachFiles")}
          >
            +
          </button>
          <input
            type="file"
            multiple
            accept=".txt,.pdf,.doc,.docx,.png,.jpg,.jpeg,.gif"
            onChange={handleFileInputChange}
            style={{ display: 'none' }}
            ref={fileInputRef}
          />
          <input
            className="centered-input"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder={t("chat.inputPlaceholder")}
            onKeyDown={e => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />
          <button 
            className={`input-mic-btn ${isListening ? 'listening' : ''}`}
            onClick={handleVoiceInput}
            title={isListening ? t("chat.stopRecording") : t("chat.voiceInput")}
          >
            🎤
          </button>
          <button 
            className="input-send-btn" 
            onClick={handleSend} 
            disabled={isUploading} 
            title={isUploading ? t("chat.uploadWait") : t("chat.send")}
          >
            ⚡
          </button>
        </div>

        {!hasMessages && uploadedFiles.length > 0 && (
          <div className="centered-files">
            {uploadedFiles.map((file, index) => (
              <div key={index} className="file-chip-centered">
                <span>📄 {file.name}</span>
                <button onClick={() => removeFile(index)}>×</button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}