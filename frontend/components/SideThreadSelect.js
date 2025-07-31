import Styles from '../styles/SideThreadSelect.module.css'

export default function SideThreadSelect() {
  return (
    <nav className={Styles.SideThreadSelect}>
      <button className={Styles.SideThreadToggleBtn}>Side</button>
      <ul className={Styles.SideThreadList}>
        <li className={Styles.SideThreadListItem}></li>
        <li className={Styles.SideThreadListItem}></li>
        <li className={Styles.SideThreadListItem}></li>
        <li className={Styles.SideThreadListItem}></li>
        <li className={Styles.SideThreadListItem}></li>
      </ul>
    </nav>
  );
}