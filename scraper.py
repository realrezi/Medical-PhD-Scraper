import os
import re
from dotenv import load_dotenv
from seleniumbase import SB
from filter import matches_medical_phd
from database import save_to_neon

# Load environment variables from .env file
load_dotenv()

# Number of pages to scrape (default 10, can be overridden via environment variable)
PAGE_LIMIT = int(os.getenv("SCHOLARSHIP_PAGES", "10"))


def scrape_page(sb, url):
    print(f"\nNavigating to {url}...")
    try:
        sb.get(url)
        # Give it a moment to load and handle Cloudflare challenge
        sb.sleep(5)

        page_source = sb.get_page_source()
        if "Just a moment" in page_source or "Cloudflare" in page_source:
            print("  ⚠️ Cloudflare challenge detected, waiting longer...")
            sb.sleep(10)
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return []

    raw_listings = []
    try:
        # Extract all PhD/Doctorate scholarship entries from the page using JavaScript
        items = sb.execute_script('''
            const items = [];
            // Find all anchor tags that contain relevant keywords in their text
            const keywordRegex = /phd|ph\\.d|doctorate|doctoral/i;
            document.querySelectorAll('h4 a').forEach(a => {
                const title = a.innerText.trim();
                const container = a.closest('li');
                let desc = '';
                if (container) {
                    desc = container.innerText.replace(title, '').trim();
                }
                
                if (keywordRegex.test(title) || keywordRegex.test(desc)) {
                    const url = a.href;
                    items.push({
                        title: title,
                        description: desc,
                        url: url
                    });
                }
            });
            return items;
        ''')

        raw_listings = items if items else []
        print(
            f"Found {len(raw_listings)} PhD/Doctorate scholarship entries on this page. Filtering for medical relevance...")
    except Exception as e:
        print(f"Error scraping content from {url}: {e}")

    return raw_listings


def scrape_and_process():
    all_valid_positions = []

    # Dynamically generate URLs for pages 1 through PAGE_LIMIT on scholarshipdb
    # Using 'q=Medical%20Sciences' to leverage the site's built-in relevancy engine
    pages_to_scrape = [
        f"https://scholarshipdb.net/scholarships?q=Medical%20Sciences&page={i}" for i in range(1, PAGE_LIMIT + 1)
    ]

    print(
        f"Starting sweep of {len(pages_to_scrape)} pages using SeleniumBase UC mode...")

    # We use SeleniumBase UC mode to bypass Cloudflare
    with SB(uc=True, headless=True) as sb:
        for target_url in pages_to_scrape:
            result = scrape_page(sb, target_url)

            # Process results and aggregate all valid positions
            if result:  # Non‑empty list
                for item in result:
                    if matches_medical_phd(item['title'], item['description']):
                        all_valid_positions.append(item)
                        print(f"   -> 🎉 MATCH FOUND: {item['title']}")

    print("\n========================================")
    print(
        f"Finished sweep! Found a total of {len(all_valid_positions)} matching positions.")
    print("========================================")

    if all_valid_positions:
        save_to_neon(all_valid_positions)

    return all_valid_positions


if __name__ == "__main__":
    scrape_and_process()
