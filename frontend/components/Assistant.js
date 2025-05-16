import React from 'react';
import styles from '../styles/Assistant.module.css';
import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowUpFromBracket } from '@fortawesome/free-solid-svg-icons'

export default function Assistant() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  // Function to fetch the response from the API
  async function fetchResponse(userInput) {
    try {
      const response = await fetch('http://127.0.0.1:8000/assistant/', {
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
    <section className={styles.assistant}>
      <h1>AI Assistant</h1>
      <div className={styles.content}>
        <ul className={styles.messages}>
          {messages.map((message, index) => (
            <li key={index} className={styles[message.type]}>
              <p>{message.content}</p> {/* Wrap the message content in a <p> tag */}
            </li>
          ))}
        </ul>
      </div>
      <form className={styles.input} onSubmit={handleSubmit}>
        <input
          className={styles.inputField}
          type="text"
          placeholder="Need help? Ask me anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)} // Update state on input change
        />
        <button type="submit">
          <FontAwesomeIcon className={styles.upload} icon={faArrowUpFromBracket} />
        </button>
      </form>
    </section>
  );
}
