import Styles from '../styles/Workspace.module.css'
import { useTheme } from './ThemeProvider'

export default function FileView({ file }) {

  const { theme } = useTheme()

  return (
    <iframe className={`${theme === 'light' ? Styles.lightTheme : null}`}
      src={file}
      width="100%"
      height="100%"
      title="File Viewer"
    />
  )
}
