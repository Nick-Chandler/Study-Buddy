import React from 'react'
import { useAuth } from './AuthProvider'
import Styles from '../styles/Navbar.module.css'


export default function LoggedInAccount() {
  const { user, login, logout } = useAuth()
  return (
    <div className={Styles.account}>
      <button className={Styles.logout} onClick={logout}>Logout</button>
    </div>
  )
}
