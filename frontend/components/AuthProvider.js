// context/AuthContext.js
import { createContext, useState, useContext, useEffect } from 'react';
import Router, { useRouter } from 'next/router';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const router = useRouter();

    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        console.log(typeof storedUser)
        if (storedUser !== "undefined") {
          console.log(storedUser)
          setUser(JSON.parse(storedUser)); // Restore user data from localStorage
        }
    }, []);

    const login = (userData) => {
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData)); // Save user data to localStorage
        console.log(userData);
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('user'); // Clear user data from localStorage
        router.reload();
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}


