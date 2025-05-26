import React from "react";
import Styles from '../styles/Assistant.module.css'
import { useState, useRef } from 'react'
import { useAuth } from './AuthProvider'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowUpFromBracket } from '@fortawesome/free-solid-svg-icons'

  

export default function AssistantInput(props) {

  const [input, setInput] = useState('')
  const {user, activeThread, activeMessages, setActiveMessages, addMessage, getAiResponse} = useAuth()

// Function to send a message to the assistant
  async function talkToAssistant(e) {
    e.preventDefault() // Prevent default form submission
    // call api to get response
    let userId = user?.user?.id || ""
    console.log("AssistantInput - User ID: ", userId)
    console.log("AssistantInput - Active Thread: ", activeThread)
    if (!userId) return
    // Add Human Message to active Messages
    let temp_input = input
    addMessage(temp_input, "human")
    setInput('') // Clear input field
    console.log("Calling getAiResponse with User ID: ", userId, " and Active Thread: ", activeThread)
    console.log("Calling getAiResponse with Input: ", temp_input)
    let response = await getAiResponse(userId, temp_input)
    // Add Assistant Message to active Messages
    addMessage(response, "ai") // Add Assistant Message to active Messages
  }



  return (
    <form id="input" className={Styles.input} onSubmit={talkToAssistant}>
      <input
        className={Styles.inputField}
        type="text"
        placeholder="Need help? Ask me anything..."
        value={input}
        name="assistantInput"
        onChange={(e) => setInput(e.target.value)} // Update state on input change
      />
      {/* <div className={Styles.inputButtons}>
        <input
          type="file"
          id="file"
          name="file"
          accept=".png"
          style={{ display: 'none' }} // Hide the default file input
        />
        <label htmlFor="file" className={Styles.fileButton}>
          <FontAwesomeIcon
            className={Styles.fileUpload}
            icon={faArrowUpFromBracket}
          />
        </label>
        <button type="submit">
          <FontAwesomeIcon
            className={Styles.upload}
            icon={faArrowUpFromBracket}
          />
        </button>
      </div> */}
    </form>
  );
}
