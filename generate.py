from datetime import datetime, timedelta
import pytz

zones = {
    "Los Angeles": "America/Los_Angeles",
    "New York": "America/New_York",
    "Liège": "Europe/Brussels",
    "Doha": "Asia/Qatar",
    "Hong Kong": "Asia/Hong_Kong",
    "Sydney": "Australia/Sydney"
}

def next_dst_change(tz):
    """Return the next DST transition for a timezone."""
    now = datetime.now(tz)
    one_year = now + timedelta(days=365)

    # pytz exposes transitions via _utc_transition_times
    transitions = tz._utc_transition_times

    # Convert transitions to timezone-aware datetimes
    future_transitions = []
    for t in transitions:
        dt = pytz.utc.localize(t)
        if dt > now.astimezone(pytz.utc) and dt < one_year.astimezone(pytz.utc):
            future_transitions.append(dt)

    if future_transitions:
        return future_transitions[0].astimezone(tz)
    return None


html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>World Clock</title>
<style>
body { font-family: Arial; padding: 40px; background: none; color: #172b4d; }
h1 { margin-bottom: 20px; }
.row {
    display: flex;
    justify-content: space-between;
    font-size: 1.4rem;
    margin-bottom: 6px;
}
.sub {
    font-size: 0.9rem;
    color: #555;
    margin-bottom: 14px;
}
</style>
</head>
<body>"""

# Track earliest DST change worldwide
global_next_change = None
global_next_zone = None

for city, zone in zones.items():
    tz = pytz.timezone(zone)
    now = datetime.now(tz).strftime("%H:%M")

    # Find next DST change for this zone
    change = next_dst_change(tz)

    if change and (global_next_change is None or change < global_next_change):
        global_next_change = change
        global_next_zone = city

# Add DST info
if global_next_change:
    formatted = global_next_change.strftime("%Y-%m-%d %H:%M")
    now_local = datetime.now(global_next_change.tzinfo)
    delta = global_next_change - now_local
    delta_days = delta.days
    html += f"""
    <h2>Next Time Change</h2>
    <div class="sub">
        The next worldwide DST change occurs in <strong>{global_next_zone}</strong> on <strong>{formatted}</strong> in {delta_days} days.
    </div>
    """
else:
    html += """
    <h2>Next Time Change</h2>
    <div class="sub">No DST changes detected in the next year.</div>
    """

html += """
</body>
</html>
"""
html += f"<!-- Generated at {datetime.utcnow()} UTC -->\n"

with open("index.html", "w") as f:
    f.write(html)
