import React from 'react'
import Styles from '../styles/NewAssistant.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons'

export default function FileThumbnail({src,alt,deleteFile}) {
  return (
    <div className={Styles.fileThumbnail}>
      <button type='button'
      className={Styles.fileThumbnailDelete} 
      onClick={(e) => {
          e.preventDefault(); // Prevent form submission
          deleteFile();
        }}>
        <FontAwesomeIcon icon={faTimes} />
      </button>
      <img src={src} alt={alt} className={Styles.fileThumbnailImage}/>
    </div>
  )
}
