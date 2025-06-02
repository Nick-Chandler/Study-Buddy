import Assistant from '../components/Assistant';
import Customizations from '../components/Customizations';
import Workspace from '../components/Workspace';
import Navbar from '../components/Navbar';
import DefaultLayout from '../components/DefaultLayout';
import ReferenceLayout from '../components/ReferenceLayout';
import CSLayout from '../components/CSLayout';
import { AuthProvider } from '../components/AuthProvider';
import { useAuth } from '../components/AuthProvider';
import { useEffect } from 'react';
import { useLayout } from '../components/LayoutContext';


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
      {componentMap[currentLayout] || <DefaultLayout />}
    </div>
  );
}