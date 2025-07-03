import React, { act, use, useEffect } from "react";
import Styles from '../styles/Navbar.module.css'
import { useAuth } from './AuthProvider'



export default function ThreadSelect() {

  const {user, threads, setThreads, activeThread, setActiveThread} = useAuth()

  function handleThreadChange(e) {
    let newConvoIdx = e.target.value
    console.log("newConvoIdx: ", newConvoIdx)
    console.log(`Setting Active Thread to: `, e.target.value)
    console.log("New Thread Index: ", newConvoIdx)
    setActiveThread(e.target.value);
    console.log("Thread Changed", e.target.value)
  }

  async function getUserThreads(userId) {
    console.log("Get User Threads - User:", user)
    if (
      !user.userId ||
      user.userId === null ||
      user.userId === undefined
    )
      return;
    const url = `http://localhost:8000/get_user_thread_list/${userId}`;
    console.log("Get User Threads - Threads URL: ", url);
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      console.log("Get Thread List - No Threads Found for User: ", userId);
    }
    const threads = await response.json();
    console.log("Get Thread List - Got Response: ", threads)
    setThreads(threads);
    return threads;
  }

  useEffect(() => {
    console.log("ThreadSelect - Rendered");
    console.log("ThreadSelect - User Threads: ", threads);
    console.log("ThreadSelect - Active Thread: ", activeThread);
    getUserThreads(user.userId);
  }, []);

  useEffect(() => {
    console.log("ThreadSelect - Threads Changed: ", threads);
    console.log("ThreadSelect - Active Thread: ", activeThread);
  },[threads])



  return (
    <select
      onChange={handleThreadChange}
      className={Styles.threadSelect}
      value={activeThread}
    >
      {threads.map((thread, i) => (
        <option onChange={handleThreadChange} key={i} value={thread.threadId}>
          {thread.name}
        </option>
      ))}
    </select>
  );
}
