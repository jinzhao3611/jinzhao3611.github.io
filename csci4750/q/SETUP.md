# In-class questions — setup & run guide

Live polling for CSCI 4750/5750. Students answer on their phones; the answer
distribution (multiple choice) or a wall of anonymous responses (free text)
appears on the projector in real time. Same app as CSCI 4845/5845.

- **Students:** `https://jinzhao3611.github.io/csci4750/q/`
- **Presenter (you):** `https://jinzhao3611.github.io/csci4750/q/present.html`

Hosting is GitHub Pages; the live data layer is Firebase Firestore.

---

## Setup: already done

This course reuses the Firebase project created for CSCI 4845/5845
(`csci4845-poll`). `firebase-config.js` here differs from the NLP copy only in
`COURSE = "csci4750-s27"` and the student URL. Every Firestore document lives
under `courses/{COURSE}/`, so this course's questions, live state, and responses
are separate from the NLP course's, and the published rules (`firestore.rules`,
identical to the NLP copy) already cover it. The domain `jinzhao3611.github.io`
is already authorized. Nothing to do in the Firebase console.

If you ever want a separate project instead, follow the one-time steps in
`../../csci4845/q/SETUP.md` and paste the new values into `firebase-config.js`.

**Before the first class (Mon Jan 11):** open `present.html`, sign in with
Google, click **Add question set…**, paste the contents of
`lectures/lecture01/CSCI-4750-2027-Lecture-01-Questions.txt` from the course
folder (the background survey), and click **Add set**. Do the same for the
other lectures whenever convenient — every lecture folder has a
`...-Questions.txt` paste file (`set: lec02` … `set: lec38`, plus `set: studio`
for the Mar 1 project studio).

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
   session = the distinct emails for that set. This course allows **up to 6
   missed sessions** without penalty (42 meetings).

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

## Paste format

```
set: lec02
mc: Which k gives the smoothest k-NN decision boundary?
- k = 1
- k = 5
- k = 50
note: Think about how many points vote.
multi: Which of these have you used? (select all that apply)
- NumPy
- scikit-learn
text: One thing from Monday that is still unclear?
```

`mc:` is single choice, `multi:` is select-all-that-apply (both take `- choice`
lines), `text:` is free text. An optional `note:` line right after a question
adds a small hint under its prompt. A line with no prefix continues the
previous line. Ids and order are automatic (`lec02-q1`, `lec02-q2`, … top to
bottom). Re-adding a set name overwrites its questions — fine for fixing typos,
but don't reorder MC choices after students have answered (answers store the
choice index), and if you shrink a set, delete the leftover question docs in
the Firebase console (Firestore → Data → courses → csci4750-s27 → questions).

The answers to each set are in the instructor-only
`...-Question-Key.md` next to it in the course folder — never paste those.
