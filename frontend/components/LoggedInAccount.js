import React from 'react'
import { useAuth } from './AuthProvider'
import Styles from '../styles/Navbar.module.css'


export default function LoggedInAccount() {

  const { user, conversations, activeConversation, userConversations, setActiveConversation, login, logout, getUserConversations } = useAuth()
  
  function handleConversationChange(e) {
    console.log("Conversation Target Changed", e.target)
    console.log("Conversation Changed", e.target.value)
    setActiveConversation(e.target.value)
  }


  return (
    <div className={Styles.account}>
      <select onChange={handleConversationChange} className={Styles.conversations}>
        {userConversations.map((conversation, i) => (
          <option onChange={handleConversationChange} key={conversation.conversation_id} value={i}>
            {conversation.name}
          </option>
        ))}
        <option value="new">New Conversation</option>
      </select>
      <button className={Styles.logout} onClick={logout}>Logout</button>
    </div>
  )
}
