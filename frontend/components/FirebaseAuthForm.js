"use client" // for Next.js App Router

import { useState } from "react"
import { auth } from "../lib/firebase"
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword
} from "firebase/auth"

export default function FirebaseAuthForm() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isLogin, setIsLogin] = useState(true)

  const handleSubmit = async e => {
    e.preventDefault()
    try {
      if (isLogin) {
        await signInWithEmailAndPassword(auth, email, password)
        console.log("Logged in!")
      } else {
        await createUserWithEmailAndPassword(auth, email, password)
        console.log("Account created!")
      }
    } catch (err) {
      console.error("Auth error:", err.message)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button type="submit">{isLogin ? "Log In" : "Sign Up"}</button>
      <p onClick={() => setIsLogin(!isLogin)} style={{ cursor: "pointer" }}>
        {isLogin ? "Need an account? Sign up" : "Already have an account? Log in"}
      </p>
    </form>
  )
}
