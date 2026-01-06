from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from recipes.models.notification import Notification

@login_required
def inbox(request):
    """
    Display the user's notification inbox with optional filtering
    """
    notifications = Notification.objects.filter(
        recipient=request.user
    ).select_related('sender', 'content_type')

    filter_type = request.GET.get('filter', 'all')

    match filter_type:
        case 'favourite':
            notifications = notifications.filter(notification_type='favourite')
        case 'comment':
            notifications = notifications.filter(notification_type='comment')
        case 'follow':
            notifications = notifications.filter(notification_type='follow')
        case 'request':
            notifications = notifications.filter(notification_type='request')

    context = {
        'notifications': notifications,
        'current_filter': filter_type
    }

    return render(request, 'inbox.html', context)

@login_required
@require_POST
def delete_notification(request, pk):
    """
    Delete a notification belonging to the current user
    Allows users to remove individual notifcations from their inbox
    """
    notification = get_object_or_404(Notification, pk=pk)

    if notification.recipient == request.user:
        notification.delete()

    return redirect('inbox')
