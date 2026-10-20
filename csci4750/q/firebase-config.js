// ---------------------------------------------------------------------------
// Firebase configuration for the CSCI 4750/5750 in-class question system.
//
// This course reuses the Firebase project set up for CSCI 4845/5845
// ("csci4845-poll"; one-time setup steps in ../../csci4845/q/SETUP.md).
// Every document lives under courses/{COURSE}/..., so the two courses never
// see each other's questions, live state, or responses, and the same
// firestore.rules (which match /courses/{course}/...) cover both. The domain
// jinzhao3611.github.io is already authorized, so no console work is needed.
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
export const COURSE = "csci4750-s27";

// Only these Google accounts can control questions from present.html.
// Must match the emails in firestore.rules.
// (jin.zhao@slu.edu is not a Google account, so the personal Gmail is used.)
export const INSTRUCTOR_EMAILS = ["jinzhao3611@gmail.com"];

// URL the QR code points students to.
export const STUDENT_URL = "https://jinzhao3611.github.io/csci4750/q/";

export const configured = firebaseConfig.projectId !== "PASTE_ME";
