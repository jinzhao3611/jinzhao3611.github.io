// Lecture 1 question set — record of what is uploaded to Firestore.
// Expanded Aug 2026: the old HW0 background survey is folded in (HW0 removed).
// Not imported by the app: sets are added by pasting them into the presenter's
// "Add question set…" box (see SETUP.md). Survey's "anything you want me to
// know" (accessibility/scheduling) deliberately excluded — free-text answers
// show on the projector; that item goes to email/office hours instead.

export const LEC01 = [
  {
    id: "lec01-q1", order: 1, type: "mc", set: "lec01",
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
    id: "lec01-q2", order: 2, type: "mc", set: "lec01",
    prompt: "Which best describes your background coming in?",
    choices: [
      "I've trained neural networks before (course or project)",
      "I've taken an ML course, but little hands-on deep learning",
      "Comfortable in Python, new to ML",
      "Still figuring out where I stand",
    ],
  },
  {
    id: "lec01-q3", order: 3, type: "mc", set: "lec01",
    prompt: "How often do you use AI assistants (ChatGPT, Claude, Copilot, …)?",
    choices: ["Daily", "A few times a week", "Occasionally", "Rarely or never"],
  },
  {
    id: "lec01-q4", order: 4, type: "text", set: "lec01",
    prompt: "In one sentence: what do you hope to be able to build or understand by December?",
  },
  {
    id: "lec01-q5", order: 5, type: "text", set: "lec01",
    prompt: "Optional: anything you're worried about coming into this course?",
  },
  {
    id: "lec01-q6", order: 6, type: "mc", set: "lec01",
    prompt: "Which program are you in?",
    choices: ["M.S. in AI", "M.S. in CS", "B.S. (senior undergraduate)", "Other"],
  },
  {
    id: "lec01-q7", order: 7, type: "mc", set: "lec01",
    prompt: "How comfortable are you with Python?",
    choices: [
      "I write Python weekly",
      "Comfortable, but a bit rusty",
      "I know the basics",
      "Still learning (honest answers welcome)",
    ],
  },
  {
    id: "lec01-q8", order: 8, type: "mc", set: "lec01",
    prompt: "Math background — probability, linear algebra, calculus?",
    choices: [
      "Comfortable with all three",
      "Comfortable with some, rusty on others",
      "Rusty on most of it",
      "Minimal exposure",
    ],
  },
  {
    id: "lec01-q9", order: 9, type: "mc", set: "lec01",
    prompt: "Have you used LLM APIs (OpenAI, Anthropic, …) from code?",
    choices: [
      "Regularly",
      "A few times",
      "Never from code, but I use the chat apps",
      "Never",
    ],
  },
  {
    id: "lec01-q10", order: 10, type: "mc", set: "lec01",
    prompt: "Which topic are you most excited about?",
    choices: [
      "Classical NLP foundations",
      "Transformers & building LLMs",
      "RAG & agents",
      "Evaluation & safety",
      "Multilingual & speech",
    ],
  },
  {
    id: "lec01-q11", order: 11, type: "mc", set: "lec01",
    prompt: "Can you bring a laptop or tablet with a browser + internet to class?",
    choices: ["Yes, every class", "Usually", "Rarely — phone only", "No"],
  },
  {
    id: "lec01-q12", order: 12, type: "text", set: "lec01",
    prompt: "What computer will you use for coursework? (OS, rough RAM, whether you can install software — e.g. \"MacBook Air M1, 8 GB, yes\")",
  },
];
