import React from 'react'
import { useAuth } from './AuthProvider'
import Styles from '../styles/Navbar.module.css'


export default function LoggedInAccount() {

  const { user, conversations, activeConversation, setActiveConversation, login, logout } = useAuth()
  
  function handleConversationChange(e) {
    console.log("Conversation changed: ", e.target.value)
    setActiveConversation(e.target.value)
  }


  return (
    <div className={Styles.account}>
      <select onChange={handleConversationChange} className={Styles.conversations}>
        {conversations.map((conversation) => (
          <option onChange={handleConversationChange} key={conversation.id} value={conversation.id}>
            {conversation.name}
          </option>
        ))}
        <option value="new">New Conversation</option>
      </select>
      <button className={Styles.logout} onClick={logout}>Logout</button>
    </div>
  )
}
