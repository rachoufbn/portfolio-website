# Rachelle Fabian Portfolio website

## Tech Stack
- Python 3, Flask 3, MySQL 8, Docker
- Python scraping with requests + BeautifulSoup
- Frontend: vanilla JS, Bootstrap, simple search/filter utilities
- Caddy reverse proxy (local TLS) for convenient local HTTPS
- Anthropic Claude client wired for future AI features

## Quick Start
1) Copy `.env.example` to `.env` in the repo root:
    - Generate a random password for `MYSQL_ROOT_PASSWORD` and `MEETING_NOTES_BOT_DB_PASS`
    - For the meeting notes bot to work you will need to provide an `ANTHROPIC_API_KEY`
2) Add `127.0.0.1 local.rachellefabian.com` to the hosts file on your computer
3) Start the stack: `docker compose up -d --build`

## Projects

### Snow Report
Snow reports for Swiss ski resorts - scraped live from Bergfex.

- Scrapes live snow data from Bergfex using BeautifulSoup library and enriches it with resort metadata.
- API endpoint returns JSON with resort name, snow depths, new snow, and open lifts.
- Frontend features search and region-based filtering with JavaScript utilities.
- Demonstrates web scraping, REST API design, error handling, and client-side DOM manipulation.

### Meeting Notes Bot (WIP)
Goal: Generate AI-assisted notes from Teams `.vtt` transcripts with per-user meeting storage, including optionality for further AI chatting for note refinement and comprehension/clarification.

Current capabilities:
- **Authentication**: handling sign up, logins and user authentication. Email/password flows with Flask sessions and bcrypt password hashing.

- **File Uploads**: `.vtt` transcript with file size and extension validation.

- **Data**: Meeting notes bot MySQL schema created for `users | meetings | notes | chat_history` for storing users and per-user meetings/notes versions.

- **Per-request DB/auth lifecycle**: connection pooling and teardown hooks.

- **Frontend/UI**: login/signup flow, meeting list with upload/search/delete, and meeting detail page with chat + notes panes ready for AI responses.

Evidence of engineering practice: input validation, structured error handling (`UserFacingError`), environment-driven config, pooled DB access, modular route blueprints, and separation of concerns across routes/services/repository layers.

**To do**: Wire Claude calls (`ChatService` placeholder), complete chat/notes flow; production Gunicorn/AWS deployment still pending.

## License
This project is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later). See [LICENSE](LICENSE) for full terms.