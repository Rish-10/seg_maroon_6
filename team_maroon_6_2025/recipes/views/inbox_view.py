from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from recipes.models.notification import Notification
from django.views.decorators.http import require_POST

@login_required
def inbox(request):
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
@require_POST  # Security: Prevent deletion via simple URL typing
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)

    # Security: Ensure only the owner can delete it
    if notification.recipient == request.user:
        notification.delete()

    # Redirect back to inbox.
    # We could theoretically grab the 'filter' param to keep them on the same tab.
    return redirect('inbox')
