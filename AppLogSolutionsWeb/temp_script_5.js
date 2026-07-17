
    import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
    import { getApps, initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
    import { getStorage } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-storage.js";
    import { firebaseConfig } from "./firebase-config.js";

    const app = getApps().length > 0 ? getApps()[0] : initializeApp(firebaseConfig);
    window.db = getFirestore(app);
    window.firebaseStorage = getStorage(app);
