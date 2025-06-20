import { createContext, useState, useContext, useEffect } from 'react';
import { useAuth } from './AuthProvider';
const LayoutContext = createContext();

export function LayoutProvider({ children }) {
  const [currentLayout, setCurrentLayout] = useState("reference");
  const [availableLayouts, setAvailableLayouts] = useState(["default", "reference", "cs"]);
  const [referenceImg, setReferenceImg] = useState(null);
  const [document, setDocument] = useState(null);
  const { user, activeThread } = useAuth();

    async function uploadFile(formData) {
    try {
      const url = `http://localhost:8000/upload_document/${user?.userId}`
      console.log("uploadFile - URL: ", url);
      console.log("uploadFile - FormData: ", formData);
      console.log("uploadFile - User", user)
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        alert('Failed to save file. Please try again.');
        return
    }
      else {
        const data = await response.json();
        console.log("File uploaded successfully: ", data);
        return true
      }
      
    }
    catch (error) {
      console.error("Error saving file - No Response from server:", error);
      alert('Failed to save file. Please try again.');
      return false
    }

  }

  async function getAiResponse(user_id, user_input, fileArray) {
    console.log("getAiResponse called with user_input: ", user_input);
    console.log("getAiResponse called with fileArray: ", fileArray);
    const url = `http://localhost:8000/assistant/${user_id}/${activeThread}`
    console.log("Context - Active Thread: ", activeThread)
    console.log("getAiResponse - Document: ", document)
    const formData = new FormData()
    formData.append('user_input', user_input)
    fileArray.forEach(file => formData.append('files', file))
    document && formData.append('document', document)
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()
    console.log("Assistant - Response: ", data)
    return data.message
}

  return (
    <LayoutContext.Provider 
        value={{ 
        currentLayout,
        setCurrentLayout,
        availableLayouts,
        referenceImg,
        setReferenceImg,
        document,
        setDocument,
        uploadFile,
        getAiResponse
      }}
    >
      {children}
    </LayoutContext.Provider>
  );
}

export function useLayout() {
  return useContext(LayoutContext);
}
