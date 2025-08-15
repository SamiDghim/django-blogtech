import logging
import os
import subprocess

from django.conf import settings
from django.core.management import call_command

logger = logging.getLogger(__name__)


class TailwindCSSMiddleware:
    """
    Middleware to rebuild Tailwind CSS on each request during development.
    Only active when DEBUG=True.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only rebuild CSS in development mode
        if settings.DEBUG and not request.path.startswith("/admin/"):
            self.rebuild_css()

        response = self.get_response(request)
        return response

    def rebuild_css(self):
        try:
            # Run Tailwind CSS build command
            result = subprocess.run(
                ["npm", "run", "build-once"],
                cwd=os.getcwd(),
                capture_output=True,
                text=True,
                timeout=10,  # 10 second timeout
            )

            if result.returncode == 0:
                logger.debug("CSS rebuilt successfully")
            else:
                logger.warning(f"CSS rebuild failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            logger.warning("CSS rebuild timed out")
        except FileNotFoundError:
            logger.warning("npm not found for CSS rebuild")
        except Exception as e:
            logger.warning(f"CSS rebuild error: {e}")
