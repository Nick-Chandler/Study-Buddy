import Styles from '../styles/Navbar.module.css'
import Link from 'next/link'
import { useAuth } from './AuthProvider'
import LoggedInAccount from './LoggedInAccount'
import { useEffect } from 'react'
import { useTheme } from './ThemeProvider'

export default function Navbar() {

  const { user, login, logout, loggedIn, activeMessages, activeThread, threads } = useAuth()
  const { theme } = useTheme()
  console.log("Navbar - User: ", user)
  console.log("Navbar - Active Messages: ", activeMessages)


  useEffect(() => {
    if (!loggedIn) {
      console.log("Navbar - No user found")
    }
    console.log("Navbar - User: ", user)
    console.log("Navbar - User.username: ", user?.username)
    console.log("Logged In: ", loggedIn)
  }, []);

  function printStates() {
    console.log("Print States - User: ", user);
    console.log("Print States - Logged In: ", loggedIn);
    console.log("Print States - Threads: ", threads);
    console.log("Print States - Active Thread: ", activeThread);
    console.log("Print States - Active Messages: ", activeMessages);
  }


  return (
    <nav className={`${Styles.navbar} ${theme === 'light' ? Styles.lightTheme : null}`}>
      <div className={Styles.container}>
        <div className={Styles.placeholder}>
          {user?.username ?? user?.user?.username ?? "Guest"}
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
