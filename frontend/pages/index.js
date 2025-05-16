import React from 'react';
import styles from '../styles/Home.module.css';
import Assistant from '../components/Assistant';
import Customizations from '../components/Customizations';
import Workspace from '../components/Workspace';
import Navbar from '../components/Navbar';
import '../lib/fontawesome'; // Import the fontawesome library

const Home = () => {
  return (
    <div className='homepage'>
      <Navbar />
      <main>
        <Customizations />
        <Workspace />
        <Assistant />
      </main>
    </div>
  );
};

export default Home;