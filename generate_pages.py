from datetime import datetime, timedelta
import pytz

# -----------------------------
#  MODULES
# -----------------------------

zones = {
    "Los Angeles": "America/Los_Angeles",
    "New York": "America/New_York",
    "Liège": "Europe/Brussels",
    "Doha": "Asia/Qatar",
    "Hong Kong": "Asia/Hong_Kong",
    "Sydney": "Australia/Sydney"
}

def next_dst_change(tz):
    now = datetime.now(tz)
    one_year = now + timedelta(days=365)
    transitions = tz._utc_transition_times

    future = []
    for t in transitions:
        dt = pytz.utc.localize(t)
        if now.astimezone(pytz.utc) < dt < one_year.astimezone(pytz.utc):
            future.append(dt)

    return future[0].astimezone(tz) if future else None


# -----------------------------
#  PAGE 1: WORLD CLOCK
# -----------------------------

def page_dst_change():
    html = ""

    global_next_change = None
    global_next_zone = None

    for city, zone in zones.items():
        tz = pytz.timezone(zone)
        change = next_dst_change(tz)

        if change and (global_next_change is None or change < global_next_change):
            global_next_change = change
            global_next_zone = city

    if global_next_change:
        formatted = global_next_change.strftime("%Y-%m-%d %H:%M")
        now_local = datetime.now(global_next_change.tzinfo)
        delta_days = (global_next_change - now_local).days

        html += f"""
        <div>
            Next DST change: <strong>{global_next_zone}</strong> in {delta_days} days.<br>
            Date: <strong>{formatted}</strong>
        </div>
        """
    else:
        html += "<div>No DST changes in the next year.</div>"

    return html


# -----------------------------
#  PAGE 2: EVENT COUNTDOWN
# -----------------------------

EVENTS = [
    ("World Cup", "2026-06-11"),
    ("Rugby League WC", "2026-10-15"),
    ("YOG Dakar", "2026-10-31"),
    ("NAB", "2026-04-18"),
    ("Summer Olympics", "2028-07-14")
]

def page_event_countdown():
    now = datetime.now()
    upcoming = []

    # Convert and filter upcoming events
    for name, date_str in EVENTS:
        event_date = datetime.strptime(date_str, "%Y-%m-%d")
        if event_date > now:
            upcoming.append((name, event_date))

    # Sort and keep next 3
    upcoming = sorted(upcoming, key=lambda e: e[1])[:3]

    if not upcoming:
        return "<div>No upcoming events.</div>"

    # Build horizontal layout
    html = '<div style="display: flex; gap: 25px; align-items: center;">'

    for name, date in upcoming:
        delta_days = (date - now).days

        html += f"""
        <div style="display: flex; align-items: center;">
            <div style="
                width: 50px;
                height: 50px;
                background: #f2f2f2;
                border: 2px solid #ccc;
                border-radius: 6px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                font-weight: bold;
                margin-right: 10px;
            ">
                {delta_days}
            </div>
            <div style="white-space: nowrap;">
                {name}
            </div>
        </div>
        """

    html += "</div>"
    return html


# -----------------------------
#  PAGE REGISTRY
# -----------------------------

PAGES = {
    "dst_change": page_dst_change,
    "countdown": page_event_countdown,
}

# -----------------------------
#  INDEX PAGE REGISTERY
# -----------------------------

def build_homepage():
    links = []

    for page_name in PAGES.keys():
        filename = f"{page_name}.html"
        title = page_name.replace("_", " ").title()
        links.append(f'<li><a href="{filename}">{title}</a></li>')

    content = f"""
    <h1>Available Pages</h1>
    <ul>
        {''.join(links)}
    </ul>
    """

    html = render_page(content, title="Home")

    with open("index.html", "w") as f:
        f.write(html)

    print("Generated index.html with links to all pages")


# -----------------------------
#  MAIN GENERATOR
# -----------------------------

def render_page(content, title="Page"):
    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
html, body {{margin: 0;padding: 0;}}
body {{ font-family: Arial; background: none; color: #172b4d; }}
</style>
</head>
<body>
{content}
</body>
</html>
"""

def build(page_name):
    if page_name not in PAGES:
        raise ValueError(f"Unknown page '{page_name}'. Available: {list(PAGES.keys())}")

    content = PAGES[page_name]()
    html = render_page(content, title=page_name.capitalize())

    filename = f"{page_name}.html"
    with open(filename, "w") as f:
        f.write(html)

    print(f"Generated {filename}")


# -----------------------------
#  RUN
# -----------------------------

if __name__ == "__main__":
    # Automatically build every page defined in PAGES
    for page_name in PAGES.keys():
        build(page_name)

    # Build homepage linking to all pages
    build_homepage()

