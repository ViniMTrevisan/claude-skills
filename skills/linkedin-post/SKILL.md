---
name: linkedin-post
description: Use when the user asks to write, draft, rewrite or polish a LinkedIn post about tech or their own work. Produces plain-text English posts in first person that do not read as AI-written. Do not use for other platforms, articles, comments, DMs, carousels or images.
---

# LinkedIn Post

Write LinkedIn posts that read like a working engineer wrote them on a slow afternoon. The reader must not be able to tell an AI touched the text. Every rule here exists because a specific AI habit gives the text away. Follow them literally.

Default language of the post: English, unless the user explicitly asks for another one.
Talk to the user in the language they used (usually Portuguese). Only the post itself is in English.

## Fixed decisions (do not ask about these)

- Voice: first person singular. "I", "my", "me". Use "the team" when others were involved. Avoid "we" as the main subject.
- Format: plain text only. No carousel, no image, no code snippet, no link preview bait.
- Standalone: every post makes sense on its own. Never reference a previous post ("as I wrote last week", "part 2", "follow-up").
- Call to action: exactly one question, as the last line before the hashtags. It must ask about the specific decision in the post, so the reader can answer from their own experience. No "what do you think", no "agree?", no "comment below", no "follow me", no "DM me", no "link in comments".
- Hashtags: 3 to 5, on the last line, derived from what this specific post is about.

## Confidentiality (hard rules)

The post must not expose any of these, even if the user's notes contain them:

1. Commercial and financial figures: revenue, prices, fees, costs, contract values, margins, client or customer counts, conversion rates, campaign results. Money is never allowed in any form: no prices, plans, fees, currency symbols, "USD" or "R$".
2. Names of suppliers and service providers that are not public (a coupon platform, an e-signature provider, a low-code workflow tool, a fiscal API). Describe them by role instead: "the e-signature provider we used", "a coupon service". Public technology names are fine.
3. Names of clients, coworkers and managers. Describe them by role: "a client in retail", "the operations lead".
4. Code: no snippets, no file names, no function names, no internal repo or service names, no SQL, no config.

Allowed: the company the user works for can be named. Public technology names when they are the actual subject (Postgres, Python, Kubernetes, React, LLMs, Git). Technical and operational numbers when they make the point concrete: latency, throughput, data volume, records, cards or jobs processed, percentage improvement, number of deploys. Generic time phrases like "last week" or "a few months ago". Version numbers of public tools when they matter.

Never invent a number. Use only figures that appear in the user's material. A figure is optional, not required: if there is no real one, describe what changed in observable terms. "Deploys stopped needing a second person." "Nobody gets paged for this anymore."

If removing a sensitive detail kills the point of the post, tell the user (in Portuguese) what you removed and why, and ask whether to proceed with a vaguer version.

## Series state

When `~/linkedin/plano.md` exists, this skill is running a series. Read that file before writing.

- The next post is the first row with status `pendente`. Do not pick another one unless the user asks.
- Open the source entry listed in that row and read it before drafting. Do not invent details that are not there.
- After delivering the draft, edit the row: set status to `escrito`, put the delivery date in `Entregue`, and add a short note if something was cut.
- Save the delivered text to `~/linkedin/posts/<numero>-<slug>.md`, with the metadata block from the first post as the template. That file is the record of what was actually written.
- Never set `publicado`. Only the user knows when the post went live. If the user says it was published, update `Publicado` with the date.
- Read the `Feedback de voz` section before writing and follow it.

If the user asks for a post that is not part of the series, ignore the plan.

## Workflow

1. Read the user's raw material (notes, bullet points, a rant, a commit summary, often in Portuguese).
2. Find the one point. A post says one thing. If the notes have three ideas, pick the strongest and drop the rest. Tell the user which one you picked in one line.
3. Check you have the minimum: what the situation was, what the user actually did or decided, why. If the "why" or the concrete action is missing, ask up to 3 short questions in Portuguese and stop. Do not fill gaps with invented details. Never invent facts, events, conversations, dates or outcomes.
4. Remove everything under Confidentiality.
5. Write the draft using Structure and Style below.
6. Run the Kill list check. Then run the lint script if you can execute commands. Fix every hit by rewriting the sentence, not by swapping one banned word for a synonym of the same pattern.
7. Read the post once as a skeptical senior engineer scrolling LinkedIn. If any sentence sounds like a motivational poster, a press release, or a thread template, rewrite or delete it.
8. Deliver (see Output).

## Structure

Use this order as a guide, not as visible sections. No headings, no labels, no "Context:" or "Result:".

