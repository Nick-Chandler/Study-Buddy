import React from "react";
import Styles from '../styles/Assistant.module.css'
import { useState, useRef } from 'react'
import { useAuth } from './AuthProvider'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowUpFromBracket } from '@fortawesome/free-solid-svg-icons'

  

export default function AssistantInput(props) {

  const [input, setInput] = useState('')
  // const { user, conversations, activeConversation, setActiveConversation, activeMessages, addMessage } = useAuth()
  // const fileInputRef = useRef(null)

  // async function fetchResponse(userInput) {
  //   try {
  //     const response = await fetch(`http://127.0.0.1:8000/assistant/${activeConversation}`, {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({ query: userInput }),
  //     });

  //     if (response.ok) {
  //       const data = await response.json();
  //       let msg = { content: data.message, type: 'assistant' }
  //       addMessage(msg) // Add assistant's response to the messages
  //     } else {
  //       console.error('Error:', response.statusText);
  //     }
  //   } catch (error) {
  //     console.error('Error:', error);
  //   }
  // };

  // Handle form submission
  async function handleSubmit(e){
    e.preventDefault();
    if (input.trim() === '') return;
    let msg = { content: input, type: 'user' }
    addMessage(msg) // Add user's message to the messages
    fetchResponse(input); // Call the function to fetch the response from the API
    setInput('');
  };

  return (
    <form id="input" className={Styles.input} onSubmit={handleSubmit}>
      <input
        className={Styles.inputField}
        type="text"
        placeholder="Need help? Ask me anything..."
        value={input}
        onChange={(e) => setInput(e.target.value)} // Update state on input change
      />
      <div className={Styles.inputButtons}>
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
      </div>
    </form>
  );
}
