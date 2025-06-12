import React from 'react'
import { useState } from 'react'
import { useLayout } from './LayoutContext';

export default function LayoutsButton() {
  const [open, setOpen] = useState(false);
  const { currentLayout, setCurrentLayout } = useLayout();

  function handleLayoutChange(layout) {
    if (currentLayout === layout) {
      return;
    }
    // alert(`Layout changed to: ${layout}`);
    setCurrentLayout(layout);
    document.getElementById('layoutButton').click()
  }

  return (
    <div >
      <button id='layoutButton' onClick={() => setOpen(!open)}>
        Layout Menu
      </button>
      {open && (
        <div style={{
          position: 'absolute',
          border: '1px solid black',
          marginBottom: "50%",
          marginLeft: "10%",
          backgroundColor: 'white',
          zIndex: 1000,
        }}>
          <ul style={{border: "3px solid black", padding: "10px", margin: 0, listStyleType: 'none'}}>
            <li onClick={() => handleLayoutChange("default")} style={{ border: '1px solid black', color: "black", cursor: "pointer" }}>Default Layout</li>
            <li onClick={() => handleLayoutChange("reference")}style={{ border: '1px solid black', color: "black", cursor: "pointer" }}>Reference Layout</li>
            <li onClick={() => handleLayoutChange("cs")} style={{ border: '1px solid black', color: "black", cursor: "pointer" }}>CS Layout</li>
          </ul>
        </div>
      )}
    </div>
  )
}

