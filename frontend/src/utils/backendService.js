const API_BASE_URL =
  import.meta.env.VITE_BACKEND_BASE_URL || "http://localhost:7860";

/**
 * Analyzes a text prompt using the backend API.
 * @param {string} prompt - The user's prompt.
 * @returns {Promise<Object>} The structured response from the API.
 */
export const analyzePrompt = async (prompt) => {
  try {
    const formData = new FormData();
    formData.append("prompt", prompt);

    const response = await fetch(`${API_BASE_URL}/analyze/prompt`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Backend Analysis Error:", error);
    throw error;
  }
};

/**
 * Analyzes an uploaded document.
 * @param {File} file - The file to upload.
 * @returns {Promise<Object>} The structured response from the API.
 */
export const analyzeDocument = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/analyze/document`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Backend Document Analysis Error:", error);
    throw error;
  }
};
