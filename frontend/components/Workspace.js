import { useState } from 'react';
import Styles from '../styles/NewWorkspace.module.css'
import FileView from './FileView';
import UploadPrompt from '../components/UploadPrompt';
import { useAuth } from './AuthProvider';
import { useTheme } from './ThemeProvider';
import { useLayout } from './LayoutContext';

export default function Workspace() {
  const { uploadFile, setDocument } = useLayout()
  const { user } = useAuth() // Get the user from AuthProvider
  const { theme } = useTheme()
  const [fileUrl, setFileUrl] = useState(null); // State to hold the file URL

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
      formData.append('doc', selectedFile)
      formData.append('docname', selectedFile.name)
      setDocument(selectedFile)
      uploadFile(formData)
    } else {
      alert('Please upload a valid PDF file.'); // Show an alert if the file is not a PDF
      return
    }

  };

  return (
    <div className={Styles.workspace}>
      
      <div className={`${Styles.content}`}>
        {fileUrl ? <FileView file={fileUrl} /> : <UploadPrompt handleFileChange={handleFileChange} />}
      </div>
    </div>
  );
}
