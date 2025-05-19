import { useState, useContext } from 'react';
import { useRouter } from 'next/router'
import { useAuth } from '../components/AuthProvider';
import Link from 'next/link'
import Styles from '../styles/Login.module.css';

export default function login() {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter()

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      if (response.ok) {
        console.log(data)
        login(data.user)
        alert(data.message);
        router.push('/')
      } else {
        setError(data.error || 'Login failed');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    }
  };

  return (
    <div>
      <h1 className={Styles.header}>Login</h1>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
      <Link className={Styles.register} href="/register">
        <button>Register</button>
      </Link>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}


