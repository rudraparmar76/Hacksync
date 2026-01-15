const GEMINI_API_KEY = import.meta.env.VITE_GEMINI_API_KEY;

export const sendToGemini = async (text) => {
  try {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${GEMINI_API_KEY}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [
            {
              role: "user",
              parts: [{ text }],
            },
          ],
        }),
      }
    );

    const data = await res.json();

    if (data.error) {
      throw new Error(data.error.message);
    }

    return data.candidates[0].content.parts[0].text;

  } catch (err) {
    console.error("Gemini Frontend Error:", err);
    return "AI response unavailable (frontend mode)";
  }
};
