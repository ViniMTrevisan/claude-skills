#!/usr/bin/env python3
"""Lint a LinkedIn post draft for AI tells. Usage: lint.py FILE (or stdin). Exit 1 on any ERROR."""
import re
import sys

BANNED_WORDS = """delve|dive into|deep dive|leverage|leveraging|robust|seamless|seamlessly|streamline|tapestry|landscape|realm|
pivotal|crucial|crucially|vital|foster|navigate|navigating|elevate|unlock|unleash|empower|journey|testament|underscore|harness|
cutting-edge|game-changer|game-changing|transformative|revolutionize|intricate|nuanced|meticulous|meticulously|embark|synergy|
holistic|paradigm|ever-evolving|dynamic|vibrant|resonate|showcase|spearhead|insights|actionable|impactful|moreover|furthermore|
additionally|notably|it's worth noting|in essence|essentially|honestly|genuinely|truly|incredibly|absolutely|massive|powerful|
ultimately|at its core|the power of|level up|supercharge|next level|move the needle|low-hanging fruit|double down|
hit the ground running|north star|mindset|learnings|value-add|best-in-class|world-class|effortless|effortlessly|fast-paced|
rapidly|unprecedented|groundbreaking|key lesson|key takeaway|takeaway|lesson learned|at the end of the day|in short|to sum up|
all in all|bottom line|here's the thing|here's why|here's what|turns out|spoiler|plot twist|the kicker|the best part|guess what|
unpopular opinion|hot take|i'll be honest|let me be honest|truth is|let that sink in|read that again|sound familiar|
we've all been there|thrilled|excited to|proud to|happy to share|big news|let's dive|let's talk about|i've been thinking a lot|
in today's|in a world where|as engineers, we|grateful|humbled|shoutout|couldn't have done it without|super """
BANNED_RE = re.compile(r"\b(" + BANNED_WORDS.replace("\n", "").strip() + r")\b", re.I)

CONTRAST = [
    r"\b(it|this|that)(\s+i|')s\s+not\b[^.]*[,.]\s*(it|this|that)(\s+i|')s\b",
    r"\b(isn't|wasn't|is not|was not)\b[^.]*[.,;\u2014\u2013-]\s*(it|this|that)('s|\s+is|\s+was)\b",
    r"\bnot\b[^.,]*,\s*but\b",
    r"\bnot because\b",
    r"\bless\s+\w+,\s*more\b",
    r"\bisn't the (problem|point|question)\b",
    r"\bthe (question|problem|point) (isn't|is not)\b",
    r"\byou don't need\b[^.]*,\s*you need\b",
]

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F900-\U0001F9FF←-⇿⬀-⯿️‍]"
)
UNICODE_STYLED = re.compile("[\U0001D400-\U0001D7FF]")


def main():
    text = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    text = text.strip().strip("`").removeprefix("text").strip()
    errors, warns = [], []

    def err(msg):
        errors.append(msg)

    def warn(msg):
        warns.append(msg)

    if re.search("[—–]", text):
        err("em/en dash found")
    if re.search(r"\s-{1,2}\s|--", text):
        err("fake dash ' - ' or '--' found")
    if ";" in text:
        err("semicolon found")
    if "!" in text:
        err("exclamation mark found")
    if "..." in text or "…" in text:
        err("ellipsis found")
    if re.search("[“”‘’]", text):
        err("curly quotes/apostrophes found, use straight ones")
    if EMOJI_RE.search(text):
        err("emoji or arrow symbol found")
    if re.search(r"->|=>", text):
        err("ascii arrow found")
    if UNICODE_STYLED.search(text):
        err("unicode bold/italic letters found")
    if re.search(r"\*\*|__|^#{1,6}\s|^\s*[-*•]\s|^\s*\d+[.)]\s", text, re.M):
        err("markdown or list formatting found")

    lines = text.splitlines()
    tag_line = lines[-1].strip() if lines else ""
    body = "\n".join(lines[:-1]) if tag_line.startswith("#") else text
    tags = re.findall(r"#\w+", tag_line) if tag_line.startswith("#") else []
    if not tags:
        err("last line must be hashtags")
    elif not 3 <= len(tags) <= 5:
        err(f"{len(tags)} hashtags, need 3 to 5")
    if tag_line.startswith("#") and re.sub(r"#\w+|\s", "", tag_line):
        err("hashtag line has other text")
    if re.search(r"#\w", body):
        err("hashtag inside body")
    generic = {"innovation", "motivation", "success", "leadership", "growth", "tech", "technology",
               "hiring", "opentowork", "inspiration", "mindset", "productivity"}
    for t in tags:
        if t[1:].lower() in generic:
            err(f"generic hashtag {t}")

    for m in BANNED_RE.finditer(body):
        err(f"banned phrase: '{m.group(0)}'")
    for pat in CONTRAST:
        for m in re.finditer(pat, body, re.I):
            err(f"contrast pattern: '{m.group(0)[:70]}'")

    paras = [p for p in re.split(r"\n\s*\n", body) if p.strip()]
    q = body.count("?")
    if q == 0:
        err("missing closing question")
    elif q > 1:
        err(f"{q} question marks, exactly 1 closing question allowed")
    elif paras and "?" not in paras[-1]:
        err("question must be in the last paragraph")
    if body.count(":") > 1:
        err("more than one colon")
    elif ":" in body:
        warn("colon found, make sure it is not a reveal")
    if re.search(r"[$€£]|R\$|\bUSD\b|\bBRL\b", body):
        err("currency found")
    for m in re.finditer(r"\S*\d\S*", body):
        warn(f"digit in '{m.group(0)}', use only if it is a real metric or public version")

    words = len(body.split())
    if not 120 <= words <= 250:
        err(f"{words} words in body, need 120 to 250")
    if not 4 <= len(paras) <= 7:
        err(f"{len(paras)} paragraphs, need 4 to 7")
    sentences = [s for s in re.split(r"(?<=[.?])\s+", body) if s.strip()]
    run = 0
    for s in sentences:
        run = run + 1 if len(s.split()) <= 5 else 0
        if run == 3:
            err("three short sentences in a row (staccato)")
    single = sum(1 for p in paras[1:-1] if len(re.findall(r"[.?](\s|$)", p.strip())) <= 1)
    if single > 1:
        warn(f"{single} single-sentence paragraphs after the opening, max 1")
    starts = [s.split()[0].lower() for s in sentences if s.split()]
    for i in range(len(starts) - 2):
        if starts[i] == starts[i + 1] == starts[i + 2] and starts[i] not in {"i", "the", "it"}:
            warn(f"three sentences in a row start with '{starts[i]}'")

    for e in errors:
        print("ERROR", e)
    for w in warns:
        print("WARN ", w)
    print(f"--- {len(errors)} errors, {len(warns)} warnings, {words} words, {len(paras)} paragraphs")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
