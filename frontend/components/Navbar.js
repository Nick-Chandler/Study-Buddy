import Styles from '../styles/Navbar.module.css'
import Link from 'next/link'
import { useAuth } from './AuthProvider'
import LoggedInAccount from './LoggedInAccount'
import { useEffect } from 'react'
import { useTheme } from './ThemeProvider'

export default function Navbar() {

  const { user, login, logout, activeMessages } = useAuth()
  const { theme } = useTheme()
  let loggedIn = (user !== null && user !== undefined && user.user !== null && user.user !== undefined)
  console.log("Navbar - User: ", user)
  console.log("Navbar - Active Messages: ", activeMessages)


  useEffect(() => {
    console.log("Navbar - User: ", user)
  }, []);


  return (
    <nav className={`${Styles.navbar} ${theme === 'light' ? Styles.lightTheme : null}`}>
      <div className={Styles.container}>
        <div className={Styles.placeholder}>
          {user?.user?.username || 'Guest'}
        </div>
        <h1 className={Styles.title}>Study Buddy</h1>
          {loggedIn ? (<LoggedInAccount />) :
            (<Link className={Styles.login} href="/login">
              <button>Login</button>
            </Link>)}
      </div>
    </nav>
  )
}
