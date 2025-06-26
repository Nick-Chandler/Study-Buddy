import { useEffect, useState } from 'react';
import Styles from '../styles/NewWorkspace.module.css'
import FileView from './FileView';
import UploadPrompt from '../components/UploadPrompt';
import { useAuth } from './AuthProvider';
import { useTheme } from './ThemeProvider';
import { useLayout } from './LayoutContext';

export default function Workspace() {
  const { uploadFile, document, setDocument, documentName, setDocumentName } = useLayout()
  const { user } = useAuth() // Get the user from AuthProvider
  const { theme } = useTheme()
  const [fileUrl, setFileUrl] = useState(null); // State to hold the file URL


  useEffect(() => {
    console.log("Workspace - Loaded")
    if (user && user.lastAccessedFile) {
      retrieveFile(user.lastAccessedFile);
    }
  },[]);

  useEffect(() => {
    uploadFile();
  }, [document]);

  function userFileChange(e) {
    const selectedFile = e.target.files[0]; // Get the first selected file
    return handleFileChange(selectedFile); // Call the function to display the file 

  };

  function handleFileChange(selectedFile) {
    if (!selectedFile) {
    console.log('No file selected')
    return
    }
    if (selectedFile && selectedFile.type === 'application/pdf') { // Ensure it's a PDF
      const fileUrl = URL.createObjectURL(selectedFile); // Create a URL for the file
      setFileUrl(fileUrl); // Update the state with the file URL
      setDocument(selectedFile)
      setDocumentName(selectedFile.name) // Set the document name
      console.log('File selected:', selectedFile);
      console.log('File URL:', fileUrl);
      console.log('Document Name:', selectedFile.name);
    } else {
      alert('Please upload a valid PDF file.'); // Show an alert if the file is not a PDF
      return
    }
  }

  async function retrieveFile(fileId) {
    try {
      const response = await fetch(`http://localhost:8000/api/userfile/${fileId}/download/`);
      if (response.ok) {
        const blob = await response.blob();
        const fileUrl = URL.createObjectURL(blob);
        setFileUrl(fileUrl); // Update the state with the file URL
      } else {
        console.error("Failed to fetch file:", await response.json());
      }
    } catch (error) {
      console.error("Error fetching file:", error);
    }
  }

  return (
    <div className={Styles.workspace}>
      
      <div className={`${Styles.content}`}>
        {fileUrl ? <FileView file={fileUrl} /> : <UploadPrompt userFileChange={userFileChange} />}
      </div>
    </div>
  );
}
