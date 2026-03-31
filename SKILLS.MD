# Bitly Clone Project - Skills & Context

This document provides a detailed overview of the `bitly_clone` project to serve as context for future development and debugging sessions. It outlines the technology stack, application architecture, models, views, and environment setup.

## 1. Project Overview
- **Framework:** Django 4.1.7
- **Database:** SQLite (`db.sqlite3`)
- **Key External Dependencies:** Django REST Framework, `corsheaders`, `requests` (used for IP geolocation fetching)
- **Deployment Context:** `ALLOWED_HOSTS` include `swapnil123.pythonanywhere.com` and `STATIC_ROOT` is `/home/swapnil123/bitly_clone/static/`, indicating a PythonAnywhere deployment environment.

## 2. Apps & Architecture
The project consists of the main `bitly_clone` configuration app and a core functional app named `shortner`.

### `shortner` App
This app handles all the logic for shortening URLs, redirecting, and tracking clicks and IP locations.

#### Models (`shortner/models.py`)
- **`Url`**: Stores the mapping between the original `long_url` and `short_url`.
  - Also tracks `clicks` (incremented on each visit), `created_at`, and the `ip` of the user who created it.
  - Automatically generates a random 6-character alphanumeric string for `short_url` on save if not provided.
- **`Ip`**: Stores location data associated with IP addresses.
  - Fields: `ip`, `latitude`, `longitude`, `city`.

#### Views & Endpoints (`shortner/urls.py` & `shortner/views.py`)
- **Frontend Views (Class-Based):**
  - **`HomeView` (`/`)**: A frontend page with a form (`UrlForm`) to submit a long URL and get a shortened version.
  - **`UrlRedirectView` (`/<short_url>/`)**: Looks up the `short_url` in the database, increments the `clicks` counter, and redirects the user to the original `long_url`.
- **API Views (Function-Based / DRF):**
  - **`get_url` (`/api/<short_url>/`)**: Handles both `GET` and `POST`. 
    - Fetches the user's IP location via `https://ipapi.co/{ip}/json` using the `requests` library.
    - Saves the IP and location info to the `Ip` model.
    - Returns the original URL (`GET`) or creates/updates a short URL mapping (`POST`).

## 3. Environment & Setup Details
- **Virtual Environment:** There is an `env` directory in the root. 
- **Requirements Fix:** The `requirements.txt` file was missing the `requests` library, which is required for the IP geolocation feature in `views.py`. Ensure `requests` is installed (`pip install requests`) when installing requirements.
- **Admin Credentials:** 
  - There is a superuser account: 
    - **Username:** `Payal` 
    - **Password:** `admin123!`
  - Admin panel is accessible at `/admin/`.

## 4. Known Gotchas
- The API uses `ipapi.co` for IP tracking, which has rate limits for free usage without an API key. If the `getinfo` function fails or returns 429 Too Many Requests, it will silently pass but won't record accurate location data.
- Ensure the `env` virtual environment is activated before running DB migrations or starting the server.
- Forms are currently served primarily using `django-bootstrap-form` (based on `requirements.txt`).

Use this document as a quick-start reference when modifying or adding features to this Bitly clone.
