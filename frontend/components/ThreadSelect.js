import React, { act, useEffect } from "react";
import Styles from '../styles/Navbar.module.css'
import { useAuth } from './AuthProvider'

export default function ThreadSelect() {

  const {activeThread, threads, setActiveThread} = useAuth()

  function handleThreadChange(e) {
    let newConvoIdx = e.target.value
    console.log("newConvoIdx: ", newConvoIdx)
    console.log(`Setting Active Thread to: `, e.target.value)
    console.log("New Thread Index: ", newConvoIdx)
    setActiveThread(e.target.value);
    console.log("Thread Changed", e.target.value)
  }



  return (
    <select
      onChange={handleThreadChange}
      className={Styles.threadSelect}
      value={activeThread}
    >
      {threads.map((thread, i) => (
        <option onChange={handleThreadChange} key={i} value={thread.thread_id}>
          {thread.name}
        </option>
      ))}
    </select>
  );
}
