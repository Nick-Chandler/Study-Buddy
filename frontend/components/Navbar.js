import Styles from '../styles/Navbar.module.css'
import Link from 'next/link'
import { useAuth } from './AuthProvider'
import LoggedInAccount from './LoggedInAccount'
import { useEffect } from 'react'

export default function Navbar() {

  const { user, login, logout } = useAuth()
  let loggedIn = (user !== null)

  useEffect(() => {
  }, [user]);


  return (
    <nav className={Styles.navbar}>
      <div className={Styles.container}>
        <div className={Styles.placeholder}>{user?.user.username || 'Guest'}</div>
        <h1 className={Styles.title}>Study Buddy</h1>
          <div className={Styles.account}>
            {loggedIn ? (<LoggedInAccount />) :
              (<Link className={Styles.login} href="/login">
                <button>Login</button>
              </Link>)}
          </div>
      </div>
    </nav>
  )
}
