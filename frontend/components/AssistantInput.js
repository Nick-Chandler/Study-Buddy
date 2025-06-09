import React from "react";
import Styles from '../styles/NewAssistant.module.css'
import FileView from './FileView'
import FileThumbnail from "./FileThumbnail";
import { useState, useRef, useEffect } from 'react'
import { useAuth } from './AuthProvider'
import { useLayout } from "./LayoutContext";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowUpFromBracket } from '@fortawesome/free-solid-svg-icons'

  

export default function AssistantInput({ scrollToBottom }) {

  const [input, setInput] = useState('')
  const [fileThumbnails, setFileThumbnails] = useState([]);
  const [fileUploads, setFileUploads] = useState([]);
  const {user, activeThread, activeMessages, setActiveMessages, addMessage} = useAuth()
  const { referenceImg, setReferenceImg, getAiResponse} = useLayout();

// Function to send a message to the assistant
  async function talkToAssistant(e) {
    console.log("AssistantInput - talkToAssistant called with input: ", input);
    if (input.trim() === '') {
      console.log("AssistantInput - Empty input, returning early.");
      return; // Prevent sending empty messages
    }
    e.preventDefault() // Prevent default form submission
    // call api to get response
    let userId = user?.user?.id || ""
    console.log("AssistantInput - User ID: ", userId)
    console.log("AssistantInput - Active Thread: ", activeThread)
    if (!userId) return
    // Add Human Message to active Messages
    let temp_input = input
    addMessage(temp_input, "user")
    scrollToBottom()
    setInput('') // Clear input field
    console.log("Calling getAiResponse with User ID: ", userId, " and Active Thread: ", activeThread)
    console.log("Calling getAiResponse with Input: ", temp_input)
    let response = await getAiResponse(userId, temp_input, fileUploads)
    // Add Assistant Message to active Messages
    addMessage(response, "assistant") // Add Assistant Message to active Messages
  }

  function handleFileUpload(e) {
    console.log("File Added: ", e);
    const file = e.target.files[0];
    if (file) {
      setFileUploads(prevUploads => [...prevUploads, file]);
      const fileUrl = URL.createObjectURL(file);
      setFileThumbnails(prevUploads => [...prevUploads, fileUrl]);
    }
    e.target.value = null;
  }

  function deleteFile(index) {
    console.log("Deleting file at index: ", index);
    URL.revokeObjectURL(fileThumbnails[index]); // Free up memory
    setFileUploads(prevUploads => prevUploads.filter((_, i) => i !== index));
    setFileThumbnails(prevUploads => prevUploads.filter((_, i) => i !== index));
  }

  useEffect(() => {
    console.log("File Upload Changed: ", fileThumbnails);
  },[fileThumbnails])



  return (
    <form id="input" className={Styles.input} onSubmit={talkToAssistant} autoComplete="off">
      {fileThumbnails.length > 0 && <ul className={Styles.fileUploads}>{fileThumbnails.map((file, index) => (
        <FileThumbnail
          key={index}
          src={file}
          alt={`Uploaded File ${index + 1}`}
          deleteFile={() => deleteFile(index)}
          className={Styles.fileThumbnail}
        />
      ))}</ul>}
      <div className={Styles.inputContainer}>
        <input
          className={Styles.inputField}
          type="text"
          placeholder="Need help? Ask me anything..."
          value={input}
          name="assistantInput"
          onChange={(e) => setInput(e.target.value)} // Update state on input change
        />
        <input type="file" id="fileUpload" name="fileUpload" style={{ display: 'none' }}  onChange={handleFileUpload}/>
        <label htmlFor="fileUpload" className={Styles.fileUploadLabel}>
          <FontAwesomeIcon icon={faArrowUpFromBracket} />
        </label>
      </div>
    </form>
  );
}
