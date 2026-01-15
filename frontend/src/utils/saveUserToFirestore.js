import { doc, getDoc, setDoc, serverTimestamp } from "firebase/firestore";
import { db } from "../auth/firebase";

/**
 * Saves user only if not already present
 */
export const saveUserToFirestore = async (user) => {
  if (!user || !user.uid) return;

  const userRef = doc(db, "users", user.uid);
  const userSnap = await getDoc(userRef);

  // ✅ If user already exists → DO NOTHING
  if (userSnap.exists()) {
    return;
  }

  // ✅ Create new user document
  await setDoc(userRef, {
    uid: user.uid,
    email: user.email,
    name: user.displayName || user.email.split("@")[0],
    provider: user.providerData[0]?.providerId || "password",
    createdAt: serverTimestamp(),
  });
};
