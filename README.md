# AP U.S. Government — Learning Library

Class notes from **AP U.S. Government and Politics**, kept in three layers:

1. **The notes as taken** — transcribed from the notebook, word for word, slips and all. Your own words, searchable.
2. **The corrections** — every factual slip found in those notes, with what is actually true and why it matters on an exam.
3. **The expansions** — one page per topic, going well past the notes: the mechanism, the dates, the required founding documents, and how the College Board frames it.

**Browse the site:** <https://masiarek.github.io/gov-learning-library/> · **Every correction in one place:** [CORRECTIONS.md](CORRECTIONS.md) · **A–Z of terms:** [GLOSSARY.md](GLOSSARY.md) · **The nine required documents:** [FOUNDING_DOCUMENTS.md](FOUNDING_DOCUMENTS.md)

## The five units

The AP course is five units. Everything covered so far lands in Unit 1.

| Unit | Status |
|---|---|
| [Class notes (as taken)](00_Class_Notes/README.md) | 3 class days transcribed |
| [Unit 1 · Foundations of American Democracy](01_Foundations_of_American_Democracy/README.md) | **10 topic pages written** |
| [Unit 2 · Interactions Among Branches of Government](02_Interactions_Among_Branches_of_Government/README.md) | Not started |
| [Unit 3 · Civil Liberties and Civil Rights](03_Civil_Liberties_and_Civil_Rights/README.md) | Not started |
| [Unit 4 · American Political Ideologies and Beliefs](04_American_Political_Ideologies_and_Beliefs/README.md) | Not started |
| [Unit 5 · Political Participation](05_Political_Participation/README.md) | Not started |

## How each topic page works

Every page in Unit 1 has the same five parts:

1. **One line** — the whole idea in a sentence, for the night before a test.
2. **A five-row table** — definition, how it works, an example, why it matters, and the **common mistake** people make. The common-mistake row is the one worth reading twice; it is usually the difference between a 2 and a 3 on a free-response question.
3. **From the class notes** — the relevant lines of the notebook, quoted, so the page connects to what was actually said in class.
4. **Corrections**, when the notes got something wrong — what they say, what is true, and why the distinction matters.
5. **The full picture** — the expansion: dates, people, mechanism, and the argument historians or the College Board actually care about. Then **Where it sits in AP**, naming the course topic number.

## Two conventions worth knowing

**The notes are transcribed, not cleaned up.** [00_Class_Notes](00_Class_Notes/README.md) preserves the notebook as written, because a study page you cannot match to your own handwriting is a study page you will not trust. Wrong lines there carry a **⚠** marker pointing at the correction — they are never silently fixed in place.

**This library is in English only**, unlike its [biology sibling](https://github.com/masiarek/biology-learning-library), which is bilingual EN/PL. The reason is the subject: biology vocabulary maps onto a real Polish curriculum term for term, so a Polish column teaches something. American government does not — the terms are proper nouns and doctrines from one country's constitutional tradition, the exam is written and answered in English, and precise English wording *is* the skill being graded. A Polish column here would be invented prose with nothing to check it against.

## Where the material comes from

The unit and topic numbering follows the College Board's **AP United States Government and Politics Course and Exam Description**. The notes are from a Wake County, NC classroom; the textbook on the shelf is AMSCO's *AP United States Government and Politics*. Everything written here is written from scratch for this library — a study companion, not a copy of any classroom or published material.

## Local preview

```bash
uv run --group docs mkdocs serve
```

The docs toolchain is pinned in `pyproject.toml` (`docs` dependency group) + `uv.lock`; the site deploys automatically from `.github/workflows/docs.yml` on every push to master. CI builds with `--strict`, which is the broken-link gate: a link to a page that does not exist fails the build. Unit stubs therefore name their future topics in **plain text** and link nothing unwritten — keep it that way rather than dropping `--strict` to get a build green.
