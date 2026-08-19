#!/bin/bash
# Regenerate the CSCI 4845/5845 course-site pages from the course markdown.
#
# Source of truth: the md files in the course repo (SRC below). This script
# converts them with pandoc, wraps them in the shared nav/footer shell, and
# adapts a few instructor-facing notes for the public pages — the local md
# files are never modified.
#
# Pages built: schedule, assignments, project, syllabus-4845, syllabus-5845.
# NOT built: index.html (course home) — that page is maintained by hand.
#
# Usage:  ./regen.sh    then review with `git diff`, commit, and push.

set -euo pipefail
SRC="${SRC:-$HOME/Documents/slu/2026_fall/teaching/CSCI_4845_nlp}"
OUT="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# --- syllabi: link to the live pages instead of naming local files ---
for num in 4845 5845; do
  sed -e '3,6s/$/  /' \
      -e 's/`assignments\.md`/[the assignments page](assignments.html)/g' \
      -e 's/`project\.md`/[the project page](project.html)/g' \
      -e 's/`schedule\.md`/[the class schedule](schedule.html)/g' \
      -e 's/; see open-decisions list)/)/' \
      -e 's/Suggested letter scale/Letter scale/' \
      -e 's/ (Adjust to department norms\.)//' \
      -e 's/ — verify against the current release[^)]*//' \
      "$SRC/syllabus_${num}.md" > "$TMP/syllabus_${num}.md"
  pandoc "$TMP/syllabus_${num}.md" -f markdown -t html -o "$TMP/body_${num}.html"
done

# --- schedule: drop instructor-facing asides ---
sed -e 's/Verified against the official SLU 2026–27 academic calendar (published July 29, 2025):/Key dates per the official SLU 2026–27 academic calendar:/' \
    -e 's/ (re-check numbering against the current release)//' \
    -e 's/## Topics deliberately compressed (state this on day 1)/## Topics deliberately compressed/' \
    "$SRC/schedule.md" > "$TMP/schedule.md"
pandoc "$TMP/schedule.md" -f markdown -t html -o "$TMP/body_schedule.html"

# --- assignments: strip instructor-facing notes ---
perl -0pe 's/\(students always love watching a trigram\s+model babble — save the outputs, they return as a punchline in Unit 3\)/(save your samples — they return as a punchline in Unit 3)/s;
           s/- Starter code: one GitHub repo per assignment \(template notebooks \+ unit tests\)\. Build these.*?to build and test starters\./- Starter code: one GitHub repo per assignment (template notebooks + unit tests), linked from Canvas./s' \
  "$SRC/assignments.md" > "$TMP/assignments.md"
pandoc "$TMP/assignments.md" -f markdown -t html -o "$TMP/body_assignments.html"

# --- project: student-ready as-is ---
pandoc "$SRC/project.md" -f markdown -t html -o "$TMP/body_project.html"

# --- shared page shell ---
nav_link() { if [ "$3" = "$4" ]; then echo "    <a href=\"$1\" class=\"active\">$2</a>"; else echo "    <a href=\"$1\">$2</a>"; fi; }

make_page() { # outfile title bodyfile active footer_label banner
  outfile="$1"; title="$2"; bodyfile="$3"; active="$4"; footer_label="$5"; banner="$6"
  {
    cat <<EOF
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<link rel="stylesheet" href="course.css">
</head>
<body>

<nav class="topnav">
  <div class="wrap">
    <span class="brand">CSCI 4845/5845 · NLP · Fall 2026</span>
$(nav_link index.html "Course Home" home "$active")
$(nav_link schedule.html "Schedule" schedule "$active")
$(nav_link assignments.html "Assignments" assignments "$active")
$(nav_link project.html "Project" project "$active")
$(nav_link syllabus-4845.html "Syllabus (4845 UG)" s4845 "$active")
$(nav_link syllabus-5845.html "Syllabus (5845 Grad)" s5845 "$active")
    <a href="https://jinzhao3611.github.io/">Instructor</a>
  </div>
</nav>

<main class="wrap">
EOF
    [ -n "$banner" ] && echo "$banner"
    cat "$bodyfile"
    cat <<EOF
</main>

<footer>
  <div class="wrap">${footer_label} · Natural Language Processing · Saint Louis University ·
  Fall 2026 · <a href="https://jinzhao3611.github.io/">Jin Zhao</a></div>
</footer>

</body>
</html>
EOF
  } > "$outfile"
}

make_page "$OUT/schedule.html" "Schedule — CSCI 4845/5845 Natural Language Processing · Fall 2026" \
  "$TMP/body_schedule.html" schedule "CSCI 4845/5845" ""
make_page "$OUT/assignments.html" "Assignments — CSCI 4845/5845 Natural Language Processing · Fall 2026" \
  "$TMP/body_assignments.html" assignments "CSCI 4845/5845" ""
make_page "$OUT/project.html" "Final Project — CSCI 4845/5845 Natural Language Processing · Fall 2026" \
  "$TMP/body_project.html" project "CSCI 4845/5845" ""
make_page "$OUT/syllabus-4845.html" "CSCI 4845 Syllabus — Natural Language Processing · Fall 2026" \
  "$TMP/body_4845.html" s4845 "CSCI 4845" \
  '<div class="notice">This is the <strong>undergraduate</strong> (CSCI 4845) syllabus.
Graduate students: see the <a href="syllabus-5845.html">CSCI 5845 syllabus</a>.</div>'
make_page "$OUT/syllabus-5845.html" "CSCI 5845 Syllabus — Natural Language Processing · Fall 2026" \
  "$TMP/body_5845.html" s5845 "CSCI 5845" \
  '<div class="notice">This is the <strong>graduate</strong> (CSCI 5845) syllabus.
Undergraduate students: see the <a href="syllabus-4845.html">CSCI 4845 syllabus</a>.</div>'

echo "Regenerated 5 pages into $OUT"
