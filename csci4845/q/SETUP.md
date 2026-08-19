# In-class questions — setup & run guide

Live polling for CSCI 4845/5845. Students answer on their phones; the answer
distribution (multiple choice) or a wall of anonymous responses (free text)
appears on the projector in real time.

- **Students:** `https://jinzhao3611.github.io/csci4845/q/`
- **Presenter (you):** `https://jinzhao3611.github.io/csci4845/q/present.html`

Hosting is GitHub Pages (already yours); the live data layer is Firebase
Firestore, whose free Spark tier is far above what 31 students generate.

---

## One-time setup (~10 minutes)

1. **Create the project.** <https://console.firebase.google.com> → *Add project*
   → name it e.g. `csci4845-poll`. Google Analytics: **disable** (not needed).

2. **Create the database.** Build → *Firestore Database* → *Create database* →
   **Production mode** → pick the `nam5` (US) location.

3. **Publish the security rules.** Firestore → *Rules* tab → replace the contents
   with `firestore.rules` from this folder → *Publish*. These rules let any
   signed-in student read results and write **only their own** answer, and let
   only your email create questions or change which question is live.

4. **Enable sign-in.** Build → *Authentication* → *Get started* → *Sign-in
   method* → enable **Anonymous** (students) and **Google** (you).

5. **Paste the config.** Project settings (gear icon) → *Your apps* → click the
   `</>` (Web) icon → register an app (nickname anything, no Hosting needed) →
   copy the `firebaseConfig` object → paste the values into
   `firebase-config.js` in this folder, replacing every `PASTE_ME`.

6. **Authorize the domain.** Authentication → *Settings* → *Authorized domains*
   → *Add domain* → `jinzhao3611.github.io`.

7. **Commit and push** the edited `firebase-config.js`. (These keys are meant to
   be public — Firebase web config is an identifier, not a secret. Access is
   controlled by the rules in step 3, which is why step 3 matters.)

8. **Seed the questions.** Open `present.html`, sign in with your SLU Google
   account, click **Seed Lecture 1 set**. The five Lecture 1 questions appear in
   the sidebar.

---

## Running it in class

1. Open `present.html` on the projector and sign in. The QR code and join URL
   are in the left sidebar — leave them up while students join.
2. Click a question in the sidebar to put it live. Students' phones switch to it
   automatically; no refresh needed.
3. Watch the counter (`N answered`) climb. Results update live for you and for
   any student who has already answered.
4. Click **Hide question (blank screen)** to clear the screen while you lecture,
   or click the next question when you're ready.
5. **Student-paced browsing** (toggle in the sidebar): when ON, students get
   Back/Next buttons and move through the whole question set at their own speed —
   ideal for the Lecture 1 intake survey. Leave it OFF for mid-lecture questions
   so answers aren't visible ahead of your reveal. Your projected screen always
   shows whichever question you clicked, in either mode.
6. After class (or at end of term), click **Export responses CSV** for grading —
   one row per response with timestamp, question, name, email, and answer.

### Notes

- **Students identify themselves once** with name + SLU email, stored in their
  browser, so later classes are one tap. Answers are recorded per student for
  participation credit; free-text answers are shown on screen **without names**.
- **Changing an answer** is allowed while a question is live — a student's
  document is overwritten, never duplicated.
- **Late joiners** see whatever question is currently live, so a student who
  arrives mid-question can still answer.
- Results are only shown to a student **after** they answer, so the distribution
  doesn't anchor their choice.

## Adding questions for later lectures

Either write them from the presenter console, or copy
`questions-lec01.js` to `questions-lec02.js`, edit, and import it in
`present.html` next to the `LEC01` import. Each question is:

```js
{ id: "lec07-q1", order: 1, type: "mc",     // unique id; order = sidebar position
  prompt: "…", choices: ["…", "…"] }        // choices only for type "mc"
{ id: "lec07-q2", order: 2, type: "text",   // free response
  prompt: "…" }
```

`quizzes/quiz-bank.md` in the course repo holds 50 written MCQs with rationales —
a ready supply of in-class questions for the rest of the semester.
