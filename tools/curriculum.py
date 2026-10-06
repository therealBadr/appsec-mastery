#!/usr/bin/env python3
"""Curriculum tooling for this repo. Python 3.8+, standard library only.

  python tools/curriculum.py init [--force]   one-time import of the 42 subject HTML files (archive/subjects-html/)
                                              as Markdown chapters under docs/. After the import, the Markdown is
                                              the source of truth: existing files are never overwritten without --force.
  python tools/curriculum.py refresh          refresh everything that is derived from what is actually published:
                                              the status tables (docs/roadmap.md, README.md), each chapter's status
                                              block, and the navigation in mkdocs.yml. CI runs this before building.

A chapter's status is derived, not hand-maintained:
  complete  -> `status: complete` in the chapter's index.md front matter (you set this when you have finished it)
  writing   -> at least one published lesson (docs/<stage>/<NN-subject>/lessons/NN-*.md) or solution page
  planned   -> otherwise
Files whose name starts with "_" are drafts: they stay in the repo but are not published or counted.
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
DOCS = ROOT / "docs"
ARCHIVE = ROOT / "archive" / "subjects-html"
CUR = json.loads((TOOLS / "curriculum.json").read_text(encoding="utf-8"))
INDENT = "    "


# ------------------------------------------------------------------ mini HTML DOM
class Node:
    __slots__ = ("tag", "attrs", "kids", "parent")

    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.kids, self.parent = tag, attrs, [], parent

    @property
    def classes(self):
        return set((self.attrs.get("class") or "").split())


class _Builder(HTMLParser):
    VOID = {"meta", "link", "br", "hr", "img", "input"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root", {}, None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, dict(attrs), self.cur)
        self.cur.kids.append(n)
        if tag not in self.VOID:
            self.cur = n

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.kids.append(data)


def parse_html(path):
    b = _Builder()
    b.feed(Path(path).read_text(encoding="utf-8"))
    return b.root


def walk(n):
    for k in n.kids:
        if isinstance(k, Node):
            yield k
            yield from walk(k)


def find_all(n, tag=None, cls=None):
    return [x for x in walk(n) if (tag is None or x.tag == tag) and (cls is None or cls in x.classes)]


def find_one(n, tag=None, cls=None):
    r = find_all(n, tag, cls)
    return r[0] if r else None


def direct(n, tag=None):
    return [k for k in n.kids if isinstance(k, Node) and (tag is None or k.tag == tag)]


def raw_text(n):
    out = []
    for k in n.kids:
        out.append(k if isinstance(k, str) else raw_text(k))
    return "".join(out)


# ------------------------------------------------------------- HTML -> Markdown
def esc(s):
    s = s.replace("\\", "\\\\").replace("*", "\\*").replace("<", "&lt;").replace(">", "&gt;")
    return s


def wrap(marker, text):
    m = re.match(r"(\s*)(.*?)(\s*)$", text, re.S)
    if not m or not m.group(2):
        return text
    return f"{m.group(1)}{marker}{m.group(2)}{marker}{m.group(3)}"


def inline(n, skip=()):
    out = []
    for k in n.kids:
        if isinstance(k, str):
            out.append(esc(k))
        elif k.tag in skip or k.tag in ("style", "script"):
            continue
        elif k.tag == "code":
            t = re.sub(r"\s+", " ", raw_text(k)).strip()
            out.append(f"`` {t} ``" if "`" in t else f"`{t}`")
        elif k.tag in ("strong", "b"):
            out.append(wrap("**", inline(k, skip)))
        elif k.tag in ("em", "i"):
            out.append(wrap("*", inline(k, skip)))
        elif k.tag == "a":
            out.append(f"[{inline(k, skip).strip()}]({k.attrs.get('href', '')})")
        else:
            out.append(inline(k, skip))
    return re.sub(r"[ \t\r\n]+", " ", "".join(out))


def text(n, skip=()):
    return inline(n, skip).strip()


def md_list(lst, task=False):
    lines = []
    ordered = lst.tag == "ol"
    for i, li in enumerate(direct(lst, "li"), 1):
        marker = "- [ ]" if task else (f"{i}." if ordered else "-")
        lines.append(f"{marker} {text(li, skip=('ul', 'ol'))}")
        for sub in direct(li, "ul") + direct(li, "ol"):
            lines += [INDENT + l for l in md_list(sub)]
    return lines


def admon(kind, title, chunks):
    body = "\n\n".join(c for c in chunks if c and c.strip())
    ind = "\n".join((INDENT + l) if l.strip() else "" for l in body.split("\n"))
    return f'!!! {kind} "{title}"\n\n{ind}'


def md_table(tbl):
    rows = []
    for tr in find_all(tbl, "tr"):
        rows.append([text(c).replace("|", "\\|") for c in direct(tr) if c.tag in ("th", "td")])
    if not rows:
        return ""
    w = max(len(r) for r in rows)
    rows = [r + [""] * (w - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * w]
    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(out)


UNKNOWN = set()
NUMBERED = True  # keep "Chapter III — ..." prefixes (full-depth subjects and the routine cross-reference them)
SKIP_CLASSES = {"toc", "stats-strip", "subj-grid", "chapter-label", "endcap", "cover", "block-label", "sub-label",
                "exercise-head", "howto"}


def render_children(n):
    chunks = []
    for k in n.kids:
        if isinstance(k, Node):
            chunks += render(k)
    return chunks


def render_exercise(a):
    num, name = find_one(a, cls="ex-num"), find_one(a, cls="ex-name")
    chunks = [f"### {text(num) if num else ''} — {text(name) if name else ''}"]
    dl = find_one(a, "dl", "exercise-meta")
    if dl:
        items = []
        for dt, dd in zip(direct(dl, "dt"), direct(dl, "dd")):
            items.append(f"- **{text(dt)}:** {text(dd)}")
        chunks.append("\n".join(items))
    kinds = {"block-description": None, "block-mandatory": ("success", "Mandatory"),
             "block-forbidden": ("failure", "Forbidden"), "block-norm": ("note", "Norm"),
             "block-bonus": ("tip", "Bonus")}
    for b in direct(a, "div"):
        key = next((k for k in kinds if k in b.classes), None)
        if key is None:
            continue
        body = []
        for k in direct(b):
            if k.tag == "p":
                body.append(text(k))
            elif k.tag in ("ul", "ol"):
                body.append("\n".join(md_list(k)))
        if kinds[key] is None:
            chunks += body
        else:
            kind, title = kinds[key]
            if key == "block-bonus":
                lbl = find_one(b, cls="block-label")
                title = text(lbl) if lbl and text(lbl) else title
            chunks.append(admon(kind, title, body))
    return chunks


def render_appendix(ab):
    h4 = find_one(ab, "h4")
    chunks = [f"### {text(h4) if h4 else ''}"]
    d = find_one(ab, "div", "defense")
    if d:
        ol = find_one(d, "ol")
        if ol:
            chunks += ["**Defense questions**", "\n".join(md_list(ol))]
    e = find_one(ab, "div", "edge")
    if e:
        ul = find_one(e, "ul")
        if ul:
            chunks += ["**Test / edge cases**", "\n".join(md_list(ul, task=True))]
    return chunks


def render(n):
    t, c = n.tag, n.classes
    if t in ("style", "script", "head", "nav", "header", "footer", "span") or (c & SKIP_CLASSES):
        return []
    if t == "section" and "chapter" in c:
        label = find_one(n, cls="chapter-label")
        h2 = next(iter(direct(n, "h2")), None)
        lab, h = (text(label) if label else ""), (text(h2) if h2 else "")
        if NUMBERED and re.match(r"^(Chapter|Appendix)", lab) and h:
            head = f"{lab} — {h}"
        else:
            head = h or lab
        return [f"## {head}"] + [x for k in n.kids if isinstance(k, Node) and k.tag != "h2" for x in render(k)]
    if t == "article" and "exercise" in c:
        return render_exercise(n)
    if t == "div" and "appendix-block" in c:
        return render_appendix(n)
    if t == "div" and "topic-block" in c:
        h4, body = find_one(n, "h4"), find_one(n, cls="tbody")
        chunks = [f"### {text(h4) if h4 else ''}"]
        if body:
            for k in direct(body):
                if k.tag == "p":
                    chunks.append(text(k))
                elif k.tag in ("ul", "ol"):
                    chunks.append("\n".join(md_list(k)))
        return chunks
    for cls, kind, title in (("outputs-block", "success", "Practical outputs"),
                             ("delusions-block", "warning", "Common delusions at this stage"),
                             ("exitgate-block", "abstract", "Exit gate: all of it, without notes"),
                             ("cert-block", "info", "Checkpoint")):
        if t == "div" and cls in c:
            body = []
            for k in direct(n):
                if k.tag in ("ul", "ol"):
                    body.append("\n".join(md_list(k)))
                elif k.tag == "p":
                    body.append(text(k))
            return [admon(kind, title, body)]
    if t == "div" and "capstone-note" in c:
        return [admon("info", "How this capstone forces everything together", [text(n)])]
    if t == "div" and ("lab-warning" in c or "warn-box" in c):
        return [admon("warning", "Read this first" if "lab-warning" in c else "Note",
                      [text(n)] if not direct(n, "p") else [text(p) for p in direct(n, "p")])]
    if t == "div" and "checklist" in c:
        lbl = find_one(n, cls="block-label")
        body = []
        for k in direct(n):
            if k.tag in ("ul", "ol"):
                body.append("\n".join(md_list(k)))
            elif k.tag == "p":
                body.append(text(k))
        return [admon("success", text(lbl) if lbl else "Checklist", body)]
    if t == "div" and "block-card" in c:
        h4 = find_one(n, "h4")
        dur = find_one(h4, "span", "dur") if h4 else None
        head = (text(h4, skip=("span",)) + (f" — {text(dur)}" if dur else "")) if h4 else ""
        out = [f"### {head}"]
        body = find_one(n, cls="bc-body")
        return out + (render_children(body) if body else [])
    if t == "div" and "cadence-grid" in c:
        items = []
        for card in find_all(n, "div", "cadence-card"):
            f, p = find_one(card, cls="freq"), find_one(card, "p")
            items.append(f"- **{text(f) if f else ''}:** {text(p) if p else ''}")
        return ["\n".join(items)]
    if t == "div" and "rule" in c:
        tag, body = find_one(n, cls="tag"), find_one(n, cls="body")
        return [f"**{text(tag)}** {text(body)}"] if tag and body else []
    if t == "p":
        if "foreword" in c:
            return ["> *" + text(n).strip('"') + "*"]
        if "appendix-intro" in c:
            return ["> " + text(n)]
        if "summary" in c:
            return []
        return [text(n)]
    if t in ("ul", "ol"):
        return ["\n".join(md_list(n, task="edge-list" in c))]
    if t == "pre":
        return ["```text\n" + raw_text(n).strip("\n") + "\n```"]
    if t == "table":
        return [md_table(n)]
    if t in ("h2", "h3"):
        return [("## " if t == "h2" else "### ") + text(n)]
    if t == "h4":
        return ["#### " + text(n)]
    if t in ("div", "section", "article", "body", "html", "root", "main"):
        if c and not (c & {"shell", "body", "tbody", "bc-body"}):
            UNKNOWN.add((t, " ".join(sorted(c))))
        return render_children(n)
    UNKNOWN.add((t, " ".join(sorted(c))))
    return [text(n)] if text(n) else []


def convert(path):
    global NUMBERED
    root = parse_html(path)
    NUMBERED = bool(find_all(root, "article", "exercise")) or Path(path).name.startswith("00_weekly")
    info = {"title": text(find_one(root, "h1")), "subtitle": "", "version": "", "summary": "",
            "exercises": [], "topics": []}
    for key, cls in (("subtitle", "subtitle"), ("version", "version")):
        n = find_one(root, cls=cls)
        info[key] = text(n) if n else ""
    s = find_one(root, "p", "summary")
    info["summary"] = text(s) if s else ""
    for a in find_all(root, "article", "exercise"):
        num, name = find_one(a, cls="ex-num"), find_one(a, cls="ex-name")
        desc = find_one(a, "div", "block-description")
        d = text(desc) if desc else ""
        d = re.sub(r"^\*\*Description\.\*\*\s*", "", d)
        info["exercises"].append({"label": text(num) if num else "", "name": text(name) if name else "", "desc": d})
    for tb in find_all(root, "div", "topic-block"):
        h4 = find_one(tb, "h4")
        info["topics"].append(text(h4) if h4 else "")
    shell = find_one(root, cls="shell") or root
    md = "\n\n".join(c for c in render_children(shell) if c and c.strip())
    info["md"] = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    return info


# ------------------------------------------------------------------- generators
def first_sentence(s, limit=200):
    s = re.sub(r"\s+", " ", s).strip()
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    out = m.group(1) if m else s
    return (out[: limit - 1] + "…") if len(out) > limit else out


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def write(path, content, force=False):
    path = Path(path)
    if path.exists() and not force:
        return "skip"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "write"


def subject_paths(stage, s):
    cdir = DOCS / stage["dir"] / f"{s['n']:02d}-{s['slug']}"
    return cdir


STATUS_BLOCK = "<!-- status:start -->\n<!-- status:end -->"


def overview_md(stage, s, info, prev):
    full = bool(info["exercises"])
    lines = ["---", f"title: {yaml_str(s['title'])}", f"description: {yaml_str(first_sentence(info['summary'], 155))}",
             "---", f"# {s['title']}", "",
             f"*Stage {stage['n']}: {stage['title']} · Subject {s['n']} of {len(stage['subjects'])} · "
             f"{stage['depth']} subject*", "", f"> {info['summary']}", ""]
    if full:
        lines += ["## What you will build", ""]
        for e in info["exercises"]:
            lines.append(f"- **{e['label']} — {e['name']}.** {first_sentence(e['desc'], 400)}")
    else:
        lines += ["## What you will study", ""]
        lines += [f"- {t}" for t in info["topics"]]
    lines += ["", "## In this chapter", "",
              "- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it",
              "- [The Subject](subject.md): the full specification, "
              + ("with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions"
                 if full else "with theory, practical outputs, common delusions and the exit gate"),
              "", "## Status", "", STATUS_BLOCK, ""]
    if prev:
        lines += ["## Order", "",
                  f"Recommended after [{prev[1]['title']}](../{prev[0]}/index.md)." if prev[2] == "same"
                  else f"Recommended after [{prev[1]['title']}](../../{prev[0]}/index.md).", ""]
    return "\n".join(lines)


def lessons_index_md(s):
    lines = ["---", 'title: "Lessons"', "---", f"# {s['title']}: Lessons", "",
             "Lessons are written while I study this subject, in my own words, with output from my own lab. "
             "Each one lists what it was verified on. Found a mistake? "
             "[Open an issue](https://github.com/YOUR_GITHUB_USERNAME/appsec-mastery/issues/new/choose).", ""]
    planned = s.get("planned_lessons")
    if planned:
        lines += ["## Planned lessons", "",
                  "This list is the outline, not a promise of order. Lessons are linked here once published.", ""]
        lines += [f"{i}. {t}" for i, t in enumerate(planned, 1)]
        lines.append("")
    else:
        lines += ["No lessons published yet. Watch the repository to be notified when this chapter starts.", ""]
    return "\n".join(lines)


def stage_index_md(stage):
    lines = ["---", f"title: {yaml_str('Stage %d: %s' % (stage['n'], stage['title']))}", "---",
             f"# Stage {stage['n']}: {stage['title']}", "", f"{stage['tagline']}", "",
             f"**Depth:** {stage['depth']} subjects.", "", "## Subjects", ""]
    for s in stage["subjects"]:
        lines.append(f"{s['n']}. [{s['title']}]({s['n']:02d}-{s['slug']}/index.md)")
    lines.append("")
    return "\n".join(lines)


ROADMAP_INTRO = """---
title: Roadmap
---
# Roadmap

