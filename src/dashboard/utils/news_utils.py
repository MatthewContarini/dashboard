import feedparser

FEED_URL = "https://www.abc.net.au/news/feed/10719986/rss.xml" # ABC Top Stories

def get_top_stories(count=4, exclude_categories=None):
    """
    Fetch the top `count` stories from the RSS `FEED_URL`, 
    excluding any whose categories match (case-insensitive)
    entries in `exclude_categories`.
    Returns a list of dicts with 'headline' and 'description'.
    """
    

    # Normalize exclude_categories to lowercase set for fast lookup
    exclude = {cat.lower() for cat in (exclude_categories or [])}

    feed = feedparser.parse(FEED_URL)
    stories = []

    for entry in feed.entries:
        # Gather all categories (tags) for this entry, lowercase
        entry_cats = {tag.term.lower() for tag in entry.get("tags", [])}

        # If any of this entry's categories is in the exclude set, skip it
        if exclude & entry_cats:
            continue

        # Otherwise, include it
        stories.append({
            "headline": entry.title,
            "description": entry.get("description", "").strip(),
        })
        if len(stories) >= count:
            break

    return stories