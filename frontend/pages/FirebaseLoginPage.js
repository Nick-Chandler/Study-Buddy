// src/SignIn.js
import React from "react"
import { useState } from "react"
import { signInWithPopup } from "firebase/auth"
import { auth, provider } from "../lib/firebase"
import FirebaseAuthForm from "../components/FirebaseAuthForm"


export default function FirebaseLoginPage() {

  console.log("auth:", auth)
  console.log("auth currentUser:", auth?.currentUser)
  console.log("Current User:",auth?.currentUser ? auth.currentUser : "No User")
  const handleGoogleSignIn = () => {
    signInWithPopup(auth, provider)
      .then(result => {
        const user = result.user
        console.log("Signed in as:", user.displayName)
        console.log("User", user)
        console.log(auth.currentUser?.email)
        console.log(typeof auth.currentUser?.email)
      })
      .catch(error => {
        console.error("Error signing in:", error.message)
      })
  }

  return (
    <div>
      <FirebaseAuthForm />
      <button onClick={handleGoogleSignIn}>
        Sign in with Google
      </button>
    </div>
  )
}
