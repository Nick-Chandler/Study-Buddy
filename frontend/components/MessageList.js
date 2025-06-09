import React, { use, useEffect } from 'react'
import { useState } from 'react'
import { useAuth } from './AuthProvider'
import ReactMarkdown from 'react-markdown'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import 'katex/dist/katex.min.css'
import Styles from '../styles/NewAssistant.module.css'
import Message from './Message'

export default function MessageList(props) {

  const { user, threads, activeThread, activeMessages, setActiveThread, setActiveMessages, addMessage } = useAuth()
  const [key, setKey] = useState(0)

  useEffect(() => {
    console.log("MessageList - Active Messages: ", activeMessages);
  }, [activeMessages]);

  function autoMathFormat(text) {
  // Convert \(...\) to $...$
  text = text.replace(/\\\((.+?)\\\)/g, (match, p1) => `$${p1.trim()}$`);
  // Convert \[...\] to $$...$$
  text = text.replace(/\\\[(.+?)\\\]/g, (match, p1) => `$$${p1.trim()}$$`);

  // Convert any equation on its own line not already wrapped to block math
  text = text.split('\n').map(line => {
    // Check for a simple math equation (improve regex for your needs)
    if (
      /^[\s\(\)A-Za-z0-9+\-/*^=<>|.,:;{}\[\]\\]+$/.test(line.trim()) &&
      !line.trim().startsWith('$') &&
      (line.includes('=') || line.includes('^'))
    ) {
      return `$$${line.trim()}$$`;
    }
    return line;
  }).join('\n');

  return text;
}


  return (
    <ul className={Styles.messages}>
      {activeMessages.map((message, index) => (
        <li key={index} className={Styles.message}>
          <div className={Styles[message.role]}>
            <Message
              content={autoMathFormat(message.text)}
              role={message.role}
              className={Styles.message} // If your Message component takes className
              // Add more props if needed (like time, username, etc.)
            />
          </div>
            
        </li>
        
      ))}
    </ul>
  )
}
