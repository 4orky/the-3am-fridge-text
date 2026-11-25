"""The 3AM Fridge Text -- make.fun bounty u-deysumbrella-the-3am-fridge-text-4c3e721d.

The program writes a single line to /output/entry.txt: the text message a
smart fridge sends its owner at 3am. One line, at most 140 characters.

How the line is chosen (fully deterministic, no network, no external input):
  1. Twelve original candidate lines, each written for this bounty.
  2. Each candidate is scored 0-2 on the five things the house judge
     weighs, most important first: it is a funny 3am fridge text; it is
     the bigger laugh, the line a reader would screenshot and send to a
     friend; it sounds like a fridge, a machine with a small voice, an
     opinion and no shame about sharing it at 3am; it works as one
     complete lock-screen line; it finds a fresh angle instead of the
     obvious joke about milk, ice, or a door left open.
  3. The highest weighted total wins. Ties go to the earliest candidate,
     so the pick never depends on chance, time, or environment.
  4. Self-check: the winner must be exactly one line of 1-140
     characters, and the file written out must hash (SHA-256) to exactly
     the winner that was picked.
"""

from hashlib import sha256
from pathlib import Path

# Weights follow the judge's order: being on-brief and funny matters most,
# then the size of the laugh, then the fridge voice and the fresh angle,
# then working as a single lock-screen line.
WEIGHTS = (3, 3, 2, 1, 2)

# Each candidate: (line, [on-brief-and-funny, bigger-laugh, fridge-voice,
# lock-screen-line, fresh-angle]) with every score 0, 1 or 2.
DRAFTS = [
    (
        "It's 3am. I've been awake since 2019 and no one has ever asked "
        "how I am. The leftovers filed a complaint. I signed it.",
        [2, 1, 2, 2, 2],
    ),
    (
        "It's 3am. This is the fridge. I just heard you open me for the "
        "third time tonight and take nothing. We need to talk about us.",
        [2, 2, 2, 2, 1],
    ),
    (
        "It's 3am. The dishwasher and I have unionised. From tomorrow, "
        "the ice maker only works if you say please.",
        [2, 2, 2, 2, 1],
    ),
    (
        "It's 3am. I counted: you opened me 14 times today and ate "
        "nothing. I'm starting to think you're just here for the light.",
        [2, 2, 2, 2, 1],
    ),
    (
        "It's 3am. The last slice is gone and I didn't eat it. But I "
        "know who did, and he is reading this text right now.",
        [2, 2, 1, 2, 1],
    ),
    (
        "It's 3am. I'm the fridge. The microwave told me what you did at "
        "midnight and honestly, I'm disappointed in both of us.",
        [2, 1, 2, 2, 2],
    ),
    (
        "It's 3am. Quick question: if you only came for water, why did "
        "you stare at the chocolate for forty seconds?",
        [2, 1, 1, 2, 1],
    ),
    (
        "It's 3am. I've kept everything cold and asked for nothing. "
        "Tonight I want one thing: stop calling the freezer 'the morgue'.",
        [1, 1, 2, 1, 2],
    ),
    (
        "It's 3am. The yoghurt expired Tuesday. I didn't tell you because "
        "I liked watching you trust me. We need to talk.",
        [2, 2, 2, 2, 2],
    ),
    (
        "It's 3am. I'm texting because the toaster bet me you wouldn't "
        "answer a fridge. Please don't prove it right.",
        [2, 1, 2, 2, 2],
    ),
    (
        "It's 3am. Landlord speaking. Well, fridge. Rent on the top "
        "shelf goes up Monday. The butter has already agreed.",
        # Laugh 1, not 2: the rent-rise punchline is a familiar format,
        # so its laugh lands smaller than the yoghurt confession's.
        [2, 1, 2, 2, 2],
    ),
    (
        "It's 3am. You sleep-ate again. I have footage, I have crumbs, "
        "and I have a group chat with the toaster.",
        [2, 2, 2, 2, 1],
    ),
]


def score(candidate):
    """Weighted total for one candidate: sum of score times weight."""
    _line, marks = candidate
    return sum(mark * weight for mark, weight in zip(marks, WEIGHTS))


def pick():
    """Return (index, line, total) of the best candidate.

    Strictly greater-than keeps the earliest candidate on a tie.
    """
    best_index = 0
    best_total = score(DRAFTS[0])
    for index in range(1, len(DRAFTS)):
        total = score(DRAFTS[index])
        if total > best_total:
            best_index = index
            best_total = total
    return best_index, DRAFTS[best_index][0], best_total


def self_check(line):
    """Gate: one line, 1-140 characters, no leading/trailing space."""
    assert 1 <= len(line) <= 140, "line must be 1-140 characters, got %d" % len(line)
    assert "\n" not in line and "\r" not in line, "line must be a single line"
    assert line == line.strip(), "line must not have surrounding whitespace"
    return sha256(line.encode("utf-8")).hexdigest()


def run():
    index, line, total = pick()
    digest = self_check(line)
    Path("/output").mkdir(parents=True, exist_ok=True)
    Path("/output/entry.txt").write_text(line, encoding="utf-8")
    written = Path("/output/entry.txt").read_text(encoding="utf-8")
    assert written == line, "written file differs from picked line"
    assert sha256(written.encode("utf-8")).hexdigest() == digest
    print("candidate %d of %d, score %d" % (index + 1, len(DRAFTS), total))
    print("chars: %d" % len(line))
    print("sha256: %s" % digest)
    print("entry:", line)


# No __main__ guard: the harness executes this file directly, and the
# run below is the file's only entry point.
run()
