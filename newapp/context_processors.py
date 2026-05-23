from .models import Notification

def admin_notifications(request):
    """Context processor to inject unread notification details into templates"""
    if request.user.is_authenticated and request.user.is_staff:
        recent_notifications = Notification.objects.filter(is_admin=True).order_by('-created_at')[:8]
        unread_notifications_count = Notification.objects.filter(is_admin=True, is_read=False).count()
        return {
            'recent_notifications': recent_notifications,
            'unread_notifications_count': unread_notifications_count,
        }
    return {
        'recent_notifications': [],
        'unread_notifications_count': 0,
    }
