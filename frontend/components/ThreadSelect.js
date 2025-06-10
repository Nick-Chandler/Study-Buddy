import React, { act, use, useEffect } from "react";
import Styles from '../styles/Navbar.module.css'
import { useAuth } from './AuthProvider'



export default function ThreadSelect() {

  const {user, activeThread, setActiveThread} = useAuth()

  function handleThreadChange(e) {
    let newConvoIdx = e.target.value
    console.log("newConvoIdx: ", newConvoIdx)
    console.log(`Setting Active Thread to: `, e.target.value)
    console.log("New Thread Index: ", newConvoIdx)
    setActiveThread(e.target.value);
    console.log("Thread Changed", e.target.value)
  }

  useEffect(() => {
    console.log("ThreadSelect - Rendered");
    console.log("ThreadSelect - User Threads: ", user.threads);
    console.log("ThreadSelect - Active Thread: ", activeThread);
  }, []);



  return (
    <select
      onChange={handleThreadChange}
      className={Styles.threadSelect}
      value={activeThread}
    >
      {user.threads.map((thread, i) => (
        <option onChange={handleThreadChange} key={i} value={thread.threadId}>
          {thread.name}
        </option>
      ))}
    </select>
  );
}
