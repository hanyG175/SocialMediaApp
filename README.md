# Social Media Platform

This is a Django-based social media application built with Python, featuring user authentication, profiles, posts, likes, friendships, and notifications. It uses basic HTML templates for the front-end and includes real-time features via Django Channels (WebSocket support partially implemented).

## Features
- User authentication (signup, signin, signout).
- Profile management with customizable fields (e.g., bio, profile image).
- Posting images with captions.
- Liking posts and sending friend invitations.
- Feed displaying posts from followed users.
- User search and profile suggestions.
- Notifications for likes and friend requests.
- Basic privacy settings page.

## Project Structure
- **`SocialMediaApp/`**: Main project directory with settings and root URL configuration.
  - `manage.py`: Django management script.
  - `SocialMediaApp/settings.py`: Project settings (adjust for your environment).
  - `SocialMediaApp/urls.py`: Root URL routing (includes app URLs).
- **`core/`**: Django app directory.
  - `views.py`: Handles HTTP requests and logic (e.g., feed, profile, likes).
  - `models.py`: Defines database models (e.g., `Profile`, `Post`, `Friendship`).
  - `urls.py`: App-specific URL routing.
- **`templates/`**: HTML templates for rendering pages.
  - `index.html`: Home feed with posts and suggestions.
  - `signup.html`: User registration form.
  - `signin.html`: Login form.
  - `setting.html`: Profile settings page.
  - `profile.html`: User profile view.
  - `search.html`: Search results page.
  - `privacy.html`: Privacy settings page.
  - `testing.html`: Placeholder for testing features.
-**`static/`**: for keeping the static file like images and fonts.
-**`media/`**: for storing the uploaded images from the user interface.
## Prerequisites
- **Python 3.x** (tested with Python 3.9+)
- **Django**: `pip install django`
- **Pillow**: `pip install Pillow` (for image handling)
- **Django Channels**: `pip install channels` (for WebSocket support)
- A database (e.g., SQLite by default; configure in `settings.py` for others like PostgreSQL).

## Installation
1. Clone the repository:
   `git clone <repository-url>`
   `cd SocialMediaProject`
2. Install dependencies:
   `pip install django Pillow channels`
3. Set up the database:
   `python manage.py makemigrations`
   `python manage.py migrate`
4. Create a superuser (optional):
   `python manage.py createsuperuser`
5. Configure `SocialMediaProject/settings.py`:
   - Add `'socialmedia'` and `'channels'` to `INSTALLED_APPS`.
   - Set up media file handling:
   `MEDIA_URL = '/media/'`
   `MEDIA_ROOT = BASE_DIR / 'media'`
- Configure `ASGI_APPLICATION` for Channels (e.g., `SocialMediaProject.asgi:application`).

## Usage
1. Run the development server:
`python manage.py runserver`
2. Access the app at `http://127.0.0.1:8000/`.
3. Steps:
- Sign up via `/signup/` to create an account.
- Log in at `/signin/`.
- Update your profile at `/settings/`.
- Post content at `/upload/`.
- Follow users, like posts, and view profiles at `/profile/<user_id>`.

## Key Components
- **`views.py`**:
- `index`: Displays the user feed and suggestions.
- `signup`/`signin`/`signout`: Authentication logic.
- `profile`: Shows user details and posts.
- `like`/`invite`: Handles interactions (likes, friend requests).
- `search`: Finds users by username.
- **`models.py`**:
- `Profile`: Stores user details (e.g., bio, image).
- `Post`: Manages user posts.
- `Friendship`: Tracks follower relationships.
- `Notification`: Logs likes and friend requests.
- **`urls.py`**: Maps URLs to views (e.g., `/`, `/profile/<pk>`).

## Templates
Basic HTML templates render the UI:
- `index.html`: Feed with posts, likes, and notifications.
- `profile.html`: User info, posts, and follow button.
- Others handle forms and static pages.

## Customization
- **Models**: Add fields (e.g., `Profile.work`) in `models.py` and update migrations.
- **Views**: Extend `index` to filter posts or enhance `search` logic.
- **Templates**: Modify HTML files (e.g., add Bootstrap via `STATIC_URL`).
- **Real-Time**: Fully implement WebSocket consumers in `views.py` for live notifications.

## Limitations
- WebSocket functionality not fully implemented.
- Minimal front-end styling; enhance with CSS/JavaScript.
- No comment functionality in views (though `Comment` model exists).
- SQLite is default; scale with a production database like PostgreSQL.

## Contributing
Submit issues or pull requests to add features (e.g., messaging, comments) or improve the UI!

## License
This project is open-source under the [MIT License](LICENSE).
