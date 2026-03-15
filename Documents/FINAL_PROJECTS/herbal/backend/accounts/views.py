from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard:dashboard")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid email or password"}
        )

    return render(request, "accounts/login.html")
