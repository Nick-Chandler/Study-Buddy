import { useState } from 'react';
import Styles from '../styles/NewWorkspace.module.css'
import FileView from './FileView';
import UploadPrompt from '../components/UploadPrompt';
import { useAuth } from './AuthProvider';
import { useTheme } from './ThemeProvider';

export default function Workspace() {
  const [fileUrl, setFileUrl] = useState(null);
  const { user } = useAuth(); // Get the user from AuthProvider
  const { theme } = useTheme()


  function handleFileChange(e) {
    const selectedFile = e.target.files[0]; // Get the first selected file
    if (!selectedFile) {
    console.log('No file selected')
    return
    }
    if (selectedFile && selectedFile.type === 'application/pdf') { // Ensure it's a PDF
      const fileUrl = URL.createObjectURL(selectedFile); // Create a URL for the file
      setFileUrl(fileUrl); // Update the state with the file URL
      const formData = new FormData()
      formData.append('file', selectedFile)
      formData.append('filename', selectedFile.name)
      uploadFile(formData)
    } else {
      alert('Please upload a valid PDF file.'); // Show an alert if the file is not a PDF
      return
    }
      
    };

    async function uploadFile(formData) {
    try {
      const response = await fetch(`http://localhost:8000/upload_file/${user?.user?.id}`, {
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

  return (
    <div className={Styles.workspace}>
      
      <div className={`${Styles.content}`}>
        {fileUrl ? <FileView file={fileUrl} /> : <UploadPrompt handleFileChange={handleFileChange} />}
      </div>
    </div>
  );
}
