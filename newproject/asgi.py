"""
ASGI config for newproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newproject.settings')

application = get_asgi_application()

# Programmatic database migration and setup on load for zero-config Render deployments
try:
    from django.core.management import call_command
    print("[INFO] Running automatic programmatic database migrations...")
    call_command('migrate', interactive=False)
    print("[INFO] Running automatic programmatic database setup/seeding...")
    call_command('setup', interactive=False)
    print("[SUCCESS] Automatic database initialization completed successfully!")
except Exception as e:
    print(f"[ERROR] Automatic database initialization failed: {str(e)}")
