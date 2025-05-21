// context/AuthContext.js
import { createContext, useState, useContext, useEffect } from 'react';
import Router, { useRouter } from 'next/router';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null)
    const [conversations, setConversations] = useState([])
    const [activeConversation, setActiveConversation] = useState(1)
    const router = useRouter()

    useEffect(() => {
        const storedUser = JSON.parse(localStorage.getItem('user'))
        if (storedUser !== "undefined") {
          setUser(storedUser); // Restore user data from localStorage
        }
    }, []);

    useEffect(() => {
    }, [user]);

    const login = (userData) => {
        setUser(userData)
        setConversations(userData.conversations.data); // Set conversations from user data
        localStorage.setItem('user', JSON.stringify(userData)); // Save user data to localStorage
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('user'); // Clear user data from localStorage
        router.reload();
    };

    return (
        <AuthContext.Provider value={{ user, conversations, activeConversation, setActiveConversation, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}


