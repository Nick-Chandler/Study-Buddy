// context/AuthContext.js
import { createContext, useState, useContext, useEffect } from "react";
import Router, { useRouter } from "next/router";
import { useRef } from "react";

const ThemeContext = createContext();

export function ThemeProvider({ children }) {

  const [theme, setTheme] = useState('dark'); // Default theme is 'dark'

  useEffect(() => {
    changeTheme(theme);
  },[theme])

  function changeTheme(newTheme) {
    let background = document.querySelector('body');
    let navbar = document.querySelector('nav');
    if (newTheme == 'light') {
      navbar.classList.add('light-theme');
      navbar.classList.remove('dark-theme');
    } 
    else {
      navbar.classList.remove('light-theme');
      navbar.classList.add('dark-theme');
    }

    
    background.style.backgroundColor = newTheme === 'dark' ? '#121212' : '#ffffff';
  }

  return (
    <ThemeContext.Provider
      value={{
        theme,
        setTheme,
        changeTheme
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