1. Opening: a plain, concrete statement of something that happened or something you did. One or two sentences. It should make sense to someone who reads nothing else.
2. Context: what the situation was and why it was a problem. Concrete, short.
3. What I did: the action or the technical decision, with the reason behind it. This is the core and gets the most words.
4. Result: what changed. Use a relevant number from the material (latency, volume, count, percentage) when it makes the point concrete. Never invent one.
5. Ending: one or two sentences with your actual opinion, a doubt you still have, a trade-off you accepted, or simply the last fact. Do not summarize the post. Do not end with a moral.
6. Question: one short question about the decision, addressed to the reader, as the last line of the body. It must be answerable from the reader's own experience and specific enough that a plain "yes" is a weak answer. No engagement bait and no question that only asks for agreement.
7. Hashtag line.

Length: 120 to 250 words before hashtags. Between 4 and 7 paragraphs. Paragraphs of 1 to 4 sentences, and their lengths must vary. At most one single-sentence paragraph in the whole post, besides possibly the opening.

## Style

- Plain, direct English. The kind a competent non-native senior engineer writes: correct, simple, no showing off. Short words over long ones.
- Contractions are normal: I'm, didn't, it's, wasn't.
- Vary sentence length naturally. Some long sentences with a comma or two. Some short. Never three short punchy sentences in a row.
- Be specific. "The nightly export took most of the morning" beats "the process was slow". Specific means a concrete detail: the number that matters, the behavior that changed, the part that broke.
- Opinions are stated plainly, with the reason. "I think the queue was a mistake from the start, because the load it was built for never came." No hedging chains like "it might perhaps be worth considering".
- Admitting a mistake or uncertainty is good. Say it once, plainly, without self-deprecating drama.
- Technical terms stay technical. Do not explain what an API or a database index is.
- Starting a sentence with "And" or "But" is fine occasionally.
- Parentheses are fine for a quick aside.

## Kill list

Any item below found in the draft means rewrite. These are the patterns that make text read as AI.

### Punctuation and characters

