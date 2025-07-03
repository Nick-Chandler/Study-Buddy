import React, { useEffect } from 'react'
import Styles from '../styles/Navbar.module.css'
import { useAuth } from './AuthProvider'

export default function NewThread() {

  const { user, threads, setActiveThread, setThreads, setActiveMessages} = useAuth()



  async function handleNewThread() {
    // Ask for a new thread name
    const threadName = prompt("Enter a name for the new thread: ");
    if(!threadName) 
      return
    const userId = user.userId
    // Make a POST request to create a new thread with the chosen name or default name
    let newThreadId =  await requestNewThread(userId, threadName || "Untitled Thread")
    // setActiveThread to the new thread ID
    setThreads([
      { name: threadName, threadId: newThreadId }
      , ...threads,
    ]);
    setActiveThread(newThreadId);
    setActiveMessages([]); // Clear active messages when threads change
  }

  async function requestNewThread(userId, threadName) {
    console.log("Requesting New Thread from API");
    const url = `http://localhost:8000/create_thread_for_user/${userId}/${threadName}`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        console.error("Failed to create a new thread", response.statusText);
        return false;
      }

      const data = await response.json();
      console.log("New Thread Created: ", data);
      const { threadId, name } = data
      console.log("New Thread ID: ", threadId);
      console.log("New Thread Name: ", name);
      
      return threadId; // Change to return the new thread ID
    } catch (error) {
      console.error("Error while creating a new thread", error);
      return false;
    }
  }

  return (
    <button className={Styles.newThreadbtn} onClick={handleNewThread}>
      New Thread
    </button>
  )
}
