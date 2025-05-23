import Assistant from '../components/Assistant';
import Customizations from '../components/Customizations';
import Workspace from '../components/Workspace';
import Navbar from '../components/Navbar';

export default function index() {

  console.log("Index Rendered")

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