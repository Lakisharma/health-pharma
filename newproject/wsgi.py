"""
WSGI config for newproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newproject.settings')

application = get_wsgi_application()

# Programmatic database migration and setup on load for zero-config Render deployments
try:
    from django.core.management import call_command
    import threading

    def run_db_initialization():
        try:
            print("[INFO] Running automatic programmatic database migrations...")
            call_command('migrate', interactive=False)
            print("[INFO] Running automatic programmatic database setup/seeding...")
            call_command('setup', interactive=False)
            print("[SUCCESS] Automatic database initialization completed successfully!")
        except Exception as e:
            print(f"[ERROR] Automatic database initialization failed: {str(e)}")

    # Run in a background thread to prevent blocking the startup request
    threading.Thread(target=run_db_initialization, daemon=True).start()
except Exception as e:
    print(f"[ERROR] Failed to schedule automatic database initialization: {str(e)}")
