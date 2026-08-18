// ---------------------------------------------------------------------------
// Firebase configuration for the CSCI 4845/5845 in-class question system.
//
// SETUP (one time):
//   1. console.firebase.google.com → Add project (e.g. "csci4845-poll").
//      Google Analytics: not needed — disable.
//   2. Build → Firestore Database → Create database → Start in production mode.
//   3. Firestore → Rules tab → paste the contents of firestore.rules → Publish.
//   4. Build → Authentication → Sign-in method → enable BOTH:
//        - Anonymous            (students)
//        - Google               (instructor)
//   5. Project settings (gear) → Your apps → "</>" (Web) → register app →
//      copy the config object and paste it below, replacing the PASTE_ME values.
//   6. Project settings → Authorized domains: add jinzhao3611.github.io
// ---------------------------------------------------------------------------

export const firebaseConfig = {
  apiKey: "PASTE_ME",
  authDomain: "PASTE_ME.firebaseapp.com",
  projectId: "PASTE_ME",
  storageBucket: "PASTE_ME.appspot.com",
  messagingSenderId: "PASTE_ME",
  appId: "PASTE_ME",
};

// Firestore documents live under courses/{COURSE}/...
export const COURSE = "csci4845-f26";

// Only these Google accounts can control questions from present.html.
// Must match the emails in firestore.rules.
export const INSTRUCTOR_EMAILS = ["jin.zhao@slu.edu"];

// URL the QR code points students to.
export const STUDENT_URL = "https://jinzhao3611.github.io/csci4845/q/";

export const configured = firebaseConfig.projectId !== "PASTE_ME";
