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
  apiKey: "AIzaSyCX6nmQIR2LiniWeFAyPJBN2djfEG1B7yc",
  authDomain: "csci4845-poll.firebaseapp.com",
  projectId: "csci4845-poll",
  storageBucket: "csci4845-poll.firebasestorage.app",
  messagingSenderId: "951485567085",
  appId: "1:951485567085:web:d535568375c7fc696caf64",
};

// Firestore documents live under courses/{COURSE}/...
export const COURSE = "csci4845-f26";

// Only these Google accounts can control questions from present.html.
// Must match the emails in firestore.rules.
// (jin.zhao@slu.edu is not a Google account, so the personal Gmail is used.)
export const INSTRUCTOR_EMAILS = ["jinzhao3611@gmail.com"];

// URL the QR code points students to.
export const STUDENT_URL = "https://jinzhao3611.github.io/csci4845/q/";

export const configured = firebaseConfig.projectId !== "PASTE_ME";
