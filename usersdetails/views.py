from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
# Create your views here.
@login_required
def userDetailsView(request):
    if request.method == 'GET':
        return render(request, 'userDetails.html', {'user': request.user})
    if request.method == 'POST':
        pass

def saveUserDetailsView(request):
    if request.method == "POST":
        
        f_name = request.POST.get("first_name")
        l_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("change_password")

        user = request.user

        update = False
        if f_name and f_name != user.first_name:
            user.first_name = f_name
            update = True
        if l_name and l_name != user.last_name:
            user.last_name = l_name
            update = True
        if email and email != user.email:
            user.email = email
            update = True
        if username and username != user.username:
            user.username = username
            update = True

        if password:
            user.set_password(password)
            update = True
            update_session_auth_hash(request, user)
        if update:
            messages.success(request, "Saved Successfully")
            request.user.save()    
        else:
            messages.info(request, "No Changes Found")
    return redirect('user-details')