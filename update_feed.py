from datetime import datetime

USERNAME = "divanshusaxena-AI"
REPO = "AI-daily-podcast"
BASE_URL = f"https://{USERNAME}.github.io/{REPO}"

now = datetime.utcnow()
pub_date = now.strftime("%a, %d %b %Y %H:%M:%S +0000")
date_title = now.strftime("%d %b %Y")

feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>My Daily Podcast</title>
    <description>Personal AI generated daily briefing for Delhi commute</description>
    <language>en-in</language>
    <itunes:author>Divansh</itunes:author>
    <itunes:category text="News"/>
    <item>
      <title>Daily Briefing - {date_title}</title>
      <description>Your AI generated daily news briefing for {date_title}</description>
      <enclosure url="{BASE_URL}/podcast.mp3" type="audio/mpeg"/>
      <guid>{BASE_URL}/podcast.mp3?date={now.strftime('%Y%m%d')}</guid>
      <pubDate>{pub_date}</pubDate>
      <itunes:duration>20:00</itunes:duration>
    </item>
  </channel>
</rss>"""

with open("feed.xml", "w") as f:
    f.write(feed)

print(f"Feed updated for {date_title}")
