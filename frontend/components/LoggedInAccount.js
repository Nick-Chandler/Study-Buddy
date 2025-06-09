import React from 'react'
import { useAuth } from './AuthProvider'
import Styles from '../styles/Navbar.module.css'
import ThreadSelect from './ThreadSelect'
import NewThread from './NewThread'


export default function LoggedInAccount() {

  const { user, activeThread, threads, setActiveThread, login, logout, getThreads } = useAuth()
  

  return (
    <div className={Styles.account}>
      <NewThread></NewThread>
      <ThreadSelect></ThreadSelect>
      <button className={Styles.logout} onClick={logout}>Logout</button>
    </div>
  )
}
