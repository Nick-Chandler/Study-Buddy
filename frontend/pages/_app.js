import '../styles/Globals.css';
import { AuthProvider } from '../components/AuthProvider';


export default function MyApp({ Component, pageProps }) {

  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}
