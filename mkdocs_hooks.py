"""Build-time fixes that would otherwise cost a pinned plugin dependency.

MkDocs derives a sidebar *section* label from the folder name on disk, so
`01_Foundations_of_American_Democracy/` would read as "01 Foundations Of
American Democracy" and `common_sense/` as "Common Sense" only by luck. The
numeric prefix sets reading order in a file listing; it should not be visible
in the nav, and this subject's names ("Shays' Rebellion", "Articles of
Confederation") have a fixed casing no naive title-caser gets right.

Two jobs:

1. **Clean section labels** — unit folders get their College Board names, topic
   folders get title-cased names with overrides.
2. **Order the root nav** — ``NAV_ORDER`` pins the reading order of the
   top-level entries; anything unlisted keeps its alphabetical slot after them.

Note for anyone editing: ``on_nav`` receives a ``Navigation``, whose children
live on ``.items`` — only a ``Section`` has ``.children``. A hook that reaches
for ``.children`` at the top level does nothing at all and the build still
succeeds, so the sidebar is simply never touched.
"""

from __future__ import annotations

import posixpath
import re

# Unit folders → the label the AP course itself uses.
SECTION_LABELS = {
    "00_Class_Notes": "Class notes (as taken)",
    "01_Foundations_of_American_Democracy": "Unit 1 · Foundations of American Democracy",
    "02_Interactions_Among_Branches_of_Government": "Unit 2 · Interactions Among Branches of Government",
    "03_Civil_Liberties_and_Civil_Rights": "Unit 3 · Civil Liberties and Civil Rights",
    "04_American_Political_Ideologies_and_Beliefs": "Unit 4 · American Political Ideologies and Beliefs",
    "05_Political_Participation": "Unit 5 · Political Participation",
}

# Whole-folder-name overrides for topic slugs the word-level pass can't fix.
NAME_OVERRIDES = {
    "shays_rebellion": "Shays' Rebellion",
    "common_sense": "Common Sense",
    "road_to_independence": "The Road to Independence",
    "first_continental_congress": "The First Continental Congress",
    "declaration_of_independence": "The Declaration of Independence",
    "articles_of_confederation": "The Articles of Confederation",
    "01_declaring_independence": "08/26 · Declaring Independence",
    "02_classifications_and_the_articles": "08/27 · Government & the Articles",
    "03_democracy_and_ideals": "Democracy & the Ideals",
}

# Word-level casing fixes applied after a naive title-case.
FIXUPS = {
    "And": "and",
    "Of": "of",
    "Vs": "vs",
    "In": "in",
    "The": "the",
    "To": "to",
    "A": "a",
}

# Reading order of the root nav, by on-disk name. Unlisted entries sort
# alphabetically after these.
NAV_ORDER = [
    "index.md",
    "CORRECTIONS.md",
    "GLOSSARY.md",
    "FOUNDING_DOCUMENTS.md",
    "00_Class_Notes",
    "01_Foundations_of_American_Democracy",
    "02_Interactions_Among_Branches_of_Government",
    "03_Civil_Liberties_and_Civil_Rights",
    "04_American_Political_Ideologies_and_Beliefs",
    "05_Political_Participation",
]

# Reading order INSIDE a section, keyed by the section's folder path and listing
# children by on-disk name. Auto-nav is alphabetical, which for a lesson
# sequence is actively wrong — Unit 1 would open on "Articles of
# Confederation" and reach the Declaration fourth.
#
# Set the order here, NEVER by renaming folders to 01_, 02_ …: a folder name is
# a permanent URL, and inserting one lesson later would move a whole run of
# them. A folder's own README.md is always pinned first (navigation.indexes
# needs the index at children[0]); unlisted children keep their alphabetical
# slot after the listed ones.
SECTION_ORDER = {
    "01_Foundations_of_American_Democracy": [
        "road_to_independence",
        "first_continental_congress",
        "common_sense",
        "declaration_of_independence",
        "ideals_of_democracy",
        "types_of_democracy",
        "models_of_democracy",
        "classifications_of_government",
        "articles_of_confederation",
        "shays_rebellion",
    ],
}


def _pretty(name: str) -> str:
    if name in SECTION_LABELS:
        return SECTION_LABELS[name]
    if name in NAME_OVERRIDES:
        return NAME_OVERRIDES[name]
    name = re.sub(r"^\d+_", "", name)
    words = [w.capitalize() for w in name.split("_")]
    # Never lowercase the first word, however small it is.
    words = [words[0]] + [FIXUPS.get(w, w) for w in words[1:]]
    return " ".join(words)


def _dir_of(item) -> str:
    """TOP-LEVEL on-disk name of a nav item — used only for root nav ordering."""
    if hasattr(item, "file") and item.file is not None:
        return item.file.src_path.split("/")[0]
    for child in getattr(item, "children", None) or []:
        got = _dir_of(child)
        if got:
            return got
    return ""


def _first_src(item) -> str:
    """src_path of the first descendant page of a nav item."""
    if hasattr(item, "file") and item.file is not None:
        return item.file.src_path
    for child in getattr(item, "children", None) or []:
        got = _first_src(child)
        if got:
            return got
    return ""


def _relabel(items, depth: int = 0) -> None:
    # A section's own folder is the DEPTH-th segment of any descendant page's
    # path — labeling from segment 0 at every level is how every topic entry
    # inside a unit would otherwise read as the unit's own name.
    for item in items:
        if getattr(item, "is_section", False):
            parts = _first_src(item).split("/")
            if depth < len(parts) - 1:
                name = parts[depth]
                item.title = _pretty(name)
                _order_children(item, name, depth + 1)
            _relabel(item.children, depth + 1)


def _order_children(section, folder: str, child_depth: int) -> None:
    """Apply SECTION_ORDER to one section's children, index page first."""
    wanted = SECTION_ORDER.get(folder)
    if not wanted:
        return
    rank = {name: i for i, name in enumerate(wanted)}

    def key(child):
        parts = _first_src(child).split("/")
        # The section's own README is the only child with no folder of its own
        # at this depth; navigation.indexes needs it at children[0].
        if child_depth >= len(parts) - 1:
            return (-1, "")
        name = parts[child_depth]
        return (rank.get(name, len(rank)), name)

    section.children.sort(key=key)


def on_nav(nav, config, files):
    _relabel(nav.items)
    order = {name: i for i, name in enumerate(NAV_ORDER)}
    nav.items.sort(key=lambda it: (order.get(_dir_of(it), len(order)), _dir_of(it)))
    return nav


def on_page_markdown(markdown, page, config, files):
    """Retarget links to the repo-root README at the site's homepage.

    The root README.md is excluded from the build (index.md inlines it), so a
    unit page's "← All units" link to ``../README.md`` would 404 on the site
    while working fine on GitHub. Rewriting at build time keeps the source
    authored for GitHub's file-relative rendering — links to any *folder's*
    README are left alone.
    """
    src_dir = posixpath.dirname(page.file.src_path)

    def repl(m):
        href = m.group(2)
        if posixpath.normpath(posixpath.join(src_dir, href)) == "README.md":
            return m.group(1) + href[: -len("README.md")] + "index.md" + m.group(3)
        return m.group(0)

    return re.sub(r"(\]\()([^)\s#]*README\.md)([#)])", repl, markdown)
