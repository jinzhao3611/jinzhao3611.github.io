// Lecture 1 question set — record of what was uploaded to Firestore (Aug 2026).
// No longer imported by the app: new sets are added by pasting them into the
// presenter's "Add question set…" box (see SETUP.md).

export const LEC01 = [
  {
    id: "lec01-q1", order: 1, type: "mc",
    prompt: "What brings you to NLP? (pick the biggest reason)",
    choices: [
      "I want to build things with LLMs — career / industry skills",
      "I'm interested in NLP or ML research",
      "I want to understand how ChatGPT-style models actually work",
      "It fits my degree plan / schedule (honest answers welcome)",
      "Something else",
    ],
  },
  {
    id: "lec01-q2", order: 2, type: "mc",
    prompt: "Which best describes your background coming in?",
    choices: [
      "I've trained neural networks before (course or project)",
      "I've taken an ML course, but little hands-on deep learning",
      "Comfortable in Python, new to ML",
      "Still figuring out where I stand",
    ],
  },
  {
    id: "lec01-q3", order: 3, type: "mc",
    prompt: "How often do you use AI assistants (ChatGPT, Claude, Copilot, …)?",
    choices: ["Daily", "A few times a week", "Occasionally", "Rarely or never"],
  },
  {
    id: "lec01-q4", order: 4, type: "text",
    prompt: "In one sentence: what do you hope to be able to build or understand by December?",
  },
  {
    id: "lec01-q5", order: 5, type: "text",
    prompt: "Optional: anything you're worried about coming into this course?",
  },
];
