import React from 'react'
import Assistant from './Assistant';
import Customizations from './Customizations';
import Workspace from './Workspace';
import Styles from '../styles/CSLayout.module.css';

export default function CSLayout() {
  return (
    <main className={Styles.layout}>
      <Customizations />
      <Workspace />
      <Assistant />
    </main>
  )
}
