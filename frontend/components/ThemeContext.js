// context/AuthContext.js
import { createContext, useState, useContext, useEffect } from "react";
import Router, { useRouter } from "next/router";
import { useRef } from "react";

const ThemeContext = createContext();

export function ThemeProvider({ children }) {

  const [theme, setTheme] = useState('light'); // Default theme is 'light'

  function changeTheme(newTheme) {
    
  }

  return (
    <ThemeContext.Provider
      value={{
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useAuth() {
  return useContext(ThemeContext);
}
