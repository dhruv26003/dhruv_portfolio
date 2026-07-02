# Premium Personal Portfolio Website 🚀

A modern, production-ready, mobile-responsive, recruiter-friendly, and SEO-optimized Personal Portfolio Website built using **Python Django**, **Bootstrap 5**, and custom **HTML5/CSS3/JavaScript**. 

Everything is dynamically generated and fully manageable through the customized Django Admin Panel.

---

## 🌟 Key Features

1. **Aesthetics**: Cyberpunk dark theme (Slate-Black & Cyan Glow) with seamless in-page toggle to a clean Light Mode.
2. **Interactive Background**: Floating background grid with HTML5 Canvas interactive particle trace that tracks cursor and scales to theme change.
3. **Animations**: Typing animation for titles, Animate On Scroll (AOS) scroll revelations, floating structural shapes, and glowing borders.
4. **Skills Management**: Grouped skills by category with real-time title search and category-click filtering (zero-reload).
5. **Projects Portfolio**: Case studies filtered in real-time by tag and search bar queries.
6. **Timeline Details**: Professional career history timeline mapping Queryfinders experience and educational milestones.
7. **Contact Logs**: Secure (CSRF-protected) contact form utilizing AJAX submitting background logs to database, returning custom status alerts.
8. **Recruiter Integrations**: Direct cv resume download, quick facts board, and certificates credential check overlays.
9. **SEO Engine**: Dynamic XML `sitemap.xml`, crawling robots.txt directive, unique page titling, semantic markup hierarchy, and Open Graph meta integrations.
10. **Visitor Hit Metrics**: Dynamic session-based hit counter in footer showing unique visitor counts.
11. **Standalone Sub-Pages**: Beautiful project details view for deep case studies, and customized 404 pages.

---

## 🛠 Tech Stack

- **Backend**: Python 3.13+, Django 5+, Django ORM, Pillow (Image processing), dj-database-url (Environment variables)
- **Frontend**: HTML5, Vanilla CSS3, Bootstrap 5, FontAwesome 6, AOS.js, Typed.js
- **Database**: SQLite (Local development), MySQL/PostgreSQL Ready (Production)

---

## 📁 Repository Structure

```
portfolio/
├── manage.py
├── portfolio/
│   ├── settings.py           # Core settings (database, static/media, context processors)
│   ├── urls.py               # Main URL router
│   └── ...
├── main/
│   ├── migrations/           # Pre-assembled database migrations
│   ├── context_processors.py # Injects Profile, SocialLinks, and Active Resume globally
│   ├── models.py             # Database schemas (11 models)
│   ├── admin.py              # Customized admin panel lists and filters
│   ├── views.py              # Home, project detail, sitemap, contact handling
│   ├── urls.py               # Sub-urls mapping
│   ├── forms.py              # Contact form validation widget styling
│   └── ...
├── static/
│   ├── css/
│   │   └── style.css         # Modern dark/light design system, timelines, animations
│   └── js/
│       └── main.js           # AOS init, Typed.js config, dark-mode toggle, contact AJAX, Canvas particles
├── templates/
│   ├── base.html             # Common shell with navbar, footer, CDNs, loader, back-to-top
│   ├── main/
│   │   ├── home.html         # Section structures: Hero, About, Skills, Projects, Contact, etc.
│   │   ├── project_detail.html # Case study display page
│   │   └── 404.html          # Glitched cyber error page
│   └── sitemap.xml           # XML sitemap template
├── requirements.txt          # Production package checklist
└── seed_data.json            # Mock database record fixtures
```

---

## 🚀 Local Installation & Quick Start

### 1. Set Up Virtual Environment

Open your terminal in the workspace directory and execute:

```bash
# Initialize a virtual environment
python -m venv venv

# Activate on Windows (Command Prompt)
venv\Scripts\activate
# OR on PowerShell
.\venv\Scripts\Activate.ps1
# OR on macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

Install packages listed in the updated `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Run Database Migrations

Apply pre-compiled migrations in the sqlite database:

```bash
python manage.py migrate
```

### 4. Load Sample Seed Data

Pre-populate your database with professional sample data (including skills, categories, experiences at Queryfinders, certificates, and services):

```bash
python manage.py loaddata seed_data.json
```

### 5. Create Superuser (Admin Access)

Create an administrative account to access the custom Django Admin Panel:

```bash
python manage.py createsuperuser
```

*Follow prompts to input Username, Email, and Password.*

### 6. Boot the Local Server

Start the Django StatReloader development server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your web browser to view the portfolio. Access `http://127.0.0.1:8000/admin` to customize the portfolio details.

---

## 🔧 Production Deployment Guides

### Option 1: Render / Railway (PaaS)
1. **Database**: Provision a PostgreSQL database on Render/Railway.
2. **Environment Variables**: Add the following keys in your Environment settings:
   - `DEBUG`: `False`
   - `SECRET_KEY`: `your-custom-production-secret`
   - `DATABASE_URL`: `postgresql://user:pass@host:port/dbname` (supplied by DB provider)
3. **Build Command**: Configure build command to install dependencies, run migrations, and collect static files:
   ```bash
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input
   ```
4. **Start Command**: Set start command to run via Gunicorn:
   ```bash
   gunicorn portfolio.wsgi:application
   ```

### Option 2: VPS (Ubuntu + Nginx + Gunicorn)
1. **Install System Dependencies**: Install Python, Nginx, PostgreSQL, and supervisor.
2. **Gunicorn Systemd Service**: Setup a systemd service file `/etc/systemd/system/gunicorn.service`:
   ```ini
   [Unit]
   Description=gunicorn daemon
   After=network.target

   [Service]
   User=sammy
   WorkingDirectory=/home/sammy/portfolio
   ExecStart=/home/sammy/portfolio/venv/bin/gunicorn --workers 3 --bind unix:/home/sammy/portfolio/portfolio.sock portfolio.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```
3. **Nginx Reverse Proxy**: Configure a block in `/etc/nginx/sites-available/portfolio`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       location /static/ {
           root /home/sammy/portfolio;
       }
       location /media/ {
           root /home/sammy/portfolio;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/home/sammy/portfolio/portfolio.sock;
       }
   }
   ```
4. **SSL Setup**: Secure the site by running `sudo certbot --nginx -d yourdomain.com`.
