import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getFirestore } from "firebase/firestore";


const firebaseConfig = {
  apiKey: "AIzaSyDZvm315bHroBRpUaxQBLRroDSIxt7lqgg",
  authDomain: "ather-276b9.firebaseapp.com",
  projectId: "ather-276b9",
  storageBucket: "ather-276b9.firebasestorage.app",
  messagingSenderId: "131761041994",
  appId: "1:131761041994:web:b5c0f1ed28ad0f442e2cb3",
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
export const db = getFirestore(app);
