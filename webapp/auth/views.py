from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import generic

from apps.staff.models import StaffUser, StaffRole
from webapp.auth import forms


class AuthView(generic.View):
    model = StaffUser
    template_name = "auth.html"

    def post(self, request, *args, **kwargs):
        form = forms.AuthForm(data=request.POST)

        if not form.is_valid():
            messages.error(request, "So'rov yuborishda xaolik yuz berda. Dasturchi bilan bog'laning.")
            return redirect("web:auth:login", )

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        remember_me = form.cleaned_data['remember_me']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['branch_id'] = user.branch_id
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Expires when browser is closed
            match user.role:
                case StaffRole.ADMIN:
                    return redirect('webapp:admin:main')
                case StaffRole.RECEPTIONIST:
                    return redirect('webapp:reception:main')
                case StaffRole.DOCTOR:
                    return redirect('webapp:doctor:main')
                case StaffRole.LAB_TECH:
                    return redirect('webapp:laboratory:main')
                case _:
                    request.session.flush()
                    logout(request)
                    messages.error(request, "Tizimga kirish uchun sizda ruxsat yo'q adminstratsiya bilan bog'laning")
                    return render(request, "auth.html",
                                  {"username": username, "password": password})
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri")
            return render(request, "auth.html",
                          {"username": username, "password": password})

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return render(request, "auth.html", )
        match user.role:
            case StaffRole.ADMIN:
                return redirect('webapp:admin:main')
            case StaffRole.RECEPTIONIST:
                return redirect('webapp:reception:main')
            case StaffRole.DOCTOR:
                return redirect('webapp:doctor:main')
            case StaffRole.LAB_TECH:
                return redirect('webapp:laboratory:main')
            case _:
                request.session.flush()
                logout(request)
                messages.error(request, "Tizimga kirish uchun sizda ruxsat yo'q adminstratsiya bilan bog'laning")
                return render(request, "auth.html",
                              {"username": "", "password": ""})


def logout_view(request):
    # Optional: Clear specific session variables
    request.session.flush()  # This completely clears out the session data

    # Log the user out
    logout(request)

    # Redirect to the login page or another page
    return redirect('webapp:auth:login')
