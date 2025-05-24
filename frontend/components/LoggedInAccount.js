import React from 'react'
import { useAuth } from './AuthProvider'
import Styles from '../styles/Navbar.module.css'


export default function LoggedInAccount() {

  const { user, conversations, activeThread, userConversations, setActiveThread, login, logout, getUserConversations } = useAuth()
  
  function handleConversationChange(e) {
    console.log("Conversation Target Changed", e.target)
    console.log("Conversation Changed", e.target.value)
    setActiveThread(e.target.value)
  }


  return (
    <div className={Styles.account}>
      <select onChange={handleConversationChange} className={Styles.conversations} value={0}>
        {userConversations.map((conversation, i) => (
          <option onChange={handleConversationChange} key={i} value={i}>
            {conversation.name}
          </option>
        ))}
        <option value="new">New Conversation</option>
      </select>
      <button className={Styles.logout} onClick={logout}>Logout</button>
    </div>
  )
}
