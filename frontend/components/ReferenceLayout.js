import FileView from './FileView';
import { useLayout } from './LayoutContext';
import ReferencePrompt from './ReferencePrompt';
import Assistant from './Assistant';
import Workspace from './Workspace';
import Styles from '../styles/ReferenceLayout.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons'

export default function ReferenceLayout() {
  
  const { referenceImg ,setReferenceImg } = useLayout();


  return (
    <main className={Styles.layout}>
      <section className={Styles.left}>
        <h1 className={Styles.workspaceHeader}>Workspace</h1>
        <div className={Styles.workspaceContainer}>
          <Workspace />
        </div>
      </section>
      <section className={Styles.right}>
        <div className={Styles.referenceContainer}>
          <div className={Styles.referenceHeader}>
            <h2 className={Styles.referenceTitle}>Reference</h2>
            <button className={Styles.clearReferenceButton}
            onClick={() => setReferenceImg(null)}>
            <FontAwesomeIcon icon={faTimes} />
            </button>
          </div>
          
          {referenceImg === null
            ? <ReferencePrompt />
            : <FileView file={referenceImg} />
          }
        </div>
        <div className={Styles.assistantContainer}>
          <Assistant />
        </div>
      </section>
    </main>
  )
}
