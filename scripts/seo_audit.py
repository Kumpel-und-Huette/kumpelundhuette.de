#!/usr/bin/env python3
"""SEO audit for the Kumpel & Hütte Hugo site.

Builds the site with Hugo into a temporary directory (or reads an existing
build with --site), scores every indexable page and the site as a whole and
prints a report. Focus keywords, page profiles and thresholds live in
scripts/seo_audit.toml.

    python3 scripts/seo_audit.py
    python3 scripts/seo_audit.py --site public --json seo-report.json
    python3 scripts/seo_audit.py --verbose --page /einziehen-bei-uns/
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

if sys.version_info < (3, 11):
    sys.exit("seo_audit.py needs Python 3.11 or newer (tomllib).")
import tomllib

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = Path(__file__).with_suffix(".toml")

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
BLOCK = {
    "address", "article", "aside", "blockquote", "br", "button", "caption", "dd", "details", "div", "dl", "dt",
    "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr",
    "label", "legend", "li", "main", "nav", "ol", "p", "pre", "section", "summary", "table", "td", "th", "tr", "ul",
}
P_CLOSERS = {
    "address", "article", "aside", "blockquote", "details", "div", "dl", "fieldset", "figcaption", "figure",
    "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "main", "nav", "ol", "p", "pre",
    "section", "table", "ul",
}
SKIP_TEXT = {"script", "style", "noscript", "template", "svg"}
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]")
WEBPAGE_TYPES = {"WebPage", "AboutPage", "ContactPage", "CollectionPage", "ItemPage", "FAQPage", "ProfilePage", "QAPage"}
ARTICLE_TYPES = {"Article", "BlogPosting", "NewsArticle", "Report"}

COLOR = sys.stdout.isatty()


def paint(text, code):
    return f"\033[{code}m{text}\033[0m" if COLOR else str(text)


def score_color(score):
    return "32" if score >= 90 else "33" if score >= 75 else "31"


# --------------------------------------------------------------------------- text helpers

def norm(text):
    text = (text or "").replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ").lower()
    text = re.sub(r"[\-‐‑–—/]", " ", text)
    text = re.sub(r"[^\w\s€§]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def term_regex(term):
    return re.compile(r"(?<!\w)" + re.escape(norm(term)))


def has_term(text, term):
    haystack = norm(text)
    return any(term_regex(alt).search(haystack) for alt in term.split("|"))


def count_term(text, term):
    alts = sorted((norm(a) for a in term.split("|")), key=len, reverse=True)
    pattern = re.compile(r"(?<!\w)(?:" + "|".join(re.escape(a) for a in alts) + ")")
    return len(pattern.findall(norm(text)))


def match_terms(text, terms):
    missing = [t for t in terms if not has_term(text, t)]
    return (1 - len(missing) / len(terms)) if terms else 0.0, missing


def words_of(text):
    return re.findall(r"[^\W_]+(?:[-'’][^\W_]+)*", text or "")


def syllables(word, lang):
    w = word.lower()
    if lang == "de":
        return max(1, len(re.findall(r"[aeiouyäöü]+", w)))
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def readability(text, lang):
    sentences = [s for s in re.split(r"(?<=[.!?])\s+|\n+", text) if len(words_of(s)) >= 3]
    words = [w for s in sentences for w in words_of(s) if not w.isdigit()]
    if len(sentences) < 3 or len(words) < 50:
        return None
    asl = len(words) / len(sentences)
    asw = sum(syllables(w, lang) for w in words) / len(words)
    fre = 180 - asl - 58.5 * asw if lang == "de" else 206.835 - 1.015 * asl - 84.6 * asw
    return {"fre": round(fre, 1), "asl": round(asl, 1), "asw": round(asw, 2), "sentences": len(sentences)}


def clean_ws(text):
    text = text.replace("\u00ad", "")
    text = re.sub(r"[ \t\r\f\v\u00a0]+", " ", text)
    return re.sub(r"\s*\n\s*", "\n", text).strip()


def ramp(value, bad, good):
    """1.0 at `good`, 0.0 at `bad`, linear in between (works in both directions)."""
    if good == bad:
        return 1.0 if value == good else 0.0
    return max(0.0, min(1.0, (value - bad) / (good - bad)))


# --------------------------------------------------------------------------- HTML parsing

class Entry:
    __slots__ = ("tag", "flags", "record")

    def __init__(self, tag, flags, record=None):
        self.tag, self.flags, self.record = tag, flags, record


class PageParser(HTMLParser):
    def __init__(self, excluded_classes, decorative_classes):
        super().__init__(convert_charrefs=True)
        self.excluded_classes = set(excluded_classes)
        self.decorative_classes = set(decorative_classes)
        self.stack, self.active = [], Counter()
        self.lang, self.title = None, None
        self.meta, self.links, self.headings, self.images, self.anchors, self.jsonld = [], [], [], [], [], []
        self.text_all, self.text_main = [], []
        self._title_buf = None
        self._ld_buf = None

    def _flags_for(self, tag, attrs):
        classes = set((attrs.get("class") or "").split())
        flags = set()
        if tag == "head":
            flags.add("head")
        if tag == "main":
            flags.add("main")
        if tag in SKIP_TEXT:
            flags.add("skip")
        if tag == "nav" or classes & self.excluded_classes:
            flags.add("excluded")
        if attrs.get("aria-hidden") == "true":
            flags.add("hidden")
        if tag in ("a", "button"):
            flags.add("control")
        if classes & self.decorative_classes or attrs.get("role") in ("presentation", "none"):
            flags.add("decor")
        return flags

    def _in_content(self):
        a = self.active
        return a["main"] and not (a["excluded"] or a["hidden"] or a["skip"])

    def _pop(self):
        entry = self.stack.pop()
        for f in entry.flags:
            self.active[f] -= 1
        rec = entry.record
        if rec is None:
            return
        kind = rec.get("_kind")
        if kind in ("heading", "anchor"):
            rec["text"] = " ".join("".join(rec.pop("_buf")).split())
        elif kind == "title":
            if self.title is None:
                self.title = " ".join("".join(self._title_buf).split())
            self._title_buf = None
        elif kind == "ld":
            self.jsonld.append("".join(self._ld_buf))
            self._ld_buf = None

    def _pop_until(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i].tag == tag:
                while len(self.stack) > i:
                    self._pop()
                return

    def _close_open(self, tags, stop):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i].tag in tags:
                while len(self.stack) > i:
                    self._pop()
                return
            if self.stack[i].tag in stop:
                return

    def _newline(self):
        self.text_all.append("\n")
        if self._in_content():
            self.text_main.append("\n")

    def handle_starttag(self, tag, attrs_list):
        attrs = {k: ("" if v is None else v) for k, v in attrs_list}
        if tag == "li":
            self._close_open({"li"}, {"ul", "ol", "menu"})
        elif tag in ("dt", "dd"):
            self._close_open({"dt", "dd"}, {"dl"})
        elif tag == "tr":
            self._close_open({"tr"}, {"table", "thead", "tbody", "tfoot"})
        elif tag in ("td", "th"):
            self._close_open({"td", "th"}, {"tr"})
        elif tag in ("thead", "tbody", "tfoot"):
            self._close_open({"thead", "tbody", "tfoot"}, {"table"})
        if tag in P_CLOSERS and self.stack and self.stack[-1].tag == "p":
            self._pop()
        if tag in BLOCK:
            self._newline()

        record = None
        in_main = bool(self.active["main"])
        if tag == "html":
            self.lang = attrs.get("lang")
        elif tag == "title" and self.active["head"] and self.title is None:
            self._title_buf = []
            record = {"_kind": "title"}
        elif tag == "meta":
            key = (attrs.get("name") or attrs.get("property") or attrs.get("http-equiv") or "").lower()
            if key:
                self.meta.append((key, attrs.get("content", "")))
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self._ld_buf = []
            record = {"_kind": "ld"}
        elif re.fullmatch(r"h[1-6]", tag):
            record = {"_kind": "heading", "level": int(tag[1]), "_buf": [], "main": in_main,
                      "content": self._in_content()}
            self.headings.append(record)
        elif tag == "a" and "href" in attrs:
            record = {"_kind": "anchor", "href": attrs["href"], "_buf": [], "main": in_main,
                      "content": self._in_content(), "rel": attrs.get("rel", "")}
            self.anchors.append(record)
        elif tag == "img":
            decorative_ok = bool(self.active["control"] or self.active["hidden"] or self.active["decor"])
            self.images.append({"src": attrs.get("src", ""), "has_alt": "alt" in attrs, "alt": attrs.get("alt", ""),
                                "width": attrs.get("width"), "height": attrs.get("height"), "main": in_main,
                                "decorative_ok": decorative_ok})
            for entry in self.stack:
                if entry.record and entry.record.get("_kind") == "anchor":
                    entry.record["_buf"].append(" " + attrs.get("alt", "") + " ")

        if tag in VOID:
            return
        flags = self._flags_for(tag, attrs)
        for f in flags:
            self.active[f] += 1
        self.stack.append(Entry(tag, flags, record))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        self._pop_until(tag)
        if tag in BLOCK:
            self._newline()

    def handle_data(self, data):
        if self._title_buf is not None:
            self._title_buf.append(data)
        if self._ld_buf is not None:
            self._ld_buf.append(data)
            return
        if self.active["skip"] or self.active["head"]:
            return
        self.text_all.append(data)
        if self._in_content():
            self.text_main.append(data)
        for entry in self.stack:
            rec = entry.record
            if rec and rec.get("_kind") in ("heading", "anchor"):
                rec["_buf"].append(data)

    def close(self):
        super().close()
        while self.stack:
            self._pop()


# --------------------------------------------------------------------------- model

@dataclass
class Item:
    label: str
    weight: float
    fraction: float
    message: str = ""


@dataclass
class Result:
    name: str
    weight: float
    items: list
    notes: list = field(default_factory=list)

    @property
    def fraction(self):
        total = sum(i.weight for i in self.items)
        return sum(i.weight * i.fraction for i in self.items) / total if total else 1.0


@dataclass
class Page:
    path: str
    file: Path
    lang: str
    kind: str
    parser: PageParser
    cfg: dict
    profile: str
    results: list = field(default_factory=list)

    @property
    def meta(self):
        out = {}
        for k, v in self.parser.meta:
            out.setdefault(k, v)
        return out

    @property
    def title(self):
        return self.parser.title or ""

    @property
    def description(self):
        return (self.meta.get("description") or "").strip()

    @property
    def robots(self):
        return (self.meta.get("robots") or "").lower()

    @property
    def indexable(self):
        return self.kind == "page" and "noindex" not in self.robots

    @property
    def h1s(self):
        return [h for h in self.parser.headings if h["level"] == 1]

    @property
    def canonical(self):
        return next((l.get("href", "") for l in self.parser.links if l.get("rel") == "canonical"), "")

    @property
    def alternates(self):
        return {l["hreflang"]: l.get("href", "") for l in self.parser.links
                if l.get("rel") == "alternate" and l.get("hreflang")}

    @property
    def main_text(self):
        return clean_ws("".join(self.parser.text_main))

    @property
    def all_text(self):
        return clean_ws("".join(self.parser.text_all))

    @property
    def focus(self):
        return self.cfg.get("focus", [])

    @property
    def secondary(self):
        return self.cfg.get("secondary", [])

    @property
    def local(self):
        return self.cfg.get("local", self.profile in ("money", "contact", "listing"))

    @property
    def score(self):
        total = sum(r.weight for r in self.results)
        return 100 * sum(r.weight * r.fraction for r in self.results) / total if total else 0.0


class Site:
    def __init__(self, directory, cfg):
        self.dir = directory
        self.cfg = cfg
        self.base = cfg["site"]["base_url"].rstrip("/") + "/"
        self.host = urlsplit(self.base).netloc
        self.pages = {}
        self.page_cfg = {p["path"]: p for p in cfg.get("pages", [])}
        style = cfg.get("style", {})
        for file in sorted(directory.rglob("*.html")):
            rel = file.relative_to(directory).as_posix()
            if rel.endswith("index.html"):
                path = "/" + rel[: -len("index.html")]
            else:
                path = "/" + rel
            parser = PageParser(style.get("excluded_classes", []), style.get("decorative_containers", []))
            parser.feed(file.read_text(encoding="utf-8", errors="replace"))
            parser.close()
            kind = "page"
            if any(k == "refresh" for k, _ in parser.meta):
                kind = "alias"
            elif rel.endswith("404.html"):
                kind = "404"
            elif any(path.startswith(pfx) for pfx in cfg["site"].get("taxonomy_prefixes", [])):
                kind = "taxonomy"
            lang = next((l for l in cfg["site"]["languages"] if path.startswith(f"/{l}/")),
                        cfg["site"]["default_language"])
            pcfg = self.page_cfg.get(path, {})
            self.pages[path] = Page(path, file, lang, kind, parser, pcfg, pcfg.get("profile", "money"))
        self.sitemap_urls, self.sitemap_errors = self._read_sitemaps()

    def url_for(self, path):
        return self.base.rstrip("/") + path

    def path_of(self, url, page_url=None):
        full = urljoin(page_url or self.base, url)
        parts = urlsplit(full)
        if parts.scheme not in ("http", "https") or (parts.netloc and parts.netloc != self.host):
            return None
        return unquote(parts.path) or "/"

    def exists(self, path):
        target = self.dir / path.lstrip("/")
        if path.endswith("/"):
            return (target / "index.html").is_file()
        return target.is_file() or (target / "index.html").is_file()

    def _read_sitemaps(self):
        urls, errors, seen = [], [], set()
        queue = ["/sitemap.xml"]
        while queue:
            path = queue.pop()
            if path in seen:
                continue
            seen.add(path)
            file = self.dir / path.lstrip("/")
            if not file.is_file():
                errors.append(f"{path} is missing")
                continue
            try:
                root = ET.parse(file).getroot()
            except ET.ParseError as exc:
                errors.append(f"{path} does not parse: {exc}")
                continue
            for loc in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                value = (loc.text or "").strip()
                if root.tag.endswith("sitemapindex"):
                    child = self.path_of(value)
                    if child:
                        queue.append(child)
                    else:
                        errors.append(f"sitemap index points off-site: {value}")
                else:
                    urls.append(value)
        return urls, errors

    @property
    def indexable(self):
        return [p for p in self.pages.values() if p.indexable]


# --------------------------------------------------------------------------- JSON-LD helpers

def ld_nodes(blocks):
    nodes, errors = [], []
    for raw in blocks:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(str(exc))
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, list):
                stack.extend(node)
            elif isinstance(node, dict):
                if "@type" in node:
                    nodes.append(node)
                stack.extend(v for v in node.values() if isinstance(v, (dict, list)))
    return nodes, errors


def types_of(node):
    t = node.get("@type", [])
    return set(t if isinstance(t, list) else [t])


def dig(node, dotted):
    for alt in dotted.split("|"):
        cur, ok = node, True
        for key in alt.split("."):
            if isinstance(cur, dict) and cur.get(key) not in (None, "", []):
                cur = cur[key]
            else:
                ok = False
                break
        if ok:
            return cur
    return None


def validate_fields(node, fields):
    missing = [f for f in fields if dig(node, f) is None]
    return 1 - len(missing) / len(fields), missing


def validate_breadcrumbs(node):
    items = node.get("itemListElement") or []
    if len(items) < 2:
        return 0.0, ["itemListElement needs at least 2 entries"]
    problems = []
    for i, it in enumerate(items, 1):
        if it.get("position") != i:
            problems.append(f"item {i} position is {it.get('position')!r}")
        if not it.get("name"):
            problems.append(f"item {i} has no name")
        if i < len(items) and not it.get("item"):
            problems.append(f"item {i} has no item URL")
    return (1.0 if not problems else 0.5), problems


def validate_faq(node):
    questions = node.get("mainEntity") or []
    questions = questions if isinstance(questions, list) else [questions]
    if not questions:
        return 0.0, ["mainEntity has no questions"]
    good = [q for q in questions if q.get("name") and dig(q, "acceptedAnswer.text")]
    return len(good) / len(questions), [] if len(good) == len(questions) else ["some questions lack name/acceptedAnswer.text"]


# --------------------------------------------------------------------------- page checks

def check_title(p, site):
    th, t = site.cfg["thresholds"], p.title
    n = len(t)
    items = [Item("present", 2, 1.0 if t else 0.0, "the page has no <title>")]
    lo, hi = th["title_min"], th["title_max"]
    length = 1.0 if lo <= n <= hi else (0.5 if (hi < n <= hi + 10 or lo / 2 <= n < lo) else 0.0)
    items.append(Item("length", 2, length if n else 0.0, f"{n} characters (aim for {lo}-{hi})"))
    if p.profile != "legal":
        if p.focus:
            frac, missing = match_terms(t, p.focus)
            items.append(Item("focus keyword", 3, frac, f"missing {missing}"))
        else:
            items.append(Item("focus keyword", 3, 0.0, "no focus keyword configured in seo_audit.toml"))
        if p.local:
            loc = site.cfg["site"]["location"]
            items.append(Item("location", 1, 1.0 if has_term(t, loc) else 0.0, f"'{loc}' is not in the title"))
    brand = any(has_term(t, b) for b in site.cfg["site"]["brand"])
    items.append(Item("brand", 1, 1.0 if brand else 0.0, "brand name is not in the title"))
    dirty = [x for x in ("—", "–") if x in t] + (["emoji"] if EMOJI.search(t) else [])
    items.append(Item("clean", 0.5, 0.0 if dirty else 1.0, f"contains {dirty}"))
    dupes = [q.path for q in site.indexable if q is not p and q.title == t]
    items.append(Item("unique", 0.5, 0.0 if dupes else 1.0, f"same title on {dupes}"))
    return Result("title", 15, items)


def check_description(p, site):
    th, d = site.cfg["thresholds"], p.description
    n = len(d)
    items = [Item("present", 2, 1.0 if d else 0.0, "no meta description")]
    lo, hi = th["description_min"], th["description_max"]
    length = 1.0 if lo <= n <= hi else (0.5 if (70 <= n < lo or hi < n <= hi + 20) else 0.0)
    items.append(Item("length", 2, length if n else 0.0, f"{n} characters (aim for {lo}-{hi})"))
    reason = ""
    if d.endswith(("…", "...")):
        reason = "ends with an ellipsis, looks like a truncated auto-summary"
    else:
        head = " ".join(d.split()[:4])
        for crumb in site.cfg["style"].get("breadcrumb_words", []):
            if has_term(head, crumb):
                reason = f"starts with navigation text ('{crumb}')"
    items.append(Item("written by hand", 2, 0.0 if (reason or not d) else 1.0, reason or "missing"))
    if p.profile != "legal":
        if p.focus:
            frac, missing = match_terms(d, p.focus)
            items.append(Item("focus keyword", 2, frac, f"missing {missing}"))
        if p.local:
            loc = site.cfg["site"]["location"]
            items.append(Item("location", 1, 1.0 if has_term(d, loc) else 0.0, f"'{loc}' is not in the description"))
    dupes = [q.path for q in site.indexable if q is not p and d and q.description == d]
    items.append(Item("unique", 1, 0.0 if dupes else 1.0, f"same description on {dupes}"))
    return Result("description", 10, items)


def check_h1(p, site):
    h1s = p.h1s
    count = 1.0 if len(h1s) == 1 else (0.5 if h1s else 0.0)
    items = [Item("exactly one", 4, count, f"{len(h1s)} <h1> elements")]
    text = h1s[0]["text"] if h1s else ""
    if p.profile != "legal":
        if p.focus:
            frac, missing = match_terms(text, p.focus)
            items.append(Item("focus keyword", 5, frac, f"'{text}' is missing {missing}"))
        else:
            items.append(Item("focus keyword", 5, 0.0, "no focus keyword configured in seo_audit.toml"))
    items.append(Item("length", 1, 1.0 if 0 < len(text) <= 70 else 0.0, f"{len(text)} characters (keep it under 70)"))
    return Result("h1", 10, items)


def check_headings(p, site):
    heads = p.parser.headings
    skips, prev = [], None
    for h in heads:
        if prev is not None and h["level"] > prev + 1:
            skips.append(f"h{prev} -> h{h['level']} ('{h['text'][:40]}')")
        prev = h["level"]
    empty = [f"h{h['level']}" for h in heads if not h["text"]]
    items = [Item("no skipped levels", 2.5, 0.0 if skips else 1.0, "; ".join(skips[:4])),
             Item("no empty headings", 1, 0.0 if empty else 1.0, f"empty: {empty}")]
    if p.profile in ("money", "contact", "listing"):
        h2 = sum(1 for h in heads if h["level"] == 2 and h["content"])
        need = p.cfg.get("min_h2", 2 if p.profile == "money" else 1)
        items.append(Item("sub-headings", 1.5, min(1.0, h2 / need) if need else 1.0,
                          f"{h2} content <h2> (want {need}+)"))
    return Result("headings", 5, items)


def check_content(p, site):
    if p.profile == "legal":
        return None
    text = p.main_text
    words = words_of(text)
    n = len(words)
    th = site.cfg["thresholds"]
    need = p.cfg.get("min_words", th["min_words"].get(p.profile, th["min_words"]["money"]))
    items = [Item("depth", 3, ramp(n, need * 0.5, need), f"{n} words in the main content (want {need}+)")]
    if p.focus:
        first = " ".join(words[:100])
        frac, missing = match_terms(first, p.focus)
        items.append(Item("focus in first 100 words", 2, frac, f"missing {missing}"))
        primary = p.focus[0]
        hits = count_term(text, primary)
        items.append(Item("focus frequency", 1.5, ramp(hits, 0, 2), f"'{primary}' appears {hits}x"))
        density = 100 * hits / n if n else 0
        items.append(Item("no keyword stuffing", 1, 1.0 if density <= th["max_density"] else 0.0,
                          f"'{primary}' density {density:.1f}% (max {th['max_density']}%)"))
    else:
        items.append(Item("focus keyword", 3.5, 0.0, "no focus keyword configured in seo_audit.toml"))
    if p.secondary:
        present = [t for t in p.secondary if has_term(text, t)]
        missing = [t for t in p.secondary if t not in present]
        items.append(Item("related terms", 2.5, min(1.0, len(present) / (0.6 * len(p.secondary))),
                          f"{len(present)}/{len(p.secondary)} present, missing {missing}"))
    return Result("content", 15, items)


def check_readability(p, site):
    if p.profile == "legal":
        return None
    stats = readability(p.main_text, p.lang)
    if stats is None:
        return None
    th = site.cfg["thresholds"]["readability"][p.lang]
    fre = ramp(stats["fre"], th["fre_bad"], th["fre_good"])
    asl = ramp(stats["asl"], th["asl_bad"], th["asl_good"])
    formula = "Amstad" if p.lang == "de" else "Flesch"
    result = Result("readability", 5, [
        Item("reading ease", 3.5, fre, f"{formula} {stats['fre']} (aim for {th['fre_good']}+)"),
        Item("sentence length", 1.5, asl, f"{stats['asl']} words per sentence (aim for {th['asl_good']} or less)"),
    ])
    result.notes.append(f"{formula} reading ease {stats['fre']}, {stats['asl']} words/sentence, "
                        f"{stats['asw']} syllables/word over {stats['sentences']} sentences")
    return result


def dash_hits(text):
    hits = []
    for m in re.finditer(r"(.{0,20})(—| – |\s-\s)(.{0,20})", text):
        before, dash, after = m.groups()
        if dash.strip() in "–-" and before[-1:].isdigit() and after[:1].isdigit():
            continue
        hits.append((before + dash + after).strip())
    return hits


def check_style(p, site):
    text = p.all_text.replace("\n", " ")
    em = [h for h in dash_hits(text) if "—" in h]
    other = [h for h in dash_hits(text) if "—" not in h]
    low = text.lower()
    leftovers = [w for w in site.cfg["style"]["placeholders"] if w in low]
    h1 = p.h1s[0]["text"] if p.h1s else ""
    emoji = [x for x in (p.title, h1) if EMOJI.search(x)]
    result = Result("style", 5, [
        Item("no em dashes", 1.5, 0.0 if em else 1.0, f"{len(em)}x, e.g. '{em[0]}'" if em else ""),
        Item("no dash-style breaks", 1.5, 0.0 if other else 1.0, f"{len(other)}x, e.g. '{other[0]}'" if other else ""),
        Item("no placeholder text", 1, 0.0 if leftovers else 1.0, f"found {leftovers}"),
        Item("no emoji in title or H1", 1, 0.0 if emoji else 1.0, f"in {emoji}"),
    ])
    bangs = p.main_text.count("!")
    if bangs:
        result.notes.append(f"{bangs} exclamation mark(s) in the main content")
    return result


def check_links(p, site):
    page_url = site.url_for(p.path)
    broken, malformed, generic, targets = [], [], [], set()
    generic_words = {norm(w) for w in site.cfg["style"]["generic_anchors"].get(p.lang, [])}
    for a in p.parser.anchors:
        href = a["href"].strip()
        if "ZgotmplZ" in href:
            malformed.append(f"{href} (Go template rejected the URL, e.g. tel: without safeURL)")
            continue
        if href.startswith("tel:"):
            if not re.fullmatch(r"tel:\+?\d{6,15}", href):
                malformed.append(href)
            continue
        if href.startswith("mailto:"):
            if not re.fullmatch(r"mailto:[^@\s]+@[^@\s]+\.[a-z]{2,}(\?.*)?", href, re.I):
                malformed.append(href)
            continue
        if href.startswith(("#", "javascript:")):
            continue
        path = site.path_of(href, page_url)
        if path is None:
            continue
        if not site.exists(path):
            broken.append(href)
            continue
        if a["content"]:
            if norm(a["text"]) in generic_words:
                generic.append(a["text"])
            if path != p.path:
                targets.add(path)
    items = [Item("no broken internal links", 4, 0.0 if broken else 1.0, f"broken: {sorted(set(broken))[:5]}"),
             Item("valid tel/mailto links", 0.5, 0.0 if malformed else 1.0, f"malformed: {malformed[:3]}"),
             Item("descriptive anchor text", 2, 0.0 if generic else 1.0, f"generic: {sorted(set(generic))}")]
    if p.profile != "legal":
        need = p.cfg.get("min_links", 2)
        items.append(Item("links into other pages", 2, min(1.0, len(targets) / need),
                          f"{len(targets)} contextual internal link target(s) (want {need}+)"))
        sources = site.inbound.get(p.path, {})
        ctx, nav = sources.get("content", set()), sources.get("nav", set())
        frac = 1.0 if ctx else (0.5 if nav else 0.0)
        items.append(Item("linked from other pages", 1.5, frac,
                          "only linked from menus, no in-text link points here" if nav else "no page links here"))
    return Result("links", 10, items)


def check_images(p, site):
    imgs = p.parser.images
    if not imgs:
        return None
    with_alt = [i for i in imgs if i["has_alt"]]
    content = [i for i in imgs if i["main"] and not i["decorative_ok"]]
    described = [i for i in content if i["alt"].strip()]
    sized = [i for i in imgs if i["width"] and i["height"]]
    missing = []
    for i in imgs:
        path = site.path_of(i["src"], site.url_for(p.path)) if i["src"] else None
        if path and not site.exists(path):
            missing.append(i["src"])
    return Result("images", 5, [
        Item("alt attribute", 2, len(with_alt) / len(imgs), f"{len(imgs) - len(with_alt)} image(s) without alt"),
        Item("content images described", 1.5, len(described) / len(content) if content else 1.0,
             f"{len(content) - len(described)} content image(s) with empty alt"),
        Item("width and height", 1, len(sized) / len(imgs), f"{len(imgs) - len(sized)} image(s) without dimensions"),
        Item("image files exist", 0.5, 0.0 if missing else 1.0, f"missing: {missing[:3]}"),
    ])


def check_technical(p, site):
    items = [Item("html lang", 1.5, 1.0 if (p.parser.lang or "").split("-")[0] == p.lang else 0.0,
                  f"lang='{p.parser.lang}', expected '{p.lang}'")]
    canon = p.canonical
    own = site.url_for(p.path)
    if not canon:
        items.append(Item("canonical", 2.5, 0.0, "no canonical link"))
    else:
        ok = unquote(canon) == unquote(own)
        items.append(Item("canonical", 2.5, 1.0 if ok else (0.5 if canon.startswith("https://") else 0.0),
                          f"canonical is {canon}, expected {own}"))
    alts = p.alternates
    langs = site.cfg["site"]["languages"]
    have = [l for l in langs if l in alts]
    items.append(Item("hreflang languages", 1.5, len(have) / len(langs), f"hreflang for {have}, want {langs}"))
    items.append(Item("hreflang x-default", 0.75, 1.0 if "x-default" in alts else 0.0, "no x-default alternate"))
    bad = []
    for lang, href in alts.items():
        target = site.path_of(href)
        other = site.pages.get(target) if target else None
        if other is None:
            bad.append(f"{lang}: {href} does not exist")
        elif lang != "x-default" and target != p.path:
            back = {unquote(u) for u in other.alternates.values()}
            if unquote(own) not in back:
                bad.append(f"{lang}: {target} does not link back")
    items.append(Item("hreflang targets", 0.75, 0.0 if bad else 1.0, "; ".join(bad[:3])))
    items.append(Item("viewport", 0.5, 1.0 if "viewport" in p.meta else 0.0, "no meta viewport"))
    blocked = [w for w in ("noindex", "nofollow", "none") if w in p.robots]
    items.append(Item("indexable", 0.75, 0.0 if blocked else 1.0, f"robots meta says {blocked}"))
    in_map = unquote(own) in {unquote(u) for u in site.sitemap_urls}
    items.append(Item("in sitemap", 1, 1.0 if in_map else 0.0, "the page is not listed in the sitemap"))
    return Result("technical", 10, items)


def check_social(p, site):
    meta = p.meta
    canon = p.canonical
    image = meta.get("og:image", "")
    img_path = site.path_of(image) if image.startswith("http") else None
    return Result("social", 5, [
        Item("og:title", 1, 1.0 if meta.get("og:title") else 0.0, "missing"),
        Item("og:description", 1, 1.0 if meta.get("og:description") else 0.0, "missing"),
        Item("og:url matches canonical", 1, 1.0 if meta.get("og:url") and unquote(meta["og:url"]) == unquote(canon) else 0.0,
             f"og:url is {meta.get('og:url')!r}"),
        Item("og:image", 1, 1.0 if img_path and site.exists(img_path) else 0.0, f"og:image {image!r} missing or not absolute"),
        Item("og:image:alt", 0.5, 1.0 if meta.get("og:image:alt") else 0.0, "missing"),
        Item("og:locale", 0.5, 1.0 if meta.get("og:locale") else 0.0, "missing"),
        Item("og:site_name", 0.5, 1.0 if meta.get("og:site_name") else 0.0, "missing"),
        Item("twitter:card", 0.5, 1.0 if meta.get("twitter:card") else 0.0, "missing"),
    ])


def check_schema(p, site):
    sd = site.cfg["structured_data"]
    nodes, errors = ld_nodes(p.parser.jsonld)
    expected = list(sd["always"]) + ([] if p.path in sd["home_paths"] else list(sd["subpages"])) + p.cfg.get("schema", [])
    business_types = set(sd["local_business_types"])
    items = [Item("valid JSON-LD", 1, 0.0 if errors or not p.parser.jsonld else 1.0,
                  "; ".join(errors) if errors else "no JSON-LD on the page")]
    for want in dict.fromkeys(expected):
        if want == "LocalBusiness":
            found = [n for n in nodes if types_of(n) & business_types]
            check = lambda n: validate_fields(n, sd["local_business_fields"])
        elif want == "WebPage":
            found = [n for n in nodes if types_of(n) & WEBPAGE_TYPES]
            check = lambda n: validate_fields(n, ["name", "url", "inLanguage"])
        elif want == "WebSite":
            found = [n for n in nodes if "WebSite" in types_of(n)]
            check = lambda n: validate_fields(n, ["name", "url"])
        elif want == "BreadcrumbList":
            found = [n for n in nodes if "BreadcrumbList" in types_of(n)]
            check = validate_breadcrumbs
        elif want == "FAQPage":
            found = [n for n in nodes if "FAQPage" in types_of(n)]
            check = validate_faq
        elif want in ARTICLE_TYPES:
            found = [n for n in nodes if types_of(n) & ARTICLE_TYPES]
            check = lambda n: validate_fields(n, ["headline", "datePublished", "image", "author", "publisher"])
        else:
            found = [n for n in nodes if want in types_of(n)]
            check = lambda n: (1.0, [])
        if not found:
            items.append(Item(want, 1, 0.0, f"no {want} node"))
            continue
        frac, missing = max((check(n) for n in found), key=lambda r: r[0])
        items.append(Item(want, 1, frac, f"missing {missing}"))
    if not sd.get("allow_ratings", False):
        rated = [n for n in nodes if "aggregateRating" in n or types_of(n) & {"Review", "AggregateRating"}]
        items.append(Item("no unverified ratings", 0.5, 0.0 if rated else 1.0, "rating/review markup found"))
    return Result("structured data", 5, items)


PAGE_CHECKS = [check_title, check_description, check_h1, check_headings, check_content, check_readability,
               check_style, check_links, check_images, check_technical, check_social, check_schema]


# --------------------------------------------------------------------------- site checks

def inbound_links(site):
    inbound = defaultdict(lambda: {"content": set(), "nav": set()})
    for p in site.indexable:
        url = site.url_for(p.path)
        for a in p.parser.anchors:
            path = site.path_of(a["href"], url)
            if path and path != p.path:
                inbound[path]["content" if a["content"] else "nav"].add(p.path)
    return inbound


def site_checks(site):
    cfg = site.cfg
    results = []
    pages = site.indexable

    robots = site.dir / "robots.txt"
    txt = robots.read_text(encoding="utf-8") if robots.is_file() else ""
    lines = [l.strip() for l in txt.splitlines()]
    maps = [l.split(":", 1)[1].strip() for l in lines if l.lower().startswith("sitemap:")]
    map_ok = bool(maps) and all(m.startswith("https://") and site.path_of(m) and site.exists(site.path_of(m)) for m in maps)
    results.append(Result("robots.txt", 15, [
        Item("exists", 3, 1.0 if txt else 0.0, "no robots.txt in the build"),
        Item("user-agent rule", 1, 1.0 if any(l.lower().startswith("user-agent") for l in lines) else 0.0, "no User-agent line"),
        Item("does not block the site", 2, 0.0 if "disallow: /" in [l.lower() for l in lines] else 1.0, "Disallow: / blocks everything"),
        Item("sitemap reference", 2, 1.0 if maps and all(m.startswith("https://") for m in maps) else 0.0, "no absolute Sitemap: line"),
        Item("sitemap reference resolves", 2, 1.0 if map_ok else 0.0, f"Sitemap line(s) {maps} do not resolve"),
    ]))

    urls = site.sitemap_urls
    decoded = [unquote(u) for u in urls]
    paths = [site.path_of(u) for u in urls]
    unresolved = [u for u, pth in zip(urls, paths) if not pth or not site.exists(pth)]
    not_indexable = [pth for pth in paths if pth and (pth not in site.pages or not site.pages[pth].indexable)]
    listed = set(p for p in paths if p)
    unlisted = [p.path for p in pages if p.path not in listed]
    results.append(Result("sitemap", 20, [
        Item("parses", 2, 0.0 if site.sitemap_errors or not urls else 1.0, "; ".join(site.sitemap_errors) or "no URLs"),
        Item("every URL resolves", 2, 0.0 if unresolved else 1.0, f"{unresolved[:3]}"),
        Item("only indexable pages", 2, 0.0 if not_indexable else 1.0, f"lists {sorted(set(not_indexable))[:6]}"),
        Item("covers every indexable page", 2, 0.0 if unlisted else 1.0, f"missing {unlisted[:5]}"),
        Item("absolute https URLs", 1, 1.0 if urls and all(u.startswith(site.base) for u in urls) else 0.0, "URLs do not use the base URL"),
        Item("no duplicates", 1, 1.0 if len(decoded) == len(set(decoded)) else 0.0, "duplicate URLs"),
    ]))

    taxonomy = [p.path for p in site.pages.values() if p.kind == "taxonomy"]
    leaks = [pat for pat in cfg["site"].get("leak_files", []) if (site.dir / pat).exists()]
    four04 = [p for p in site.pages.values() if p.kind == "404"]
    open404 = [p.path for p in four04 if "noindex" not in p.robots]
    thin = [f"{p.path} ({len(words_of(p.main_text))} words)" for p in pages
            if p.profile != "legal" and len(words_of(p.main_text)) < 100]
    results.append(Result("thin or leaked pages", 10, [
        Item("no tag/category pages", 3, 0.0 if taxonomy else 1.0, f"{len(taxonomy)} built: {taxonomy[:4]}"),
        Item("no internal feeds", 2, 0.0 if leaks else 1.0, f"exposed: {leaks}"),
        Item("404 pages are noindex", 2, 0.0 if open404 else 1.0, f"indexable: {open404}"),
        Item("no thin pages", 3, 0.0 if thin else 1.0, f"{thin[:4]}"),
    ]))

    def uniq(values):
        values = [v for v in values if v]
        return len(set(values)) / len(values) if values else 0.0
    dup_titles = [t for t, c in Counter(p.title for p in pages).items() if c > 1]
    dup_desc = [d for d, c in Counter(p.description for p in pages if p.description).items() if c > 1]
    dup_h1 = [h for h, c in Counter(p.h1s[0]["text"] for p in pages if p.h1s).items() if c > 1]
    results.append(Result("duplicates", 15, [
        Item("unique titles", 2, uniq([p.title for p in pages]), f"duplicated: {dup_titles[:3]}"),
        Item("unique descriptions", 2, uniq([p.description for p in pages]), f"duplicated: {[d[:50] for d in dup_desc[:3]]}"),
        Item("unique H1s", 1, uniq([p.h1s[0]["text"] for p in pages if p.h1s]), f"duplicated: {dup_h1[:3]}"),
    ]))

    broken = sum(1 for p in pages for r in p.results for i in r.items
                 if i.label in ("no broken internal links", "image files exist") and i.fraction < 1)
    results.append(Result("broken links", 15, [
        Item("no broken links or images", 1, ramp(broken, 10, 0), f"{broken} page(s) with broken links or images"),
    ]))

    nap = cfg["nap"]
    no_tel = [p.path for p in pages if not any(a["href"].startswith("tel:") and
                                                 re.sub(r"[^\d+]", "", a["href"][4:]) == nap["phone"]
                                                 for a in p.parser.anchors)]
    no_addr = [p.path for p in pages if not (nap["street"] in p.all_text and nap["postal_code"] in p.all_text)]
    mismatched, schema_pages = [], 0
    for p in pages:
        nodes, _ = ld_nodes(p.parser.jsonld)
        biz = [n for n in nodes if types_of(n) & set(cfg["structured_data"]["local_business_types"])]
        if not biz:
            continue
        schema_pages += 1
        b = biz[0]
        want = {"telephone": nap["phone"], "address.streetAddress": nap["street"],
                "address.postalCode": nap["postal_code"], "address.addressLocality": nap["city"]}
        wrong = [k for k, v in want.items() if str(dig(b, k) or "").replace(" ", "") != v.replace(" ", "")]
        if wrong:
            mismatched.append(f"{p.path}: {wrong}")
    forbidden = []
    for rule in cfg["style"].get("forbidden", []):
        allow = re.compile(rule["allow"]) if rule.get("allow") else None
        for p in pages:
            for m in re.finditer(re.escape(rule["term"]), p.all_text):
                window = p.all_text[max(0, m.start() - 40): m.end() + 10]
                if not (allow and allow.search(window)):
                    forbidden.append(f"{p.path}: '{window.strip()[:60]}'")
    results.append(Result("name, address, phone", 10, [
        Item("phone link on every page", 2, 1 - len(no_tel) / len(pages) if pages else 0.0, f"missing on {no_tel[:4]}"),
        Item("address on every page", 2, 1 - len(no_addr) / len(pages) if pages else 0.0, f"missing on {no_addr[:4]}"),
        Item("structured data matches", 3, (1 - len(mismatched) / schema_pages) if schema_pages else 0.0,
             "; ".join(mismatched[:3]) or "no LocalBusiness markup anywhere"),
        Item("copy matches the address", 3, 0.0 if forbidden else 1.0,
             f"{len(forbidden)} conflicting mention(s), e.g. {forbidden[:2]}"),
    ]))

    groups = defaultdict(list)
    for p in pages:
        if p.focus and p.profile != "legal":
            groups[(p.lang, tuple(sorted(norm(t) for t in p.focus)))].append(p.path)
    clashes = [v for v in groups.values() if len(v) > 1]
    results.append(Result("keyword cannibalization", 5, [
        Item("one page per focus keyword", 1, 0.0 if clashes else 1.0, f"pages share a focus keyword: {clashes}"),
    ]))

    pattern = re.compile("|".join(re.escape(w) for w in cfg["style"]["placeholders"]), re.I)
    dirty = []
    for f in site.dir.rglob("*"):
        if f.suffix in (".html", ".xml", ".txt", ".json", ".webmanifest") and f.is_file():
            if pattern.search(f.read_text(encoding="utf-8", errors="replace")):
                dirty.append(f.relative_to(site.dir).as_posix())
    results.append(Result("template leftovers", 10, [
        Item("no placeholder text in any output file", 1, 0.0 if dirty else 1.0, f"found in {sorted(dirty)[:5]}"),
    ]))
    return results


def keyword_coverage(site):
    rows = []
    for lang, entries in site.cfg.get("keywords", {}).items():
        pages = [p for p in site.indexable if p.lang == lang]
        for kw in entries:
            terms = kw["terms"]
            in_title = [p.path for p in pages if match_terms(p.title, terms)[0] == 1]
            in_h1 = [p.path for p in pages if p.h1s and match_terms(p.h1s[0]["text"], terms)[0] == 1]
            in_body = [p.path for p in pages if match_terms(p.main_text, terms)[0] == 1]
            wanted = {norm(t) for t in terms}

            def rank(p):
                owns = bool(p.focus) and {norm(t) for t in p.focus} <= wanted
                return (2 * (p.path in in_title) + (p.path in in_h1) + owns, -len(p.path))
            candidates = [p for p in pages if p.path in in_title or p.path in in_h1]
            best = max(candidates, key=rank).path if candidates else "-"
            rows.append({"lang": lang, "keyword": kw["name"], "title": in_title, "h1": in_h1, "body": in_body,
                         "best": best})
    return rows


# --------------------------------------------------------------------------- driver

def build(source, base_url, dest):
    cmd = ["hugo", "--minify", "--quiet", "--destination", str(dest), "--baseURL", base_url]
    try:
        run = subprocess.run(cmd, cwd=source, capture_output=True, text=True)
    except FileNotFoundError:
        sys.exit("hugo is not installed or not on PATH.")
    if run.returncode != 0:
        sys.stderr.write(run.stdout + run.stderr)
        sys.exit(2)


def audit(site_dir, cfg):
    site = Site(site_dir, cfg)
    site.inbound = inbound_links(site)
    for p in site.indexable:
        p.results = [r for r in (chk(p, site) for chk in PAGE_CHECKS) if r is not None]
    site_results = site_checks(site)
    total = sum(r.weight for r in site_results)
    site_score = 100 * sum(r.weight * r.fraction for r in site_results) / total
    page_scores = [p.score for p in site.indexable]
    avg = sum(page_scores) / len(page_scores) if page_scores else 0.0
    overall = cfg["thresholds"]["page_share"] * avg + (1 - cfg["thresholds"]["page_share"]) * site_score
    return site, site_results, site_score, avg, overall


def result_json(r):
    return {"check": r.name, "weight": r.weight, "score": round(100 * r.fraction, 1), "notes": r.notes,
            "items": [{"label": i.label, "weight": i.weight, "score": round(100 * i.fraction, 1),
                       "message": i.message if i.fraction < 1 else ""} for i in r.items]}


def print_report(site, site_results, site_score, avg, overall, args):
    pages = sorted(site.indexable, key=lambda p: (p.lang != site.cfg["site"]["default_language"], p.path))
    skipped = [p for p in site.pages.values() if not p.indexable]
    print(paint(f"SEO audit for {site.base}", "1"))
    print(f"{len(site.pages)} HTML files, {len(pages)} indexable pages, {len(skipped)} skipped "
          f"({', '.join(sorted({p.kind if p.kind != 'page' else 'noindex' for p in skipped})) or 'none'})\n")
    print(paint("Pages", "1"))
    for p in pages:
        s = p.score
        print(f"  {paint(f'{s:5.1f}', score_color(s))}  {p.lang}  {p.path:<58.58} {p.title[:60]}")
        if args.page and args.page != p.path:
            continue
        for r in p.results:
            bad = [i for i in r.items if i.fraction < 1]
            if args.verbose:
                print(f"         {r.name:<16} {100 * r.fraction:5.1f}  " + "; ".join(r.notes))
                for i in r.items:
                    mark = paint("ok", "32") if i.fraction >= 1 else paint(f"{100 * i.fraction:.0f}%", "33")
                    print(f"            {mark:<6} {i.label}" + (f": {i.message}" if i.fraction < 1 else ""))
            elif bad:
                for i in bad:
                    print(f"         - {r.name}: {i.label} ({100 * i.fraction:.0f}%): {i.message}")
    print("\n" + paint("Site", "1"))
    for r in site_results:
        print(f"  {r.name:<26} {r.weight * r.fraction:5.1f} / {r.weight:g}")
        for i in r.items:
            if i.fraction < 1 or args.verbose:
                print(f"         - {i.label} ({100 * i.fraction:.0f}%)" + (f": {i.message}" if i.fraction < 1 else ""))
    print("\n" + paint("Keyword coverage (pages with the phrase in title / H1 / text)", "1"))
    for row in keyword_coverage(site):
        print(f"  {row['lang']}  {row['keyword']:<34} {len(row['title']):>2} / {len(row['h1']):>2} / {len(row['body']):>2}"
              f"   best: {row['best']}")
    print()
    print(f"  Average page score  {paint(f'{avg:5.1f}', score_color(avg))} / 100")
    print(f"  Site score          {paint(f'{site_score:5.1f}', score_color(site_score))} / 100")
    print(paint(f"  Overall SEO score   {overall:5.1f} / 100", "1;" + score_color(overall)))


def main():
    ap = argparse.ArgumentParser(description="Score the SEO of the Hugo site.")
    ap.add_argument("--site", type=Path, help="audit this existing build instead of running hugo")
    ap.add_argument("--source", type=Path, default=ROOT, help="Hugo project to build (default: repo root)")
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--json", type=Path, help="write the full report as JSON")
    ap.add_argument("--min-score", type=float, help="fail if any page scores below this")
    ap.add_argument("--min-site-score", type=float, help="fail if the site score is below this")
    ap.add_argument("--page", help="only print details for this URL path")
    ap.add_argument("-v", "--verbose", action="store_true", help="print every check, not only the failing ones")
    args = ap.parse_args()

    cfg = tomllib.loads(args.config.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="seo-audit-") as tmp:
        site_dir = args.site
        if site_dir is None:
            site_dir = Path(tmp) / "public"
            build(args.source, cfg["site"]["base_url"], site_dir)
        site, site_results, site_score, avg, overall = audit(site_dir.resolve(), cfg)
        print_report(site, site_results, site_score, avg, overall, args)

    if args.json:
        report = {
            "base_url": site.base, "overall": round(overall, 1), "average_page_score": round(avg, 1),
            "site_score": round(site_score, 1), "site": [result_json(r) for r in site_results],
            "pages": [{"path": p.path, "lang": p.lang, "profile": p.profile, "title": p.title,
                       "score": round(p.score, 1), "checks": [result_json(r) for r in p.results]}
                      for p in site.indexable],
            "keywords": keyword_coverage(site),
        }
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    min_page = args.min_score if args.min_score is not None else cfg["thresholds"]["page"]
    min_site = args.min_site_score if args.min_site_score is not None else cfg["thresholds"]["site"]
    failing = [p.path for p in site.indexable if p.score < min_page]
    if failing or site_score < min_site:
        print(paint(f"\n  Below target: {len(failing)} page(s) under {min_page:g}"
                    + (f", site under {min_site:g}" if site_score < min_site else ""), "31"))
        sys.exit(1)
    print(paint(f"\n  All pages at {min_page:g}+ and the site at {min_site:g}+.", "32"))


if __name__ == "__main__":
    main()
