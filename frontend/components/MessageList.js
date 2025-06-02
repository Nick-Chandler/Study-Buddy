import React, { useEffect } from 'react'
import { useAuth } from './AuthProvider'
import ReactMarkdown from 'react-markdown'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import 'katex/dist/katex.min.css'
import Styles from '../styles/NewAssistant.module.css'

export default function MessageList(props) {

  const { user, threads, activeThread, activeMessages, setActiveThread, setActiveMessages, addMessage } = useAuth()

  useEffect(() => {
    console.log("MessageList Props: ", props.messages)
  }, [props.messages]);

  useEffect(() => {
    console.log("MessageList: Active Messages Changed: ", activeMessages)
  }, [activeMessages]);


  return (
    <ul className={Styles.messages}>
      {props.messages.map((message, index) => (
        <li key={index} className={Styles.message}>
          <div className={Styles[message.role]}>
            <ReactMarkdown 
            remarkPlugins={[remarkMath]} 
            rehypePlugins={[rehypeKatex]}
            >{message.text}
            </ReactMarkdown>
          </div>
        </li>
      ))}
    </ul>
  )
}
