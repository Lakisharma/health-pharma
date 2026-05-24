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
    import sys
    
    acquired_lock = False
    lock_file = None
    
    # We only need locking on production (Linux/Render) where Gunicorn spawns multiple workers
    if os.environ.get('RENDER') or os.environ.get('PORT'):
        try:
            import fcntl
            lock_file = open('/tmp/db_init.lock', 'w')
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            acquired_lock = True
        except (ImportError, BlockingIOError, PermissionError):
            # Lock is already held by another worker process
            print("[INFO] Database initialization is already being handled by another process.")
    else:
        # Locally on Windows, always run it directly (usually single process)
        acquired_lock = True

    if acquired_lock:
        print("[INFO] Running automatic database migrations...")
        call_command('migrate', interactive=False)
        print("[INFO] Running database setup/seeding...")
        call_command('setup')
        print("[SUCCESS] Database initialization completed successfully!")
except Exception as e:
    print(f"[ERROR] Database initialization failed: {str(e)}")
