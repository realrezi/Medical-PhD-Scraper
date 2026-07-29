# 🎓 Medical PhD Scholarship Scraper

A powerful Python web scraper that finds PhD/Doctorate scholarship positions in medical fields, filters them for relevance, and saves them to a cloud database. This project demonstrates expertise in web automation, data scraping, database integration, and regex filtering.

## 🚀 Features

- **Web Scraping**: Automated crawling of scholarship platforms
- **Smart Filtering**: Regex-based filtering to identify medical/health-related PhD positions
- **Cloud Database**: Saves results to Neon PostgreSQL (cloud-hosted)
- **Duplicate Prevention**: Ensures only unique positions are stored
- **Cloudflare Resistant**: Advanced anti-detection techniques using SeleniumBase (UC mode)

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL (Neon Database) - free cloud option available
- Chrome browser (for SeleniumBase)

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/realrezi/Medical-PhD-Scraper.git
cd med_phd_scraper
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
# Create a .env file in the project root
cat > .env << EOF
NEON_URL=postgresql://username:password@host:port/database
SCHOLARSHIP_PAGES=10
EOF
```

## 📖 Usage

### Basic execution
```bash
# Scrape up to 10 pages (default)
python scraper.py

# SCrape more pages
SCOLARSHIP_PAGES=50 python scraper.py

# Use a custom database connection
NEON_URL="your_connection_string" python scraper.py
```

### Output

The scraper will:
1. Navigate to scholarship listing pages
2. Extract all PhD/Doctorate positions
3. Filter for medical/health-related content
4. Display matching positions with 🎉 icons
5. Save qualifying positions to your Neon database

### Viewing Saved Results

I have included a handy utility script to easily view the matches saved in your cloud database right from your terminal.

```bash
# View the 10 most recent matches
python view_results.py

# View a custom number of matches (e.g., 20)
python view_results.py 20
```

Example Output:
```
🏥 MOST RECENT MEDICAL PHD POSITIONS (10)

🎓 PhD student in Medical Science
🔗 https://scholarshipdb.net/scholarships-in-Sweden/...
------------------------------------------------------------
```

Example output:
```
Navigating to https://scholarshipdb.net/scholarships-in-Germany?page=1
Found 15 PhD/Doctorate scholarship entries on this page. Filtering for medical relevance...
   -> 🎉 MATCH FOUND: Clinical Research PhD Position in Berlin
   -> 🎉 MATCH FOUND: Medical Sciences Doctoral Fellowship

========================================
Finished sweep! Found a total of 2 matching positions.
========================================
☁️ Successfully saved 2 new vacancies to your Neon cloud database!
```

## 🗄️ Database Schema

Positions are stored in the `medical_vacancies` table:

```sql
CREATE TABLE medical_vacancies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    url TEXT UNIQUE,
    description TEXT
);
```

## 🔍 Filtering Logic

The scraper uses comprehensive regex patterns to identify:

**PhD/Degree Keywords:**
- PhD
- Doctorate
- Ph.D.

**Medical Fields:**
- Medical, Biomedical, Health
- Clinical, Pharmaceutical, Therapeutic
- Oncology, Cardiology, Neuroscience
- Genetics, Immunology, Pathology
- Radiology, Surgery, Internal Medicine
- Pediatrics, Psychiatry, Public Health
- Medical Sciences, Biomedical Research
- Molecular Medicine, Translational Medicine

## 🏗️ Project Structure

```
med_phd_scraper/
├── scraper.py          # Main scraping logic and orchestrator
├── filter.py           # Medical content filtering module
├── database.py         # PostgreSQL database operations
├── debug_scraper.py    # Development/debugging tool
├── requirements.txt    # Python dependencies
├── .env               # Environment configuration
└── README.md          # This file
```

## 🔧 Configuration

All settings can be overridden via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `NEON_URL` | PostgreSQL connection string | Required |
| `SCHOLARSHIP_PAGES` | Number of pages to scrape | 10 |

## 🎯 Use Cases

This project is ideal for:
- Staying updated with medical PhD opportunities
- Researching scholarship trends in healthcare
- Building portfolio projects showcasing web scraping skills
- Automating job research for academic fields

## ⚡ Key Technologies

- **Python 3.9** - Main programming language
- **SeleniumBase** - Used in Undetected-Chromedriver (UC) mode to bypass Cloudflare
- **PostgreSQL (Neon)** - Cloud-hosted database
- **Psycopg2** - PostgreSQL adapter for Python
- **Regex** - Content filtering and validation

## 🐛 Troubleshooting

### Cloudflare Protection
If Cloudflare blocks scraping:
- The scraper uses SeleniumBase in UC (Undetected Chromedriver) mode.
- If it still gets blocked, Cloudflare might be identifying the IP. Consider using residential proxies or services like ScraperAPI/ZenRows.

### Database Connection Errors
- Verify `NEON_URL` is correctly formatted
- Check database credentials and connection details
- Ensure network allows connections to Neon

### No Results Found
- Check if the target URL has changed
- Verify filtering patterns match current page structure
- Run `debug_scraper.py` to analyze page content

## 📝 License

MIT License - Feel free to use this project for educational and commercial purposes.

## 👤 Author

**Ahmadreza Shirdel**  
[GitHub Profile](https://github.com/realrezi)

## 🙏 Acknowledgments

- Playwright community for the excellent scraping library
- Neon DB for the free cloud database service
- ScholarshipDB for hosting the scholarship listings

## 🔗 Links

- [SeleniumBase Documentation](https://seleniumbase.io/)
- [Neon DB](https://neon.tech/)
- [PostgreSQL](https://www.postgresql.org/)

---

**Note**: This project is for educational purposes. Always respect `robots.txt` and website terms of service when scraping.