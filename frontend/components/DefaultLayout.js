import React from 'react'
import Assistant from './Assistant';
import Customizations from './Customizations';
import Workspace from './Workspace';
import Styles from '../styles/DefaultLayout.module.css';

export default function DefaultLayout() {  
  return (
    <main className={Styles.layout}>
      <Customizations />
      <Workspace />
      <Assistant />
    </main>
  )
}
