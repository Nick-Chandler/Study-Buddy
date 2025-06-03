import React, { use, useEffect } from 'react'
import { useState } from 'react'
import { useAuth } from './AuthProvider'
import ReactMarkdown from 'react-markdown'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import 'katex/dist/katex.min.css'
import Styles from '../styles/NewAssistant.module.css'

export default function MessageList(props) {

  const { user, threads, activeThread, activeMessages, setActiveThread, setActiveMessages, addMessage } = useAuth()
  const [key, setKey] = useState(0)

  useEffect(() => {
    console.log("MessageList - Active Messages: ", activeMessages);
  }, [activeMessages]);


  return (
    <ul className={Styles.messages}>
      {activeMessages.map((message, index) => (
        <li key={index} className={Styles.message}>
          <div className={Styles[message.role]}>
            <ReactMarkdown
              children={message.text}
              remarkPlugins={[remarkMath]}
              rehypePlugins={[rehypeKatex]}
            />
          </div>
        </li>
      ))}
    </ul>
  )
}
