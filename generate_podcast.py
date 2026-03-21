import os
import requests
import anthropic
import xml.etree.ElementTree as ET

NEWSAPI_KEY = os.environ["NEWSAPI_KEY"]
ANTHROPIC_KEY = os.environ["ANTHROPIC_KEY"]
ELEVENLABS_KEY = os.environ["ELEVENLABS_KEY"]
ELEVENLABS_VOICE_ID = os.environ["ELEVENLABS_VOICE_ID"]

# Step 1: Scrape news from multiple sources
def get_news():
    articles = []

    # NewsAPI - India headlines
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&pageSize=10&apiKey={NEWSAPI_KEY}"
        r = requests.get(url).json()
        for a in r.get("articles", []):
            if a.get("title"):
                articles.append(f"- {a['title']}")
        print(f"NewsAPI: {len(articles)} articles")
    except Exception as e:
        print(f"NewsAPI error: {e}")

    # Hacker News - Tech & AI
    try:
        hn = requests.get("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=10").json()
        hn_count = 0
        for h in hn.get("hits", []):
            if h.get("title"):
                articles.append(f"- {h['title']}")
                hn_count += 1
        print(f"HackerNews: {hn_count} articles")
    except Exception as e:
        print(f"HackerNews error: {e}")

    # Google News RSS - AI & Tech India
    try:
        rss = requests.get(
            "https://news.google.com/rss/search?q=artificial+intelligence+india&hl=en-IN&gl=IN&ceid=IN:en",
            timeout=10
        ).text
        root = ET.fromstring(rss)
        rss_count = 0
        for item in root.findall(".//item")[:10]:
            title = item.find("title")
            if title is not None:
                articles.append(f"- {title.text}")
                rss_count += 1
        print(f"Google News AI: {rss_count} articles")
    except Exception as e:
        print(f"Google News error: {e}")

    # Google News RSS - Business India
    try:
        rss2 = requests.get(
            "https://news.google.com/rss/search?q=india+business+economy&hl=en-IN&gl=IN&ceid=IN:en",
            timeout=10
        ).text
        root2 = ET.fromstring(rss2)
        rss2_count = 0
        for item in root2.findall(".//item")[:8]:
            title = item.find("title")
            if title is not None:
                articles.append(f"- {title.text}")
                rss2_count += 1
        print(f"Google News Business: {rss2_count} articles")
    except Exception as e:
        print(f"Google News Business error: {e}")

    return "\n".join(articles[:30])

# Step 2: Generate podcast script with Claude
def generate_script(news):
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"""You are a warm, engaging podcast host creating a 20-minute daily briefing for a professional in Delhi, India who has a 3-hour daily commute.

Here are today's top stories:
{news}

Create a natural, conversational podcast script that:
- Starts with a warm good morning greeting mentioning it is a weekday morning in Delhi
- Covers the top 8 to 10 stories in a flowing connected way
- Groups related stories together naturally
- Uses simple spoken language, no bullet points, no headers
- Has smooth transitions between topics
- Ends with a motivating sign-off for the commute ahead
- Feels like a knowledgeable friend briefing you, not a news reader

Write only the spoken words, nothing else. No stage directions."""
        }]
    )
    return message.content[0].text

# Step 3: Convert script to audio via ElevenLabs
def text_to_speech(script):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": script,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    r = requests.post(url, headers=headers, json=data)
    if r.status_code == 200:
        with open("podcast.mp3", "wb") as f:
            f.write(r.content)
        print("Audio saved as podcast.mp3")
    else:
        print(f"ElevenLabs error: {r.status_code} - {r.text}")
        raise Exception("Audio generation failed")

# Run everything
print("Starting podcast generation...")

print("Fetching news...")
news = get_news()
print(f"Total: {len(news.splitlines())} stories collected")

print("Generating script with Claude...")
script = generate_script(news)
print(f"Script ready: {len(script)} characters")

print("Converting to audio...")
text_to_speech(script)

print("Podcast generation complete!")
