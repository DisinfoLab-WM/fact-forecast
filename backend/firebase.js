import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";
import 'dotenv/config';

/**
 * @details Firebase configuration for the project
 */

const firebaseConfig = {
  apiKey:process.env.FIREBASE_API_KEY,
  authDomain: "disinfopractice.firebaseapp.com",
  databaseURL: "https://disinfopractice-default-rtdb.firebaseio.com",
  projectId: "disinfopractice",
  storageBucket: "disinfopractice.firebasestorage.app",
  messagingSenderId: "834128285827",
  appId: "1:834128285827:web:486cffa240652d86550bb6",
  measurementId: "G-KNXV99Q533"
};


// Initialize Firebase  
const app = initializeApp(firebaseConfig);

/**
 * @details db is the const for referencing/accessing the database
 */
export const db = getDatabase(app);
