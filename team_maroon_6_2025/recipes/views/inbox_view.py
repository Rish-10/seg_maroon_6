from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from recipes.models.notification import Notification

# Display the user's notification inbox with optional filtering
@login_required
def inbox(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).select_related('sender', 'content_type')

    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'favourite':
        notifications = notifications.filter(notification_type='favourite')
    elif filter_type == 'comment':
        notifications = notifications.filter(notification_type='comment')
    elif filter_type == 'follow':
        notifications = notifications.filter(notification_type='follow')
    elif filter_type == 'request':
        notifications = notifications.filter(notification_type='request')

    context = {
        'notifications': notifications,
        'current_filter': filter_type
    }

    return render(request, 'inbox.html', context)

# Delete a notification belonging to the current user
@login_required
@require_POST
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)

    if notification.recipient == request.user:
        notification.delete()

    return redirect('inbox')
