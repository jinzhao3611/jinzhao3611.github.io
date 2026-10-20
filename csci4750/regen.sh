#!/bin/bash
# Regenerate the CSCI 4750/5750 course-site pages from the course markdown.
#
# Source of truth: the md files in the course folder (SRC below). This script
# converts them with pandoc, wraps them in the shared nav/footer shell, and
# adapts a few instructor-facing notes for the public pages — the local md
# files are never modified. Same pipeline as ../csci4845/regen.sh.
#
# Pages built: schedule, assignments, project, syllabus-4750, syllabus-5750.
# NOT built: index.html (course home) — that page is maintained by hand.
#
# Usage:  ./regen.sh    then review with `git diff`, commit, and push.

set -euo pipefail
SRC="${SRC:-$HOME/Desktop/CSCI_4750_ml}"
OUT="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# --- syllabi: link to the live pages instead of naming local files ---
for num in 4750 5750; do
  sed -e '3,6s/$/  /' \
      -e 's/`assignments\.md`/[the assignments page](assignments.html)/g' \
      -e 's/`project\.md`/[the project page](project.html)/g' \
      -e 's/`schedule\.md`/[the class schedule](schedule.html)/g' \
      -e 's/Suggested letter scale/Letter scale/' \
      -e 's/ (Adjust to department norms\.)//' \
      "$SRC/syllabus_${num}.md" > "$TMP/syllabus_${num}.md"
  pandoc "$TMP/syllabus_${num}.md" -f markdown -t html -o "$TMP/body_${num}.html"
done

# --- schedule: drop instructor-facing asides ---
perl -0pe 's/Verified against the official SLU 2026–27 academic calendar \(published July 29, 2025\) and\nthe registrar.s final-exam table \(.*?\):/Key dates per the official SLU 2026–27 academic calendar and the registrar\x27s final-exam table:/s;
           s/ Materials in `lectures\/project-studio\/`\./ The worksheet is handed out in class./;
           s/## Topics deliberately compressed \(state this on day 1\)/## Topics deliberately compressed/' \
  "$SRC/schedule.md" > "$TMP/schedule.md"
pandoc "$TMP/schedule.md" -f markdown -t html -o "$TMP/body_schedule.html"

# --- assignments: student-facing as written ---
pandoc "$SRC/assignments.md" -f markdown -t html -o "$TMP/body_assignments.html"

# --- project: swap the instructor file map for a Canvas pointer ---
# project.md indexes the per-deliverable handouts by repo path; students cannot open
# those, so the table and the studio-materials path become Canvas references here.
perl -0pe 's/Per-deliverable instructions \(Canvas-ready, in `project\/`\):\n\n\| Deliverable \| File \|\n.*?\n\n/Detailed instructions for each deliverable — team declaration, proposal, milestone\ncheck-in, presentation, and final report — are posted on Canvas.\n\n/s;
           s/The Mar 1 \*\*project studio\*\* materials \(workshop plan, student worksheet, deck\) live in\n`lectures\/project-studio\/`\./The Mar 1 **project studio** runs in class; the worksheet is handed out that day./s;
           s/\n<!-- Compute resources.*?-->\n//s' \
  "$SRC/project.md" > "$TMP/project.md"
pandoc "$TMP/project.md" -f markdown -t html -o "$TMP/body_project.html"

# --- guard: nothing instructor-facing may survive into the public pages ---
if grep -l -E '`(lectures|project|hw[0-9]|exams)/|\.md`|state this on day|Adjust to department|Verified against' \
     "$TMP"/body_*.html; then
  echo "regen.sh: an instructor-facing note survived (file above) — update the substitutions" >&2
  exit 1
fi

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
    <span class="brand">CSCI 4750/5750 · ML · Spring 2027</span>
$(nav_link index.html "Course Home" home "$active")
$(nav_link schedule.html "Schedule" schedule "$active")
$(nav_link assignments.html "Assignments" assignments "$active")
$(nav_link project.html "Project" project "$active")
$(nav_link syllabus-4750.html "Syllabus (4750 UG)" s4750 "$active")
$(nav_link syllabus-5750.html "Syllabus (5750 Grad)" s5750 "$active")
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
  <div class="wrap">${footer_label} · Machine Learning · Saint Louis University ·
  Spring 2027 · <a href="https://jinzhao3611.github.io/">Jin Zhao</a></div>
</footer>

</body>
</html>
EOF
  } > "$outfile"
}

make_page "$OUT/schedule.html" "Schedule — CSCI 4750/5750 Machine Learning · Spring 2027" \
  "$TMP/body_schedule.html" schedule "CSCI 4750/5750" ""
make_page "$OUT/assignments.html" "Assignments — CSCI 4750/5750 Machine Learning · Spring 2027" \
  "$TMP/body_assignments.html" assignments "CSCI 4750/5750" ""
make_page "$OUT/project.html" "Final Project — CSCI 4750/5750 Machine Learning · Spring 2027" \
  "$TMP/body_project.html" project "CSCI 4750/5750" ""
make_page "$OUT/syllabus-4750.html" "CSCI 4750 Syllabus — Machine Learning · Spring 2027" \
  "$TMP/body_4750.html" s4750 "CSCI 4750" \
  '<div class="notice">This is the <strong>undergraduate</strong> (CSCI 4750) syllabus.
Graduate students: see the <a href="syllabus-5750.html">CSCI 5750 syllabus</a>.</div>'
make_page "$OUT/syllabus-5750.html" "CSCI 5750 Syllabus — Introduction to Machine Learning · Spring 2027" \
  "$TMP/body_5750.html" s5750 "CSCI 5750" \
  '<div class="notice">This is the <strong>graduate</strong> (CSCI 5750) syllabus.
Undergraduate students: see the <a href="syllabus-4750.html">CSCI 4750 syllabus</a>.</div>'

echo "Regenerated 5 pages into $OUT"
