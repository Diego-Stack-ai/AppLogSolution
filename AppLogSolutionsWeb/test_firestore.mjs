import { initializeApp } from "firebase/app";
import { getFirestore, doc, setDoc } from "firebase/firestore";

const firebaseConfigDev = {
  apiKey: "AIzaSyCfM1An6ekvcO4Y3a-UooJiEi2g5JkShFQ",
  authDomain: "log-solutions-sviluppo.firebaseapp.com",
  projectId: "log-solutions-sviluppo",
  storageBucket: "log-solutions-sviluppo.firebasestorage.app",
  messagingSenderId: "1097538489312",
  appId: "1:1097538489312:web:03390d3823f80f9c367985"
};

const app = initializeApp(firebaseConfigDev);
const db = getFirestore(app);

async function test() {
  try {
    await setDoc(doc(db, "test/test"), { a: 1 });
    console.log("Success");
  } catch (e) {
    console.error("Error:", e);
  }
}

test();
