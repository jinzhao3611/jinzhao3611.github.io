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

8. **Add the questions.** Open `present.html`, sign in, click **Add question
   set…**, paste a set (format below), and click **Add set**. (The Lecture 1
   intake set is already uploaded.)

---

## Running it in class

1. Once per lecture: open `present.html`, sign in, pick the day's set in the
   dropdown, and click **Make "lecNN" live for students**. The set stays live
   until you make the next one live — there is nothing to close — and each
   student gets **one submission per question** (no changes after submitting).
2. Leave the presenter page on the projector during the first ~5 minutes: it
   shows **every question in the set** with its live distribution or response
   wall, all updating in real time, next to the QR code students scan.
3. Students work through the set at their own pace with Back/Next on their
   phones; each student's page starts at their first unanswered question.
4. For grading and attendance: **Export responses CSV** — one row per answer
   with timestamp, set, question, name, email, and answer. Attendance per
   session = the distinct emails for that set (a pivot table by email × set,
   or ask Claude to tally participation with the drop-4 rule at term's end);
   out-of-class submissions are visible by their timestamps.

### Notes

- **Students identify themselves once** with name + SLU email, stored in their
  browser, so later classes are one tap. Answers are recorded per student for
  participation credit; free-text answers are shown on screen **without names**.
- **One submission per question**, enforced by the database rules — after
  submitting, an answer is locked; the student sees it alongside the live
  results. (A mis-tap is protected by an explicit Submit button.)
- **Late joiners** can still answer — the set stays open; the exports'
  timestamps show who answered when.
- **Results appear only on the presenter/projector screen** — student devices
  never show the distribution, and the database rules only let each student
  read their own responses.

## Adding questions for later lectures

Click **Add question set…** in the presenter sidebar, paste the set in this
format, and click **Add set** — no code changes or deploys needed:

```
set: lec02
mc: Which smoothing method backs off to lower-order n-grams?
- Laplace
- Kneser-Ney
- Stupid backoff
text: One thing from Tuesday that's still unclear?
```

Ids and order are automatic (`lec02-q1`, `lec02-q2`, … top to bottom).
Re-adding a set name overwrites its questions — fine for fixing typos, but
don't reorder MC choices after students have answered (answers store the
choice index), and if you shrink a set, delete the leftover question docs in
the Firebase console (Firestore → Data → questions).

`quizzes/quiz-bank.md` in the course repo holds 50 written MCQs with rationales —
a ready supply of in-class questions for the rest of the semester.
