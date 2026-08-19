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

## Running it in class (start-of-class question set)

1. Open `present.html` on the projector and sign in. The QR code and join URL
   are in the left sidebar — leave them up while students join.
2. Pick today's set in the **Question set** dropdown and click **Open set —
   students self-pace**. Students get Back/Next buttons and work through the
   whole set on their own devices; click any question in the sidebar to project
   its live distribution while they answer.
3. Watch the counter (`N answered`) climb. Results update live for you and for
   any student who has answered that question.
4. After ~5 minutes, click **Close set** — student devices return to "waiting"
   and class begins. You can still pose single questions mid-lecture: with the
   set closed, click a question to make it live for everyone at once, and
   **Hide question (blank screen)** to clear it.
5. For grading and attendance:
   - **Export responses CSV** — one row per answer (timestamp, set, question,
     name, email, answer).
   - **Export attendance CSV** — one row per student per set (name, email,
     questions answered out of the set, first/last answer timestamps). This is
     the per-session attendance sheet.

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

Copy `questions-lec01.js` to `questions-lec02.js`, edit the questions, import
it in `present.html` next to the `LEC01` import, and seed it the same way.
Sets are grouped by the id prefix (`lec02-q1` → set `lec02`), so keep ids in
that pattern. Each question is:

```js
{ id: "lec07-q1", order: 1, type: "mc",     // unique id; order = position in set
  prompt: "…", choices: ["…", "…"] }        // choices only for type "mc"
{ id: "lec07-q2", order: 2, type: "text",   // free response
  prompt: "…" }
```

`quizzes/quiz-bank.md` in the course repo holds 50 written MCQs with rationales —
a ready supply of in-class questions for the rest of the semester.
