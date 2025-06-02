import '../styles/Globals.css';
import { AuthProvider } from '../components/AuthProvider';
import { ThemeProvider } from '../components/ThemeProvider';
import { LayoutProvider } from '../components/LayoutContext';

export default function MyApp({ Component, pageProps }) {

  return (
    <AuthProvider>
      <ThemeProvider>
        <LayoutProvider>
          <Component {...pageProps} />
        </LayoutProvider>
      </ThemeProvider>
    </AuthProvider>
  );
}
