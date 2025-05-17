import Styles from '../styles/Navbar.module.css'

export default function Navbar() {
  return (
    <nav className={Styles.navbar}>
      <div className={Styles.container}>
        <div className={Styles.placeholder}></div>
        <h1 className={Styles.title}>Study Buddy</h1>
        <button className={Styles.loginbtn}>
          <a>Login</a>
        </button>
      </div>
    </nav>
  )
}