Six stages, 42 subjects. Each subject is a project-style specification with a mandatory part, a forbidden list,
a bonus, a capstone and defense questions. Next to every subject I publish the lessons I write while studying it,
then my solutions. Status below is computed from what is actually published.

<!-- roadmap:start -->
<!-- roadmap:end -->
"""


def cmd_init(args):
    stats = {"write": 0, "skip": 0}
    for stage in CUR["stages"]:
        sdir = DOCS / stage["dir"]
        stats[write(sdir / "index.md", stage_index_md(stage), args.force)] += 1
        prev = None
        for s in stage["subjects"]:
            html = ARCHIVE / s["html"]
            if not html.exists():
                sys.exit(f"missing {html}")
            info = convert(html)
            cdir = subject_paths(stage, s)
            body = ["---", f"title: {yaml_str('The Subject')}", f"description: {yaml_str(first_sentence(info['summary'], 155))}",
                    "---", f"# {s['title']}: The Subject", "", f"*{info['subtitle']} · {info['version']}*", "",
                    f"> {info['summary']}", "", info["md"]]
            stats[write(cdir / "subject.md", "\n".join(body), args.force)] += 1
            stats[write(cdir / "index.md", overview_md(stage, s, info, prev), args.force)] += 1
            stats[write(cdir / "lessons" / "index.md", lessons_index_md(s), args.force)] += 1
            prev = (f"{s['n']:02d}-{s['slug']}", s, "same")
        # first subject of a stage points back to nothing; handled by prev=None
    routine = ARCHIVE / "00_weekly_routine.html"
    if routine.exists():
        info = convert(routine)
        body = ["---", 'title: "Weekly Study Routine"', f"description: {yaml_str(first_sentence(info['summary'], 155))}",
                "---", "# Weekly Study Routine", "", f"> {info['summary']}", "", info["md"]]
        stats[write(DOCS / "weekly-routine.md", "\n".join(body), args.force)] += 1
    stats[write(DOCS / "roadmap.md", ROADMAP_INTRO, args.force)] += 1
    print(f"init: {stats['write']} files written, {stats['skip']} existing files left untouched")
    if UNKNOWN:
        print("converter saw classes with no dedicated handler (rendered generically):")
        for u in sorted(UNKNOWN):
            print("  ", u)


# ---------------------------------------------------------------------- roadmap
def front_matter(path):
    s = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", s, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
    return fm


def published(folder):
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.glob("*.md") if p.name != "index.md" and not p.name.startswith("_"))


def collect():
    rows = []
    for stage in CUR["stages"]:
        for s in stage["subjects"]:
            cdir = subject_paths(stage, s)
            lessons = published(cdir / "lessons")
            sols = published(cdir / "solutions")
            fm = front_matter(cdir / "index.md") if (cdir / "index.md").exists() else {}
            status = "complete" if fm.get("status") == "complete" else ("writing" if lessons or sols else "planned")
            rows.append({"stage": stage, "s": s, "cdir": cdir, "lessons": len(lessons), "solutions": len(sols),
                         "status": status})
    return rows


def replace_between(text_, start, end, new):
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pat.search(text_):
        return None
    return pat.sub(lambda m: start + "\n" + new + "\n" + end, text_)


def cmd_roadmap_tables(args):
    rows = collect()
    label = {"planned": "Planned", "writing": "Writing", "complete": "Complete"}
    total_l = sum(r["lessons"] for r in rows)
    done = sum(1 for r in rows if r["status"] == "complete")
    started = sum(1 for r in rows if r["status"] != "planned")

    # docs/roadmap.md — full table per stage, links relative to docs/
    out = [f"**Progress:** {done} of {len(rows)} subjects complete · {started} started · {total_l} lessons published.", ""]
    for stage in CUR["stages"]:
        out += [f"## Stage {stage['n']}: {stage['title']}", "", f"{stage['tagline']}", "",
                "| # | Subject | Depth | Lessons | Solutions | Status |", "|---|---|---|---|---|---|"]
        for r in rows:
            if r["stage"] is not stage:
                continue
            s = r["s"]
            link = f"{stage['dir']}/{s['n']:02d}-{s['slug']}/index.md"
            out.append(f"| {s['n']} | [{s['title']}]({link}) | {stage['depth']} | {r['lessons']} | {r['solutions']} | {label[r['status']]} |")
        out.append("")
    p = DOCS / "roadmap.md"
    if not p.exists():
        p.write_text(ROADMAP_INTRO, encoding="utf-8")
    new = replace_between(p.read_text(encoding="utf-8"), "<!-- roadmap:start -->", "<!-- roadmap:end -->", "\n".join(out))
    p.write_text(new, encoding="utf-8")

    # README.md — compact per-stage summary, links relative to repo root
    readme = ROOT / "README.md"
    if readme.exists():
        summ = ["| Stage | Subjects | Lessons published | Status |", "|---|---|---|---|"]
        for stage in CUR["stages"]:
            rs = [r for r in rows if r["stage"] is stage]
            st = "Complete" if all(r["status"] == "complete" for r in rs) else (
                "Writing" if any(r["status"] != "planned" for r in rs) else "Planned")
            summ.append(f"| [Stage {stage['n']}: {stage['title']}](docs/{stage['dir']}/index.md) | {len(rs)} | "
                        f"{sum(r['lessons'] for r in rs)} | {st} |")
        summ += ["", f"{done} of {len(rows)} subjects complete · {total_l} lessons published. "
                     "Full table: [roadmap](docs/roadmap.md)."]
        new = replace_between(readme.read_text(encoding="utf-8"), "<!-- roadmap:start -->", "<!-- roadmap:end -->",
                              "\n".join(summ))
        if new is not None:
            readme.write_text(new, encoding="utf-8")

    # each chapter's overview — status block
    for r in rows:
        ip = r["cdir"] / "index.md"
        if not ip.exists():
            continue
        parts = [f"**{label[r['status']]}.** {r['lessons']} lesson(s) and {r['solutions']} solution(s) published."]
        if r["status"] == "planned":
            parts.append("Not started yet. Follow the repository to be notified when this chapter begins.")
        new = replace_between(ip.read_text(encoding="utf-8"), "<!-- status:start -->", "<!-- status:end -->",
                              "\n\n".join(parts))
        if new is not None:
            ip.write_text(new, encoding="utf-8")
    print(f"roadmap: {done}/{len(rows)} complete, {started} started, {total_l} lessons published")


def page_title(path):
    txt = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", txt, re.S)
    if m:
        t = re.search(r'^title:\s*"?(.*?)"?\s*$', m.group(1), re.M)
        if t and t.group(1):
            return t.group(1)
    h = re.search(r"^#\s+(.+)$", txt, re.M)
    return h.group(1).strip() if h else path.stem


def q(s):
    return json.dumps(s, ensure_ascii=False)


def nav_lines():
    def rel(p):
        return p.relative_to(DOCS).as_posix()

    out = ["nav:", f"  - Home: index.md"]
    start = [("how-to-use.md", "How to use this site"), ("weekly-routine.md", "Weekly study routine"),
             ("ai-tutor.md", "Using AI as a tutor"), ("ethics.md", "Responsible use"), ("about.md", "About")]
    present = [(f, t) for f, t in start if (DOCS / f).exists()]
    if present:
        out.append("  - Start here:")
        out += [f"      - {q(t)}: {f}" for f, t in present]
    out.append("  - Roadmap: roadmap.md")
    for stage in CUR["stages"]:
        out.append(f"  - {q('Stage %d: %s' % (stage['n'], stage['title']))}:")
        out.append(f"      - {rel(DOCS / stage['dir'] / 'index.md')}")
        for s in stage["subjects"]:
            cdir = subject_paths(stage, s)
            out.append(f"      - {q(s['title'])}:")
            out.append(f"          - {rel(cdir / 'index.md')}")
            lessons = published(cdir / "lessons")
            out.append("          - Lessons:")
            out.append(f"              - {rel(cdir / 'lessons' / 'index.md')}")
            out += [f"              - {q(page_title(p))}: {rel(p)}" for p in lessons]
            out.append(f"          - The Subject: {rel(cdir / 'subject.md')}")
            sols = published(cdir / "solutions")
            if sols:
                out.append("          - Solutions:")
                out += [f"              - {q(page_title(p))}: {rel(p)}" for p in sols]
    jdir = DOCS / "journal"
    if jdir.is_dir() and (jdir / "index.md").exists():
        entries = sorted(published(jdir), reverse=True)
        out.append("  - Journal:")
        out.append(f"      - {rel(jdir / 'index.md')}")
        out += [f"      - {q(page_title(p))}: {rel(p)}" for p in entries]
    return out


def cmd_nav(args):
    p = ROOT / "mkdocs.yml"
    new = replace_between(p.read_text(encoding="utf-8"), "# <nav:start>", "# <nav:end>", "\n".join(nav_lines()))
    if new is None:
        sys.exit("mkdocs.yml has no '# <nav:start>' / '# <nav:end>' markers")
    p.write_text(new, encoding="utf-8")
    print("nav: mkdocs.yml navigation regenerated")


def cmd_refresh(args):
    cmd_roadmap_tables(args)
    cmd_nav(args)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("init")
    s.add_argument("--force", action="store_true", help="overwrite existing chapter files (destroys hand edits!)")
    s.set_defaults(fn=cmd_init)
    sp.add_parser("refresh", help="status tables, status blocks and mkdocs navigation").set_defaults(fn=cmd_refresh)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
