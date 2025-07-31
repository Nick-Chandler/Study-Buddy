import Navbar from '../components/Navbar';
import DefaultLayout from '../components/DefaultLayout';
import ReferenceLayout from '../components/ReferenceLayout';
import CSLayout from '../components/CSLayout';
import { useAuth } from '../components/AuthProvider';
import { useEffect } from 'react';
import { useLayout } from '../components/LayoutContext';
import SideThreadSelect from '../components/SideThreadSelect';


export default function index() {

  const { user } = useAuth()
  const { currentLayout } = useLayout();
  const componentMap = {
  'default': <DefaultLayout />,
  'reference': <ReferenceLayout />,
  'cs': <CSLayout />,
};

  useEffect(() => {
    console.log("Index - User: ", user)
  }, []);

  useEffect(() => {
      console.log("Index - Current Layout: ", currentLayout);
    }, [currentLayout]);


  return (
    <div className='homepage'>
      <Navbar />
      <main className='content'>
        {componentMap[currentLayout] || <DefaultLayout />}
        <SideThreadSelect />
      </main>
    </div>
  );
}