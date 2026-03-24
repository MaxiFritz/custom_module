from datetime import datetime
import pytz

zones = {
    "Los Angeles": "America/Los_Angeles",
    "New York": "America/New_York",
    "Liège": "Europe/Brussels",
    "Doha": "Asia/Qatar",
    "Hong Kong": "Asia/Hong_Kong",
    "Sydney": "Australia/Sydney"
}

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>World Clock</title>
<style>
body { font-family: Arial; padding: 40px; background: none; color: #172b4d; }
h1 { margin-bottom: 20px; }
div { margin-bottom: 10px; font-size: 1.4rem; }
</style>
</head>
<body>
<h1>Current Time</h1>
"""

for city, zone in zones.items():
    tz = pytz.timezone(zone)
    now = datetime.now(tz).strftime("%H:%M")
    html += f"<div><strong>{city}:</strong> {now}</div>\n"

html += """
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)
