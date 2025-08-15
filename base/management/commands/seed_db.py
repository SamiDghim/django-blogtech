import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from base.models import Message, Room, Topic

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            Message.objects.all().delete()
            Room.objects.all().delete()
            Topic.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS("✅ Data cleared"))

        self.stdout.write("Seeding database...")

        # Create default admin user
        admin_user, created = User.objects.get_or_create(
            email="admin@studybuddy.com",
            defaults={
                "username": "admin",
                "name": "StudyBuddy Admin",
                "bio": "Platform administrator",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(
                f"✅ Created admin user: admin@studybuddy.com (password: admin123)"
            )
        else:
            self.stdout.write(f"ℹ️  Admin user already exists: admin@studybuddy.com")

        # Create default regular users
        sample_users = [
            {
                "email": "alice@example.com",
                "username": "alice_johnson",
                "name": "Alice Johnson",
                "bio": "Computer Science student passionate about web development and AI.",
            },
            {
                "email": "bob@example.com",
                "username": "bob_smith",
                "name": "Bob Smith",
                "bio": "Mathematics major interested in data science and machine learning.",
            },
            {
                "email": "carol@example.com",
                "username": "carol_davis",
                "name": "Carol Davis",
                "bio": "Physics student exploring quantum computing and software engineering.",
            },
            {
                "email": "david@example.com",
                "username": "david_wilson",
                "name": "David Wilson",
                "bio": "Engineering student focused on robotics and automation.",
            },
            {
                "email": "emma@example.com",
                "username": "emma_brown",
                "name": "Emma Brown",
                "bio": "Design student passionate about UX/UI and creative technologies.",
            },
        ]

        created_users = []
        for user_data in sample_users:
            user, created = User.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "username": user_data["username"],
                    "name": user_data["name"],
                    "bio": user_data["bio"],
                },
            )
            if created:
                user.set_password("password123")
                user.save()
                self.stdout.write(f"✅ Created user: {user.email}")
            else:
                self.stdout.write(f"ℹ️  User already exists: {user.email}")
            created_users.append(user)

        # Create topics
        sample_topics = [
            "Python Programming",
            "JavaScript Development",
            "Machine Learning",
            "Web Development",
            "Data Science",
            "React.js",
            "Django Framework",
            "Database Design",
            "DevOps & Deployment",
            "Mobile Development",
            "UI/UX Design",
            "Algorithms & Data Structures",
            "Cloud Computing",
            "Artificial Intelligence",
            "Cybersecurity",
        ]

        created_topics = []
        for topic_name in sample_topics:
            topic, created = Topic.objects.get_or_create(name=topic_name)
            if created:
                self.stdout.write(f"✅ Created topic: {topic_name}")
            created_topics.append(topic)

        # Create sample rooms
        sample_rooms = [
            {
                "name": "Python Beginners Study Group",
                "description": "Learn Python fundamentals together! Perfect for beginners who want to master the basics of programming with Python.",
                "topic": "Python Programming",
            },
            {
                "name": "JavaScript ES6+ Deep Dive",
                "description": "Exploring modern JavaScript features, async/await, and best practices for clean code.",
                "topic": "JavaScript Development",
            },
            {
                "name": "Machine Learning Study Circle",
                "description": "Weekly discussions on ML algorithms, datasets, and practical implementations. All levels welcome!",
                "topic": "Machine Learning",
            },
            {
                "name": "React Component Patterns",
                "description": "Advanced React patterns, hooks, and state management techniques for building scalable applications.",
                "topic": "React.js",
            },
            {
                "name": "Django REST API Workshop",
                "description": "Building robust REST APIs with Django REST Framework. Hands-on coding sessions included.",
                "topic": "Django Framework",
            },
            {
                "name": "Algorithm Problem Solving",
                "description": "Daily coding challenges and algorithm discussions. Prepare for technical interviews together!",
                "topic": "Algorithms & Data Structures",
            },
            {
                "name": "Full Stack Web Development",
                "description": "End-to-end web development covering frontend, backend, and deployment strategies.",
                "topic": "Web Development",
            },
            {
                "name": "Data Science with Python",
                "description": "Pandas, NumPy, Matplotlib, and more! Analyze real-world datasets and build insights.",
                "topic": "Data Science",
            },
            {
                "name": "UI/UX Design Principles",
                "description": "User-centered design, prototyping, and creating intuitive digital experiences.",
                "topic": "UI/UX Design",
            },
            {
                "name": "Cloud Computing Fundamentals",
                "description": "AWS, Azure, and GCP basics. Learn cloud architecture and deployment strategies.",
                "topic": "Cloud Computing",
            },
        ]

        created_rooms = []
        for room_data in sample_rooms:
            topic = Topic.objects.get(name=room_data["topic"])
            host = random.choice(created_users + [admin_user])

            room, created = Room.objects.get_or_create(
                name=room_data["name"],
                defaults={
                    "description": room_data["description"],
                    "topic": topic,
                    "host": host,
                },
            )
            if created:
                # Add some random participants
                participants = random.sample(created_users, random.randint(2, 4))
                room.participants.set(participants)
                self.stdout.write(f'✅ Created room: {room_data["name"]}')
            created_rooms.append(room)

        # Create sample messages
        sample_messages = [
            "Hey everyone! Excited to start learning together! 🚀",
            "Just finished the first chapter, it's getting interesting!",
            "Anyone else finding this concept challenging? Let's discuss!",
            "Great session today! Thanks for the helpful explanations.",
            "I found this resource really helpful, sharing the link...",
            "Quick question about the latest topic we covered.",
            "Looking forward to tomorrow's study session!",
            "This community is amazing! So much to learn from everyone.",
            "Just implemented what we learned today in my project!",
            "Does anyone have experience with this framework?",
            "Sharing my notes from today's discussion for everyone.",
            "Breaking down complex problems into smaller parts really helps!",
            "The hands-on approach is making everything clearer.",
            "Thanks for being patient with my questions, team!",
            "Just discovered this cool technique, thought you'd find it useful.",
        ]

        for room in created_rooms:
            # Create 3-8 messages per room
            num_messages = random.randint(3, 8)
            for _ in range(num_messages):
                user = random.choice(list(room.participants.all()) + [room.host])
                message_body = random.choice(sample_messages)

                Message.objects.create(
                    user=user,
                    room=room,
                    body=message_body,
                )

            self.stdout.write(f'✅ Added {num_messages} messages to "{room.name}"')

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Database seeded successfully!\n"
                f"👤 Admin: admin@studybuddy.com (password: admin123)\n"
                f"👥 Users: {len(created_users)} sample users created\n"
                f"🏷️  Topics: {len(created_topics)} topics created\n"
                f"🏠 Rooms: {len(created_rooms)} study rooms created\n"
                f"💬 Messages: Sample conversations added\n\n"
                f"🔗 Access your app at: http://localhost:8000\n"
                f"🔧 Admin panel at: http://localhost:8000/admin"
            )
        )
