import Styles from '../styles/NewAssistant.module.css'
import { useState, useEffect, useRef } from 'react'
import { useAuth } from './AuthProvider'
import { useTheme } from './ThemeProvider'
import AssistantInput from './AssistantInput'
import RenameButton from './RenameButton'
import DeleteButton from './DeleteButton'

import MessageList from './MessageList'



export default function Assistant() {
  const { user, threads, activeThread, activeMessages, setActiveThread, setActiveMessages } = useAuth()
  const { theme } = useTheme()
  const assistantRef = useRef(null);
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
    assistantRef?.current && scrollToBottom(assistantRef);
  }, [activeMessages]);

  async function getUserThreadMessages(userId, activeThread) {
    console.log("Get Thread Messages - Fetching User Thread Messages");
    console.log("Get Thread Messages - User ID: ", userId);
    console.log("Get Thread Messages - Active Thread: ", activeThread);
    console.log("Get Thread Messages - Type of User ID: ", typeof userId);
    console.log("Get Thread Messages - Type of Thread ID: ", typeof activeThread);
    if(!Number.isInteger(userId) || !typeof activeThread === 'string' || !userId || !activeThread) {
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

  
  function scrollToBottom() {
    console.log("Ref: ",assistantRef.current)
    assistantRef.current.scrollTop = assistantRef.current.scrollHeight;
  }


  useEffect(() => {
    if (!activeThread) 
      return
    if (activeThread === "new")
      create_new_thread_for_user(user?.user?.id || "")

    console.log("Assistant - Active Thread Changed: ", activeThread);
    console.log("Assistant - Calling getUserThreadMessages");
    getUserThreadMessages(user?.user?.id || [], activeThread)
    }, [activeThread]);
  
  return (
    <div className={Styles.assistant}>
      <AssistantInput />
      <div className={Styles.content} ref={assistantRef} >
        <MessageList className={Styles.messages} messages={activeMessages} />
      </div>
    </div>
  );
}

