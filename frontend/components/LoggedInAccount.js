import React from 'react'
import { useAuth } from './AuthProvider'
import Styles from '../styles/Navbar.module.css'
import ConversationSelect from './ConversationSelect'


export default function LoggedInAccount() {

  const { user, conversations, activeThread, userConversations, setActiveThread, login, logout, getUserConversations } = useAuth()
  

  return (
    <div className={Styles.account}>
      <ConversationSelect></ConversationSelect>
      <button className={Styles.logout} onClick={logout}>Logout</button>
    </div>
  )
}
