import React from "react";
import Styles from '../styles/Navbar.module.css'
import { useAuth } from './AuthProvider'

export default function ConversationSelect() {

  const {activeThread, userConversations, setActiveThread} = useAuth()

  function handleConversationChange(e) {
    console.log("Conversation Changed", e.target.value)
    setActiveThread(parseInt(e.target.value))
  }


  return (
    <select
      onChange={handleConversationChange}
      className={Styles.conversations}
      value={activeThread}
    >
      {userConversations.map((conversation, i) => (
        <option onChange={handleConversationChange} key={i} value={i}>
          {conversation.name}
        </option>
      ))}
      <option value="new">New Conversation</option>
    </select>
  );
}
