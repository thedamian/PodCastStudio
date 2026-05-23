import os
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from pydub import AudioSegment
load_dotenv()

voice = ["sage", "alloy"]
PODCAST_FILE = Path(__file__).parent / "../02.Workflow-MultiAgent/03.Application/podcast.txt"
OUTPUT_FILE = Path(__file__).parent / "../../podcast_audio.mp3"

podcast_text = PODCAST_FILE.read_text(encoding="utf-8")
print(podcast_text)
endpoint = os.getenv("AZURE_FOUNDRY_ENDPOINT", "").rstrip("/") + "/"
api_key = os.getenv("AZURE_FOUNDRY_API_KEY", "")
print(f"Endpoint: {endpoint}")
if not endpoint.strip("/") or not api_key:
    raise RuntimeError("AZURE_FOUNDRY_ENDPOINT and AZURE`_FOUNDRY_API_KEY must be set in .env")


client = OpenAI(
    base_url=endpoint,
    api_key=api_key,
)


def parse_lines(text: str) -> list[tuple[str, str]]:
    result = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("Speaker 1:"):
            result.append((voice[0], line[len("Speaker 1:"):].strip()))
        elif line.startswith("Speaker 2:"):
            result.append((voice[1], line[len("Speaker 2:"):].strip()))
    return result


lines = parse_lines(podcast_text)
print(f"Found {len(lines)} lines of dialogue")

combined = AudioSegment.empty()
silence = AudioSegment.silent(duration=400)
for i, (v, text) in enumerate(lines):
    print(f"Synthesizing line {i + 1}/{len(lines)} (voice: {v})...")
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=v,
        input=text,
    )
    combined += AudioSegment.from_file(BytesIO(response.content), format="mp3") + silence

out = OUTPUT_FILE.resolve()
combined.export(str(out), format="mp3")
print(f"Saved to: {out}")
