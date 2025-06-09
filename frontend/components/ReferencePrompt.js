import React from 'react'
import Styles from '../styles/ReferenceLayout.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus } from '@fortawesome/free-solid-svg-icons'
import { useLayout } from './LayoutContext'
export default function ReferencePrompt() {
  const { setReferenceImg } = useLayout();

  function handleReferenceUpload(e) {
    const file = e.target.files[0];
    const fileUrl = URL.createObjectURL(file);
    if (file) {
      setReferenceImg(fileUrl);
    }
  }

  return (
    <div className={Styles.referencePrompt}>
      {/* Hidden file input */}
      <input
        id="referenceUpload"
        type="file"
        style={{ display: 'none' }} // Hide the default input
        onChange={handleReferenceUpload}
      />
      {/* Custom-styled label */}
      <label htmlFor="referenceUpload" className={Styles.addReferenceBtn}>
        <FontAwesomeIcon icon={faPlus} />
      </label>
    </div>
  );
}
