import Styles from '../styles/Customizations.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSun } from '@fortawesome/free-solid-svg-icons'
import { useTheme } from './ThemeProvider';
import LayoutButton from './LayoutButton';
import { useLayout } from './LayoutContext';


export default function Customizations() {
  const { theme, setTheme } = useTheme();
  const { currentLayout } = useLayout();

  return (
    <section className={`${Styles.customizations} ${theme==='light' ? Styles.lightTheme : null}`}>
      <h1>Customizations</h1>
      <button className={`${Styles.themeToggle} ${Styles.customizationBtn}`} onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        <FontAwesomeIcon icon={faSun} />
      </button>
      <LayoutButton  />
      <p>Current Layout: {currentLayout}</p>
    </section>
  )
}
