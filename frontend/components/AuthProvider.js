// context/AuthContext.js
import { createContext, useState, useContext, useEffect, use } from "react";
import Router, { useRouter } from "next/router";
import { useRef } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {

  console.log("AuthProvider - Rendered");
  
  const [user, setUser] = useState({});
  const [loggedIn, setLoggedIn] = useState(false);
  const [activeMessages, setActiveMessages] = useState([]);
  const [threads, setThreads] = useState([]);
  const [activeThread, setActiveThread] = useState(threads.length > 0 ? threads[0].threadId : 0); // Initialize activeThread to first thread or 0 if none
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
      user: user.id,
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
    if(!user || Object.keys(user).length === 0)
      return
    console.log("User Changed: ", user)
    createLoginToken(user);
    if (!user || user === null || user === undefined) return;
    console.log("Context - Setting Threads for User", user);
    setLoggedIn(true);
  }, [user]);
  
  function login(userData) {
    console.log("Context - Logging in User: ", userData);
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData)); // Save user data to localStorage
    console.log("Context - User on Load", userData);
  };
  
  function logout () {
    setUser(null);
    localStorage.removeItem("user"); // Clear user data from localStorage
    localStorage.removeItem("loginToken"); // Clear user data from localStorage
    router.reload();
  };
  
  
  function addMessage(msg, role) {
    console.log("Context - Adding Message: ", msg);
    let temp_msg = {
      id: generateUniqueId(),
      role: role,
      text: msg,
    }
    setActiveMessages((prevMessages) => [ ...prevMessages, temp_msg]);
  }
  



  return (
    <AuthContext.Provider
      value={{
        user,
        activeThread,
        activeMessages,
        threads,
        loggedIn,
        setActiveThread,
        setActiveMessages,
        addMessage,
        login,
        logout,
        validateLoginToken,
        setThreads,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
