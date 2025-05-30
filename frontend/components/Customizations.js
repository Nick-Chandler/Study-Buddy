import Styles from '../styles/Customizations.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSun } from '@fortawesome/free-solid-svg-icons'
import { useTheme } from './ThemeProvider';

export default function Customizations() {
  const { theme, setTheme, changeTheme } = useTheme();

  return (
    <section className={`${Styles.customizations} ${theme==='light' ? Styles.lightTheme : null}`}>
      <h1>Customizations</h1>
      <button className={`${Styles.themeToggle} ${Styles.customizationBtn}`} onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        <FontAwesomeIcon icon={faSun} />
      </button>
    </section>
  )
}
