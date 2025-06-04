import { createContext, useState, useContext, useEffect } from 'react';

const LayoutContext = createContext();

export function LayoutProvider({ children }) {
  const [currentLayout, setCurrentLayout] = useState("reference");
  const [availableLayouts, setAvailableLayouts] = useState(["default", "reference", "cs"]);
  const [referenceImg, setReferenceImg] = useState(null);

  return (
    <LayoutContext.Provider 
        value={{ 
        currentLayout,
        setCurrentLayout,
        availableLayouts,
        referenceImg,
        setReferenceImg
       }}>
      {children}
    </LayoutContext.Provider>
  );
}

export function useLayout() {
  return useContext(LayoutContext);
}
