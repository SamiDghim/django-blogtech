import os
import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Rebuild Tailwind CSS"

    def handle(self, *args, **options):
        self.stdout.write("🎨 Rebuilding Tailwind CSS...")

        try:
            # Run the Tailwind CSS build command
            result = subprocess.run(
                ["npm", "run", "build-once"],
                cwd=os.getcwd(),
                capture_output=True,
                text=True,
                check=True,
            )

            self.stdout.write(self.style.SUCCESS("✅ CSS rebuilt successfully!"))
            if result.stdout:
                self.stdout.write(f"Output: {result.stdout}")

        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"❌ Error rebuilding CSS: {e}"))
            if e.stderr:
                self.stdout.write(f"Error details: {e.stderr}")
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR("❌ npm not found. Make sure Node.js is installed.")
            )
