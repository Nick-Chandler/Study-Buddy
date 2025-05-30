import React from 'react'
import { useState } from 'react';

export default function test() {
  const [fileURL, setFileURL] = useState(null);

  function handleFileChange(e) 
  {
    const file = e.target.files[0]; // Get the first selected file
    const fileUrl = URL.createObjectURL(file)
    setFileURL(fileUrl)
  }

  return (
    <div style={{ height: '100vh', width: '100vw', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <input
          type="file"
          accept="application/pdf" // Restrict file selection to PDFs
          onChange={handleFileChange}
        />
        <iframe
          src={fileURL}
          width="50%"
          height="50%"
          title="File Viewer"
        />
    </div>
  )
}