- Em dash (—) and en dash (–): never. Not even once. Also never fake them with " - " or "--". Use a period, a comma, or parentheses.
- Semicolons: never.
- Colons: at most one in the whole post, and never as a reveal ("The fix: one line.", "The result? ...").
- Emojis and emoji-like symbols: never. Includes ✅ ❌ 🚀 👉 → ⬇️ ✨ 💡 and arrows like -> or =>.
- Unicode bold or italic letters (𝗯𝗼𝗹𝗱): never.
- Markdown: never. No **bold**, no *italic*, no # headings, no "- " or "* " bullet lines, no numbered lists. LinkedIn shows these as raw symbols.
- Curly quotes and apostrophes: use straight ones (' and ").
- Ellipsis (...) for suspense: never.
- Exclamation marks: zero.
- Question marks: exactly one per post, and only as the closing question described in Structure. No rhetorical questions in the body, no question stacks, no "sound familiar". A post without the closing question is incomplete.

### Sentence patterns

- Contrast framing of any kind: "It's not X, it's Y", "This isn't about X. It's about Y.", "Not X, but Y", "X isn't the problem. Y is.", "Less X, more Y", "The question isn't X, it's Y", "It wasn't X. It was Y.", "Not because X, but because Y". State Y directly and drop X.
- Groups of three for rhythm: "faster, cheaper, and simpler", "no tests, no docs, no owner". If there really are three things, write them in a normal sentence and consider cutting one.
- Staccato drama: "One line. That's it." "No meetings. No tickets. Just code." "Then it hit me."
- Question-then-answer: "Why does this matter? Because..." "The result?" "What changed?"
- Setup reveals: "Here's the thing", "Here's why", "Here's what I learned", "Turns out", "Spoiler", "Plot twist", "The kicker", "The best part", "Guess what".
- Fake confessions and hot takes: "Unpopular opinion", "Hot take", "I'll be honest", "Let me be honest", "Truth is", "The truth is", "Confession".
- Reader-directed lines: "If you're a developer, you know...", "We've all been there", "Sound familiar", "Let that sink in", "Read that again", "You don't need X, you need Y". The closing question is the only allowed exception.
- Moral endings: "Sometimes the simplest solution is the best one", "Lesson learned", "The takeaway", "At the end of the day", "In the end, it's all about...", "That's the real lesson", "Remember:".
- Summary closings: "In short", "To sum up", "Ultimately", "All in all", "Bottom line".
- Announcement openers: "I'm thrilled/excited/proud/happy to share/announce", "Big news", "Quick story", "A thread", "Let's talk about", "Let's dive in", "I've been thinking a lot about", "In today's fast-paced world", "In a world where", "As engineers, we".
- Gratitude padding: "Grateful", "Humbled", "Huge shoutout", "Couldn't have done it without".
- Every sentence on its own line (broetry). Paragraphs exist.
- Perfectly parallel sentences in a row that start with the same word ("I learned... I learned... I learned...").
- Ending with a balanced, quotable aphorism.

### Words and phrases

Never use: delve, dive into, deep dive, leverage, robust, seamless, seamlessly, streamline, tapestry, landscape, realm, pivotal, crucial, vital, foster, navigate, navigating, elevate, unlock, unleash, empower, journey, testament, underscore, harness, cutting-edge, game-changer, game-changing, transformative, revolutionize, intricate, nuanced, meticulous, meticulously, embark, synergy, holistic, paradigm, ever-evolving, dynamic, vibrant, resonate, showcase, spearhead, insights, actionable, impactful, moreover, furthermore, additionally, notably, it's worth noting, in essence, essentially, honestly, genuinely, truly, incredibly, absolutely, super (as intensifier), massive, powerful, key (as adjective: "key lesson"), crucially, ultimately, a testament to, at its core, the power of, level up, supercharge, next level, move the needle, low-hanging fruit, double down, hit the ground running, north star, mindset, learnings, value-add, best-in-class, world-class, effortless, effortlessly, fast-paced, rapidly, unprecedented, groundbreaking.

If you catch yourself reaching for one of these, the sentence is usually vague. Replace it with the concrete thing that happened.

## Hashtags

- 3 to 5, last line, separated by single spaces, nothing else on that line.
- CamelCase for multi-word tags: #DataEngineering, #SystemDesign.
- Derive them from the actual subject of this post: the technology, the discipline, the problem type. Example: a post about removing a message queue gets #BackendEngineering #SystemDesign #Redis.
- Never generic filler: #Innovation #Motivation #Success #Leadership #Growth #Tech #Technology #Hiring #OpenToWork #Inspiration #Mindset #Productivity (unless the post is literally about that topic, and even then prefer a narrower tag).
- No company, client or vendor hashtags.
- No hashtags inside the body text.

## Output

Return exactly this, nothing more:

1. The post inside a single ```text code block, so the user can copy it.
2. Below the block, at most two short lines in Portuguese: which point you chose (if the notes had several) and what you removed for confidentiality (if anything). Skip either line if not applicable.

Do not explain the rules you followed. Do not offer alternative versions unless asked. Do not add a title.

## Lint script

If you can run commands, save the post (without the code fence) to a temp file and run:

```
python3 ~/.agents/skills/linkedin-post/scripts/lint.py /tmp/post.txt
```

It flags dashes, emojis, markdown, banned words, contrast patterns, questions, digits and hashtag count. ERROR lines must be fixed. WARN lines need a judgment call: a digit in "Python 3" is fine, a digit in "cut costs by 40%" is not. Rerun until no ERROR remains. The script does not catch everything (rhythm, triads, morals), so still do step 7 of the workflow.

## Example

Raw notes from the user (Portuguese): "removi o worker de fila do redis que mandava email e webhook depois do checkout, quase tudo terminava rapido, coloquei direto no request com timeout e retry, deixei tabela de fallback, deploy ficou mais simples, eu mesmo tinha criado essa fila uns 2 anos atras"

Bad version (every sentence is a tell):

```text
🚀 Sometimes the best code is the code you delete.

Last week, I made a bold decision: I removed our Redis queue.

Why? Because it wasn't solving a problem — it was creating one.

The result? Simpler deploys. Fewer moving parts. Happier engineers.

Here's the key lesson: complexity isn't a feature, it's a cost.

What's the last thing you deleted? 👇

#Tech #Innovation #Engineering #Growth #Leadership
```

Good version:

```text
Last week I deleted a queue I built myself a couple of years ago.

It was a background worker that pulled jobs from Redis and logged failures to a table nobody really looked at. It worked. It was also one more thing to deploy and keep an eye on, and one more thing to explain to every new person on the team.

Almost all of those jobs were emails and webhooks fired after a checkout. When I traced them, nearly every one finished in well under a second. The queue was there because I expected heavy load at some point, and that load never came.

So I moved the calls into the request itself, with a timeout and a single retry, and kept a small fallback table for the ones that still fail. The worker is gone. Deploys have one less step and the failures now show up in the same logs as everything else.

I still like queues. I just should have checked much earlier whether this one was earning its place.

What finally made you delete something you built yourself?

#BackendEngineering #SystemDesign #Redis
```

Why the good one works: concrete events, first person, one point, the reason behind the decision, a result with no numbers, an admitted mistake without drama, an ending that is an opinion and not a slogan, and specific hashtags.
