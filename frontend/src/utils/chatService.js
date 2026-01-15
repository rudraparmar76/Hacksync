import {
  collection,
  addDoc,
  query,
  where,
  orderBy,
  getDocs,
  serverTimestamp,
  doc,
  updateDoc,
  deleteDoc,
  onSnapshot
} from "firebase/firestore";
import { db } from "../auth/firebase";

// Create new chat
export const createChat = async (userId, defaultTitle = "New Chat") => {
  const chatRef = await addDoc(collection(db, "chats"), {
    userId,
    title: defaultTitle,
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp()
  });
  return chatRef.id;
};

// Get user's chats (one-time)
export const getUserChats = async (userId) => {
  const q = query(
    collection(db, "chats"),
    where("userId", "==", userId),
    orderBy("updatedAt", "desc")
  );

  const snap = await getDocs(q);
  return snap.docs.map(doc => ({
    id: doc.id,
    ...doc.data()
  }));
};

// Listen to user's chats in real-time
export const listenToUserChats = (userId, callback) => {
  const q = query(
    collection(db, "chats"),
    where("userId", "==", userId),
    orderBy("updatedAt", "desc")
  );

  const unsub = onSnapshot(q, snap => {
    const data = snap.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
    callback(data);
  }, error => {
    console.error("Error listening to chats:", error);
  });

  return unsub;
};

// Send message
export const sendMessage = async (chatId, role, text, files = [], thinking = null, analysisData = null) => {
  console.log('sendMessage called with files:', files);

  const messageData = {
    role,
    text,
    files: files.length > 0 ? files : null,
    thinking: thinking || null,
    analysisData: analysisData || null,
    createdAt: serverTimestamp()
  };

  console.log('Message data to store:', messageData);

  await addDoc(collection(db, `chats/${chatId}/messages`), messageData);

  // Update parent chat document with latest message
  await updateDoc(doc(db, "chats", chatId), {
    lastMessage: text,
    lastMessageRole: role,
    updatedAt: serverTimestamp()
  });
};

// Delete chat and all messages
export const deleteChat = async (userId, chatId) => {
  // First, delete all messages in the subcollection
  const messagesQuery = query(collection(db, `chats/${chatId}/messages`));
  const messagesSnapshot = await getDocs(messagesQuery);

  const deletePromises = messagesSnapshot.docs.map(messageDoc =>
    deleteDoc(doc(db, `chats/${chatId}/messages`, messageDoc.id))
  );

  await Promise.all(deletePromises);

  // Then delete the chat document itself
  await deleteDoc(doc(db, "chats", chatId));
};
