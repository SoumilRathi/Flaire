// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyComNf7tqVebInMqnm6Xnuj5RCnXhg3wXk",
  authDomain: "styler-888.firebaseapp.com",
  projectId: "styler-888",
  storageBucket: "styler-888.appspot.com",
  messagingSenderId: "289436446890",
  appId: "1:289436446890:web:c70f2385c043cfe2e7e0d3",
  measurementId: "G-FR5KCXCHQW"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);