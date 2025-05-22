import Styles from '../styles/Assistant.module.css'
import { useState, useEffect, act } from 'react'
import { useAuth } from './AuthProvider'
import AssistantInput from './AssistantInput'



export default function Assistant() {
  const { user, conversations, activeConversation, setActiveConversation, activeMessages } = useAuth()
  console.log(activeMessages)

  // Function to fetch the response from the API

  useEffect(() => {
    console.log("Assistant - Active Conversation on Load",activeConversation)
    console.log("Assistant - All Conversations:",conversations)
    console.log("Assistant - Active Conversation:",activeConversation)
    console.log("Assistant - Active Messages:", activeMessages)
  }, []);

  useEffect(() => {
    console.log("Assistant - Messages on Change: ", activeMessages)
    displayMessages()
  },[activeMessages])

  function displayMessages() {
    const ulElement = document.querySelector(`.${Styles.messages}`);
    ulElement.innerHTML = ""; // Clear existing messages
    console.log(`Assistant - Active Messages: ${activeMessages}`)
    activeMessages.forEach((message) => {
      const li = document.createElement("li");
      const p = document.createElement("p");
      p.className = Styles[message.role]; // Apply dynamic class based on message role
      p.textContent = message.content; // Set the message content
      li.appendChild(p);
      ulElement.appendChild(li);
    });
  }
  

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

