# Playonix — Django Site

Corporate sports engagement marketing site. Built in Django so content
(packages, catalogue, testimonials, cities) is editable from `/admin`
without touching code.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up the database
python manage.py migrate

# 3. Load starter content (packages, sports/wellness catalogue, cities)
python manage.py seed_content

# 4. Create your own admin login
python manage.py createsuperuser

# 5. Run the site
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site, `http://127.0.0.1:8000/admin/` to manage content.

## Project Structure

```
playonix_site/
├── config/              ← project settings, urls
├── marketing/            ← the app: models, views, forms, admin
│   ├── models.py          Package, Testimonial, CatalogueCategory/Item, City, ContactSubmission
│   ├── views.py            home, about, contact, blog
│   ├── forms.py            ContactForm
│   ├── admin.py            registers everything for /admin editing
│   └── management/commands/seed_content.py   ← initial data loader
├── templates/
│   ├── base.html          nav, footer, shared <head> — edit ONCE, applies everywhere
│   └── marketing/         home.html, about.html, contact.html, blog.html
└── static/
    ├── css/base.css        all styling (original design + new additions)
    └── js/contact.js        small checkbox UI behavior
```

## What's editable in `/admin` (no code needed)

- **Packages** — Spark / League Pro / Enterprise: name, price-adjacent copy, features list, which one is "featured"
- **Catalogue** — Sports & Wellness categories and their items
- **Testimonials** — currently seeded with ONE unpublished placeholder. **Do not publish it** — it's not a real quote. Add real ones via admin and tick "is published."
- **Cities** — which cities are "live" vs "upcoming"
- **Contact Submissions** — every "Get a Proposal" form fill lands here, read-only (so nobody edits a lead's data by accident), plus you'll get an email if SMTP is configured

## Things still pending (flagged, not forgotten)

1. **About Us page** (`templates/marketing/about.html`) — currently a placeholder. Drop in real content + adjust `marketing/views.py::about` if you want it to pull from the database instead of being static HTML.
2. **Real images** — every photo on the site (hero, Why Playonix, the 3 Services cards, Catalogue, How It Works) currently hotlinks a themed **Unsplash** stock photo directly — same approach as the original design file, so nothing 404s and the site looks finished out of the box. To swap any of them for real photography:
   - Open `templates/marketing/home.html`, find the `<img src="https://images.unsplash.com/...">` tag for that section, and replace the URL with your own image path (e.g. `/static/images/your-photo.jpg` once you've added the file to `static/images/`).
   - The hero background is the one exception — it's set in CSS, not the template. Search `static/css/base.css` for `HERO IMAGE SLOT`.
   - The OG banner (`static/images/og-banner.jpg`, used for WhatsApp/LinkedIn link previews) is intentionally left as a placeholder, not stock — it should be your real logo/branding, not generic sports photography. Add a 1200×630px branded image at that path when ready.
3. **Email sending** — works locally by printing to your terminal console. To actually receive emails, set these environment variables (e.g. in a `.env` file, loaded via `python-decouple` or similar once you add one):
   - `EMAIL_HOST_USER` — your sending email address
   - `EMAIL_HOST_PASSWORD` — app password (not your regular password, for Gmail use an "App Password")
   - `CONTACT_NOTIFICATION_EMAIL` — where you want leads delivered (defaults to hello@playonix.in)
4. **OG banner image** — `static/images/og-banner.jpg` referenced in `templates/base.html` for link previews on WhatsApp/LinkedIn. Add a 1200×630px image there.
5. **Phone number on Contact page** — currently a placeholder (`+91 98492 89071`) in `templates/marketing/contact.html`. Update to your real number.

## Before deploying live

- Set `DJANGO_DEBUG=False` as an environment variable
- Set a real `DJANGO_SECRET_KEY` environment variable (don't use the one in `settings.py`)
- Set `DJANGO_ALLOWED_HOSTS` to your real domain
- Run `python manage.py collectstatic`
- Swap SQLite for Postgres if/when traffic grows (one line change in `settings.py` — see comment there)

## Future growth (already planned for, not built yet)

This project is structured as Django "apps" so league/team management and
live scoring can be added as new apps (`leagues/`, `scoring/`) later without
touching the marketing site. Live scoring will need **Django Channels**
added on top — flagged here so it's not a surprise when that phase starts.
