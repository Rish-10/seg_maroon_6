from django.shortcuts import render
from recipes.views.decorators import login_prohibited

# Display the public home page for unauthenticated users
@login_prohibited
def home(request):
    return render(request, 'home.html')