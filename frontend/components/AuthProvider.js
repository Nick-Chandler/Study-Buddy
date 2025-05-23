// context/AuthContext.js
import { createContext, useState, useContext, useEffect, use } from "react";
import Router, { useRouter } from "next/router";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState({});
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState();
  const [activeMessages, setActiveMessages] = useState([]);
  const [userConversations, setUserConversations] = useState([]);
  const router = useRouter();

  useEffect(() => {
    console.log("Context - Rendered")
  }, []);

  useEffect(() => {
    console.log("Context - User on Load", user);
    if (!user || user === null || user === undefined || user =={})
      return
    console.log("Context - Setting Conversations for User", user);
    getUserConversations(user?.user?.id || []);
  }, [user]);

  useEffect(() => {
      // Stopped here - get user conversation messages
    }, [activeConversation]);

  function addMessage(msg) {
    
  }

  const login = (userData) => {
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData)); // Save user data to localStorage
    console.log("Context - User on Load", userData);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("user"); // Clear user data from localStorage
    router.reload();
  };

  async function getUserConversations(userId) {
    if (!userId || userId.length === 0 || userId === null || userId === undefined) 
      return
    try {
      let url = `http://localhost:8000/get_user_thread_list/${userId}`;
      console.log("URL:", url);
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const threadArray = await response.json();  // <- this is your JSON array
      console.log("User Conversations:", threadArray);
      console.log(typeof threadArray);
      const objectArray = threadArray.map(obj => ({
        name: obj.name,
        thread_id: obj.thread_id,
      }));
      setUserConversations(objectArray);
    } catch (error) {
      console.error("Failed to fetch user conversations:", error);
      return setUserConversations([]); // Set to empty array on error
    }
  }



  return (
    <AuthContext.Provider
      value={{
        user,
        conversations,
        activeConversation,
        activeMessages,
        userConversations,
        setActiveConversation,
        addMessage,
        login,
        logout,
        getUserConversations,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
