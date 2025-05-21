import Styles from '../styles/Assistant.module.css'
import { useState, useEffect } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowUpFromBracket } from '@fortawesome/free-solid-svg-icons'
import { useAuth } from './AuthProvider'

export default function Assistant() {
  const [input, setInput] = useState('')
  const { user, conversations, activeConversation, setActiveConversation } = useAuth()
  const [messages, setMessages] = useState([])
  const cid = conversations[activeConversation-1]?.conversation_id || 1

  // Function to fetch the response from the API

  useEffect(() => {
    console.log("Assistant - Active Conversation on Load",activeConversation)
    console.log(conversations)
  }, []);

  useEffect(() => {
    console.log("Assistant - Active Conversation on Change: ", activeConversation)
    let currentMessages = conversations[activeConversation-1]?.messages || []
    setMessages(currentMessages)
  },[activeConversation])

  async function fetchResponse(userInput) {
    try {
      const response = await fetch(`http://127.0.0.1:8000/assistant/${cid}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userInput }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessages((prevMessages) => [
          ...prevMessages,
          { content: data.message, type: 'assistant' } // Add assistant's response
        ]);
      } else {
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };



  // Handle form submission
  async function handleSubmit(e){
    e.preventDefault();
    if (input.trim() === '') return;

    setMessages((prevMessages) => [
      ...prevMessages,
      { content: input, type: 'user' } // Add user's input
    ]);
    fetchResponse(input); // Call the function to fetch the response from the API
    setInput('');
  };

  return (
    <section className={Styles.assistant}>
      <h1>AI Assistant</h1>
      <div className={Styles.content}>
        <ul className={Styles.messages}>
          {messages.map((message, index) => (
            <li key={index}>
              <p className={Styles[message.role]}>{message.content}</p> {/* Wrap the message content in a <p> tag */}
            </li>
          ))}
        </ul>
      </div>
      <form id='input' className={Styles.input} onSubmit={handleSubmit}>
        <input
          className={Styles.inputField}
          type="text"
          placeholder="Need help? Ask me anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)} // Update state on input change
        />
        <button type="submit">
          <FontAwesomeIcon className={Styles.upload} icon={faArrowUpFromBracket} />
        </button>
      </form>
    </section>
  );
}