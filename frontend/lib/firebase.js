// Import the functions you need from the SDKs you need
import { initializeApp, getApps } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, GoogleAuthProvider } from "firebase/auth"
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyABiz0abza8--jWZ7W2qnk36OtIrOq0TlQ",
  authDomain: "study-buddy-c73e5.firebaseapp.com",
  projectId: "study-buddy-c73e5",
  storageBucket: "study-buddy-c73e5.firebasestorage.app",
  messagingSenderId: "238818243625",
  appId: "1:238818243625:web:4282811d813ae3362a9838",
  measurementId: "G-HXE7ES41GN"
};

// ✅ Prevent re-initialization
const app = getApps().length ? getApps()[0] : initializeApp(firebaseConfig)

// ✅ Only access auth in the browser
let auth = null
let provider = null

if (typeof window !== "undefined") {
  auth = getAuth(app)
  provider = new GoogleAuthProvider()
}

export { auth, provider }