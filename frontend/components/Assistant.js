import Styles from '../styles/Assistant.module.css'
import { useState, useEffect, act } from 'react'
import { useAuth } from './AuthProvider'
import AssistantInput from './AssistantInput'



export default function Assistant() {
  const { user, conversations, activeConversation, setActiveConversation, activeMessages } = useAuth()

  // Function to fetch the response from the API

  // Function to send a message to the assistant
  async function talkToAssistant() {
    // call api to get response
    

    // Add Human Message to active Messages
    // Wait for response
    // Add Assistant Message to active Messages
  }

  // function displayMessages() {
  //   const ulElement = document.querySelector(`.${Styles.messages}`);
  //   ulElement.innerHTML = ""; // Clear existing messages
  //   console.log(`Assistant - Active Messages: ${activeMessages}`)
  //   activeMessages.forEach((message) => {
  //     const li = document.createElement("li");
  //     const p = document.createElement("p");
  //     p.className = Styles[message.role]; // Apply dynamic class based on message role
  //     p.textContent = message.content; // Set the message content
  //     li.appendChild(p);
  //     ulElement.appendChild(li);
  //   });
  // }
  

  return (
    <section className={Styles.assistant}>
      <h1>AI Assistant</h1>
      <div className={Styles.content}>
        <ul className={Styles.messages}></ul>
      </div>
      <AssistantInput />
    </section>
  );
}

