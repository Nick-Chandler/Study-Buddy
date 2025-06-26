import React from 'react'
import { useState } from 'react';
import Styles from '../styles/NewWorkspace.module.css'
import { useAuth } from './AuthProvider';

export default function uploadPrompt({userFileChange}) {


  return (
    <div className={Styles.uploadPrompt}>
      <h1 className={Styles.uploadPromptHeader}>Upload a PDF to get started</h1>
      <p className={Styles.uploadPromptText}>Click the button below to upload your PDF file.</p>
      <label className={Styles.uploadBtn}>
        Browse Files
        <input
          type="file"
          accept="application/pdf" // Restrict file selection to PDFs
          style={{ display: 'none' }} // Hide the default file input
          onChange={userFileChange} // Handle file selection
        />
      </label>
      <p className={Styles.uploadPromptText}>Once uploaded, you can interact with the content of the PDF.</p>
    </div>
  )
}
