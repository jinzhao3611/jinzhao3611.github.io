// Lecture 1 question set — record of what is uploaded to Firestore.
// Rewritten Aug 2026 (v2): lighter icebreaker set replaces the folded-in HW0
// background survey. Not imported by the app: sets are added by pasting them
// into the presenter's "Add question set…" box (see SETUP.md — the paste
// format supports "mc:", "multi:", "text:", and "note:" lines).
// The previous version had 12 questions; re-adding "lec01" overwrites q1–q7
// but leaves lec01-q8…q12 in Firestore — delete those docs in the console
// (Firestore → Data → questions) if the old set was ever uploaded.

export const LEC01 = [
  {
    id: "lec01-q1", order: 1, type: "mc", set: "lec01",
    prompt: "What brought you to NLP?",
    choices: [
      "LLMs are everywhere, and I want to know what is under the hood.",
      "I want to build useful language technology.",
      "I may want to do AI/NLP research.",
      "I want skills for an industry job.",
      "I am interested in human language or linguistics.",
      "It fit my schedule, but I am open to being converted.",
      "I am still exploring and genuinely do not know yet.",
      "Something else.",
    ],
  },
  {
    id: "lec01-q2", order: 2, type: "mc", set: "lec01",
    prompt: "How often do you use AI assistants (ChatGPT, Claude, Copilot, …)?",
    choices: [
      "All the time, I am addicted",
      "Daily",
      "A few times a week",
      "Occasionally",
      "Rarely",
      "Never",
    ],
  },
  {
    id: "lec01-q3", order: 3, type: "mc", set: "lec01",
    prompt: "Machine learning and I are currently…",
    choices: [
      "Close friends—we have built things together.",
      "On speaking terms—I remember most of the basics.",
      "We met before, but some of the weights have decayed.",
      "It is complicated.",
      "We have not really been introduced yet.",
    ],
  },
  {
    id: "lec01-q4", order: 4, type: "multi", set: "lec01",
    prompt: "Which of these have you actually used to make something?",
    choices: [
      "Python or Jupyter",
      "scikit-learn",
      "PyTorch or TensorFlow",
      "Hugging Face",
      "Git/GitHub or the command line",
      "I have successfully run a mysterious notebook.",
      "None of these yet",
    ],
  },
  {
    id: "lec01-q5", order: 5, type: "mc", set: "lec01",
    prompt: "Which NLP task is your favorite or most interesting to you?",
    choices: [
      "Text Classification",
      "Sentiment Analysis",
      "Named Entity Recognition (NER)",
      "Machine Translation",
      "Text Summarization",
      "Question Answering",
      "Information Extraction",
      "Topic Modeling",
      "Text Generation",
      "Chatbots / Conversational AI",
      "Spam Detection",
      "Intent Classification",
      "Semantic Similarity",
      "Natural Language Inference (NLI)",
      "Part-of-Speech (POS) Tagging",
      "Language Modeling",
      "Retrieval-Augmented Generation (RAG)",
      "Fake News / Misinformation Detection",
      "Emotion Detection",
      "Speech-to-Text / Automatic Speech Recognition (ASR)",
      "Other",
    ],
  },
  {
    id: "lec01-q6", order: 6, type: "text", set: "lec01",
    prompt: "What human languages or dialects live in your brain?",
    note: "List languages or dialects that you speak, sign, read, understand, or are currently learning. Separate them with commas. Python does not count for this question.",
  },
  {
    id: "lec01-q7", order: 7, type: "text", set: "lec01",
    prompt: "Anything else about NLP you want to say?",
  },
];
