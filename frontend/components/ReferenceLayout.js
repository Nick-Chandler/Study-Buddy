import React from 'react'
import Assistant from './Assistant';
import Customizations from './Customizations';
import Workspace from './Workspace';
import Styles from '../styles/ReferenceLayout.module.css';

export default function ReferenceLayout() {
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
        <h1 className={Styles.rightHeader}>Reference</h1>
        </div>
        <div className={Styles.assistantContainer}>
          <Assistant />
        </div>
      </section>
    </main>
  )
}
