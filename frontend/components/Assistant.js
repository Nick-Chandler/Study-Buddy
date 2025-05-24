import Styles from '../styles/Assistant.module.css'
import { useState, useEffect, act, use } from 'react'
import { useAuth } from './AuthProvider'
import AssistantInput from './AssistantInput'



export default function Assistant() {
  const { user, conversations, activeThread, activeMessages, setActiveThread, setActiveMessages } = useAuth()
  console.log("Assistant Rendered");
  useEffect(() => {
    console.log("Assistant - Loaded")
    console.log("Assistant - Active Messages: " ,activeMessages)
    console.log("Assistant - User: ",user || 'No User Found')
    console.log("Assistant - User ID: ", user?.user?.id || "No User ID");
    console.log("Assistant - Active Thread: ", activeThread);
  }, []);

  useEffect(() => {
    getUserThreadMessages(user?.user?.id || [], activeThread)
    console.log("Assistant(user useEffect) - Active Messages: ", activeMessages)
  }, [user]);
 
  useEffect(() => {
    console.log("Active Messages Changed: ", activeMessages)
    displayMessages();
  }, [activeMessages]);

  async function getUserThreadMessages(userId, activeThread) {
    console.log("Get Thread Messages - Fetching User Thread Messages");
    console.log("Get Thread Messages - User ID: ", userId);
    console.log("Get Thread Messages - Active Thread: ", activeThread);
    console.log("Get Thread Messages - Type of User ID: ", typeof userId);
    console.log("Get Thread Messages - Type of Thread ID: ", typeof activeThread);
    if(!Number.isInteger(userId) || !Number.isInteger(activeThread)) {
      console.log("Get Thread Messages - No User ID or Active Thread Found");
      return;
    }
    console.log("Get Thread Messages - Creating URL for User Thread Messages");
    const url = `http://localhost:8000/get_user_thread_messages/${userId}/${activeThread}`;
    console.log("Get Thread Messages - Messages URL: ", url);
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      console.log("Get Thread Messages - No Messages Found for User: ", userId, " Thread: ", activeThread);
    }
    const msgs = await response.json();
    console.log("Get Thread Messages - Got Response: ", msgs)
    setActiveMessages(msgs);
    return msgs;
  }

  function displayMessages() {
    const ulElement = document.querySelector(`.${Styles.messages}`);
    ulElement.innerHTML = ""; // Clear existing messages
    console.log(`Assistant - Active Messages: ${activeMessages}`)
    activeMessages.forEach((message) => {
      console.log("Assistant - Message: ", message);
      const li = document.createElement("li");
      const p = document.createElement("p");
      p.className = Styles[message.role]; // Apply dynamic class based on message role
      p.textContent = message.text; // Set the message content
      li.appendChild(p);
      ulElement.appendChild(li);
    });
  }

  useEffect(() => {
    if (activeThread === null || activeThread === undefined || activeThread === "") 
      return
    console.log("Assistant - Active Thread Changed: ", activeThread);
    console.log("Assistant - User ID: ", user?.user?.id || "No User ID");
    getUserThreadMessages(user?.user?.id || [], activeThread)
    }, [activeThread]);
  
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

