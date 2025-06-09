import React from 'react'
import Styles from '../styles/Assistant.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTrash } from '@fortawesome/free-solid-svg-icons'
import { useAuth } from './AuthProvider'


export default function DeleteButton() {


  const { user, activeThread } = useAuth()

  async function handleDeleteClick(e) {
    if(!window.confirm("Are you sure you want to delete this thread? This action cannot be undone."))
      return; // Exit if user cancels

    const url = `http://localhost:8000/delete_thread/${user.user.id}/${activeThread}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    if (!response.ok) {
      console.log("Failed to delete thread for User: ", user.user.id, " Thread: ", activeThread);
      return
    }
    
    const responseJSON = await response.json();
    console.log("Deleted Thread to : ", responseJSON.deletedThreadName);
    alert(`Thread "${responseJSON.deletedThreadName}" has been deleted.`);
    window.location.reload(); // Reload the page to reflect changes
    return responseJSON.deletedThreadName;
  }


  return (
    <button onClick={handleDeleteClick}><FontAwesomeIcon icon={faTrash} /></button>
  )
}
