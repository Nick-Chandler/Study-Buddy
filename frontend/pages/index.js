import Assistant from '../components/Assistant';
import Customizations from '../components/Customizations';
import Workspace from '../components/Workspace';
import Navbar from '../components/Navbar';
import { AuthProvider } from '../components/AuthProvider';
import { useAuth } from '../components/AuthProvider';
import { useEffect } from 'react';


export default function index() {

  const { user } = useAuth()

  useEffect(() => {
    console.log("Index - User: ", user)
  }, []);


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
}