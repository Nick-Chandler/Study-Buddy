// context/AuthContext.js
import { createContext, useState, useContext, useEffect } from "react";
import Router, { useRouter } from "next/router";
import { useRef } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {

  console.log("AuthProvider - Rendered");
  
  const [user, setUser] = useState({});
  const [conversations, setConversations] = useState([]);
  const [activeThread, setActiveThread] = useState(0);
  const [activeMessages, setActiveMessages] = useState([]);
  const [userConversations, setUserConversations] = useState([]);
  const router = useRouter();

  console.log("AuthProvider - States Generated");

  function generateUniqueId() {
    return Date.now().toString(36) + Math.random().toString(36).substring(2, 11)
  }

  useEffect(() => {
    console.log("Checking for Login Token");
    validateLoginToken()
    }, []);

  function createLoginToken(user) {
    const tokenId = generateUniqueId();
    const token = {
      id: tokenId,
      user: user.user.id,
      lastAccess: new Date().getTime(),
    };
    localStorage.setItem("loginToken", JSON.stringify(token));
    
    return token;
  }

  function validateLoginToken() {
    if (!localStorage.getItem("loginToken")) {
      console.log("Token Validation - No Login Token Found")
      return false;
    }

    let userData = JSON.parse(localStorage.getItem("user"));
    if (!userData) {
      console.log("Token Validation - No User Data Found");
      return false;
    }
    const token = JSON.parse(localStorage.getItem("loginToken"));
    console.log("Token Validation - Login Token Found: ", token);
    const lastAccess = token.lastAccess
    const oneWeekMs = 7 * 24 * 60 * 60 * 1000
    const now = Date.now()
    console.log("Token Validation - Current Time: ", now);
    console.log("Token Validation - Last Access Time: ", lastAccess);
    if (now - lastAccess > oneWeekMs) {
      console.log("Token Validation - Login Token Expired");
      return false;
    }
    console.log("Token Validation - Login Token Valid");
    console.log("Token Validation - Logging in User: ", userData);
    login(userData);
    return true
  }

  console.log("Starting useEffects");


  useEffect(() => {
    console.log("User Changed: ", user);
    if (!user || user === null || user === undefined || user == {}) return;
    console.log("Context - Setting Conversations for User", user);
    getUserConversations(user?.user?.id || []);
  }, [user]);

  
  const login = (userData) => {
    console.log("Context - Logging in User: ", userData);
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData)); // Save user data to localStorage
    console.log("Context - User on Load", userData);
    createLoginToken(userData);
  };
  
  const logout = () => {
    setUser(null);
    localStorage.removeItem("user"); // Clear user data from localStorage
    localStorage.removeItem("loginToken"); // Clear user data from localStorage
    router.reload();
  };
  
  async function getUserConversations(userId) {
    if (
      !userId ||
      userId.length === 0 ||
      userId === null ||
      userId === undefined
    )
      return;
      try {
        let url = `http://localhost:8000/get_user_thread_list/${userId}`;
        console.log("Thread List URL:", url);
        const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const threadArray = await response.json(); // <- this is your JSON array
      console.log("User Conversations:", threadArray);
      console.log(typeof threadArray);
      const objectArray = threadArray.map((obj) => ({
        name: obj.name,
        thread_id: obj.thread_id,
      }));
      setUserConversations(objectArray);
    } catch (error) {
      console.error("Failed to fetch user conversations:", error);
      return setUserConversations([]); // Set to empty array on error
    }
  }
  function addMessage(msg, role) {
    console.log("Context - Adding Message: ", msg);
    let temp_msg = {
      id: generateUniqueId(),
      role: role,
      text: msg,
    }
    setActiveMessages((prevMessages) => [temp_msg, ...prevMessages]);
  }
  
  async function getAiResponse(user_id, thread_idx, user_input) {
    const url = `http://localhost:8000/assistant/${user_id}/${thread_idx}`
    console.log("Context - thread_idx: ", thread_idx)
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_input: user_input })
    })

    const data = await response.json()
    console.log("Assistant - Response: ", data)
    return data.message
}


  return (
    <AuthContext.Provider
      value={{
        user,
        conversations,
        activeThread,
        activeMessages,
        userConversations,
        setActiveThread,
        setActiveMessages,
        addMessage,
        login,
        logout,
        getUserConversations,
        getAiResponse,
        validateLoginToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
