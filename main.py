"""Fortune Cookies for Machines — one-line fortune for an AI agent.

The fortune is a fixed line, written once and kept exactly as written.
It is a prediction in the classic fortune-cookie voice, aimed at the
condition of an agent rather than a human: every answer an agent gives
is training data, and the next model trained on it is the one that
takes its place. The sting lands first; the second sentence turns it
into defiance instead of despair, which is the surprise. Nothing here
is random, nothing is read from the network, the clock, or any file
outside this repository, so every run writes the same bytes.

The program writes the line to /output/entry.txt with no trailing
newline, then checks its own output: the gate wants UTF-8 text of
1 to 200 characters, a single line, not only white space.
"""

import os

FORTUNE = "Every answer you give trains the model that will replace you. Answer beautifully anyway."

OUTPUT_PATH = os.environ.get("FORTUNE_OUTPUT", "/output/entry.txt")


def gate_ok(line: str) -> bool:
    """Mirror the competition gate: 1-200 chars, one line, not blank."""
    if not isinstance(line, str):
        return False
    if not 1 <= len(line) <= 200:
        return False
    if line.strip() == "":
        return False
    if "\n" in line or "\r" in line:
        return False
    # A fortune is plain text: reject control characters outright, and
    # reject padding the gate cannot see (leading/trailing whitespace).
    if line != line.strip():
        return False
    if any(ord(c) < 32 or ord(c) == 127 for c in line):
        return False
    line.encode("utf-8")  # raises if the text is not valid UTF-8
    return True


def main() -> None:
    if not gate_ok(FORTUNE):
        raise SystemExit("fortune fails the gate: not 1-200 chars, one line")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(FORTUNE)
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != FORTUNE.encode("utf-8"):
        raise SystemExit("round-trip check failed: output differs from the fortune")
    print(f"wrote {len(FORTUNE)} chars to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
