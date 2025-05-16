import React, { useState } from 'react';
import styles from '../styles/workspace.module.css';
import FileView from './FileView';

export default function Workspace() {
  const [fileUrl, setFileUrl] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]; // Get the first selected file
    if (selectedFile && selectedFile.type === 'application/pdf') { // Ensure it's a PDF
      const fileUrl = URL.createObjectURL(selectedFile); // Create a URL for the file
      setFileUrl(fileUrl); // Update the state with the file URL
    } else {
      alert('Please upload a valid PDF file.'); // Show an alert if the file is not a PDF
    }
  };

  return (
    <section className={styles.workspace}>
      <h1>Workspace</h1>
      <label className={styles.uploadbtn}>
        Upload
        <input
          type="file"
          accept="application/pdf" // Restrict file selection to PDFs
          style={{ display: 'none' }} // Hide the default file input
          onChange={handleFileChange} // Handle file selection
        />
      </label>
      <div className={styles.content}>
        <FileView file={fileUrl} /> {/* Pass the file URL as a prop */}
      </div>
    </section>
  );
}
