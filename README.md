# StudyBuddy

A Django-based social learning platform where users can create study rooms, participate in discussions, and find study partners around the world.

## Features

- **Study Rooms**: Create and join topic-based study rooms
- **Real-time Messaging**: Participate in conversations within rooms
- **User Profiles**: Customize your profile with avatar and bio
- **Topic Browsing**: Discover rooms by topics of interest
- **Activity Feed**: Stay updated with recent activities
- **User Authentication**: Secure login/register system

## Tech Stack 🛠️

- **Backend**: Django 4.2.5 + Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: Django Templates + Tailwind CSS
- **Containerization**: Docker & Docker Compose
- **Authentication**: Custom User model with email login

## Quick Start

### Prerequisites
- Docker and Docker Compose installed

### Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd studybuddy
```

2. **Start development environment**
```bash
./dev.sh
```
This script will:
- Build Docker containers
- Install dependencies (Python + Node.js)
- Set up Tailwind CSS watching
- Run database migrations
- Start the development server

3. **Access the application**
- Django app: http://localhost:8000

### Manual Setup

```bash
# Build and start services
docker-compose up --build

# Create superuser (in another terminal)
docker-compose exec web python manage.py createsuperuser

# For Tailwind CSS development (in another terminal)
docker-compose exec web npm run dev
```

## Development Commands

### Docker Commands
```bash
# Start services
docker-compose up

# Start with Tailwind watcher
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Reset database
docker-compose down
docker volume rm studybuddy_postgres_data
docker-compose up
```

### Django Commands
```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate

# Create migrations
docker-compose exec web python manage.py makemigrations

# Shell access
docker-compose exec web bash
```

### Tailwind CSS Commands
```bash
# Watch for changes (development)
docker-compose exec web npm run dev

# Build for production
docker-compose exec web npm run build-css-prod

# Install new packages
docker-compose exec web npm install <package-name>
```

## Styling with Tailwind CSS

This project uses Tailwind CSS with a custom dark theme

### Custom Color Palette
- `main`: #71c6dd (Primary blue)
- `dark`: #3f4156 (Dark backgrounds)
- `bg`: #2d2d39 (Main background)
- `light`: #e5e5e5 (Light text)

### Example Components
```html
<!-- Button -->
<button class="btn btn--main">
  Create Room
</button>

<!-- Card -->
<div class="bg-dark p-6 rounded-lg border border-dark-light">
  <h3 class="text-light text-xl mb-4">Card Title</h3>
</div>
```

## Project Structure 📁

```
studybuddy/
├── base/                    # Main Django app
│   ├── templates/base/      # HTML templates
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   └── urls.py             # URL patterns
├── static/
│   ├── src/input.css       # Tailwind source
│   ├── css/main.css        # Generated CSS
│   ├── js/script.js        # JavaScript
│   └── images/             # Static images
├── templates/
│   ├── main.html           # Base template
│   └── navbar.html         # Navigation
├── studybud/               # Django project settings
├── docker-compose.yml      # Docker configuration
├── tailwind.config.js      # Tailwind configuration
└── package.json           # Node.js dependencies
```

## API Endpoints

The project includes REST API endpoints:
- `/api/` - API root
- `/api/rooms/` - Room operations
- `/api/rooms/<id>/` - Room details

## Contributing 

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests if needed
5. Update documentation
6. Submit a pull request

## Troubleshooting 🔧

### CSS not updating?
```bash
# Restart Tailwind watcher
docker-compose restart tailwind
```

### Database issues?
```bash
# Reset database
docker-compose down
docker volume rm studybuddy_postgres_data
docker-compose up
```

### Container build issues?
```bash
# Rebuild without cache
docker-compose build --no-cache
```
