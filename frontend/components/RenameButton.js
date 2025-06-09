import React from 'react'
import { useAuth } from './AuthProvider'
import Styles from '../styles/Assistant.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPenToSquare } from '@fortawesome/free-solid-svg-icons'

export default function RenameButton() {

  const { user, threads, activeThread, setActiveThread } = useAuth()

  async function handleRenameClick(e) {
    let newThreadName = prompt("Enter new thread name: ");
    let taken = threads.some(t => t.name === newThreadName);
    while(taken || !newThreadName) {
      if(!newThreadName) {
        console.log("Rename Thread - User cancelled rename operation");
        return; // Exit if user cancels
      }
      newThreadName = prompt("Thread name already taken. Please enter a different name: ");
      taken = threads.some(t => t.name === newThreadName);
  }
    const url = `http://localhost:8000/rename_thread/${user.user.id}/${activeThread}/${newThreadName}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    if (!response.ok) {
      console.log("Get Thread Messages - No Messages Found for User: ", user.user.id, " Thread: ", activeThread);
    }
    
    const responseJSON = await response.json();
    console.log("Rename Thread to : ", responseJSON.newThreadName);
    window.location.reload(); // Reload the page to reflect changes
    return responseJSON.newThreadName;
  }
  return (
    <button className={Styles.renamebtn} onClick={handleRenameClick}><FontAwesomeIcon icon={faPenToSquare} /></button>
  )
}

