// context/AuthContext.js
import { createContext, useState, useContext, useEffect, use } from "react";
import Router, { useRouter } from "next/router";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState();
  const [activeMessages, setActiveMessages] = useState([]);
  const router = useRouter();

  useEffect(() => {
    const storedUser = JSON.parse(localStorage.getItem("user"));
    if (storedUser !== "undefined") {
      setUser(storedUser); // Restore user data from localStorage
    }
    login(storedUser); // Call login function with stored user data
    console.log("Context - User on Load: ", user);
  }, []);

  useEffect(() => {
    console.log("Logged in user: ", user);
    if (user) {
      setActiveConversation(user.lastConversation);
      console.log("Conversations:", conversations);
    }
  }, [user]);

  useEffect(() => {
    console.log("Context - Active Conversation on Change: ",activeConversation);
    let newMessages = [];
    for (const c of conversations) {
      if (c.conversation_id === activeConversation) {
          newMessages = c.messages; // Return the messages array
          console.log("Context - Active Messages: ", c.messages);
      }
    }; 
    setActiveMessages(newMessages);
    }, [activeConversation]);

  function addMessage(msg) {
    setActiveMessages((messages) => [...messages, msg]);
  }

  const login = (userData) => {
    console.log("Logging in user: ", userData);
    setUser(userData);
    setConversations(userData.conversations.data); // Set conversations from user data
    localStorage.setItem("user", JSON.stringify(userData)); // Save user data to localStorage
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("user"); // Clear user data from localStorage
    router.reload();
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        conversations,
        activeConversation,
        activeMessages,
        setActiveConversation,
        addMessage,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
