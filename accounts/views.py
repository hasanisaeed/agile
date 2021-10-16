from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils.datetime_safe import datetime
from django.views import generic
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm
from accounts.models import Attendance


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        print(">>> TEST")
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class DashboardView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        from django.contrib.auth.models import User
        users = User.objects.all()

        user_info = []
        for user in users:
            info = {'id': user.id,
                    'name': user.get_full_name(),
                    'last_login': user.last_login}
            try:
                attendance = user.attendance.filter(user=user).latest('enter')
                info['enter'] = attendance.enter.strftime('%H:%M:%S')
                info['exit'] = attendance.exit.strftime('%H:%M:%S')
            except:
                info['enter'] = '',
                info['exit'] = ''
            user_info.append(info)

        context['users'] = user_info
        return context


def apply_attendance(request, pk):
    if request.method == "GET":
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        user = User.objects.get(pk=pk)
        from django.urls import resolve
        url = request.GET.get("next")
        try:
            # If datetime is today and the time of attendance has not been set before.
            last_attendance = Attendance.objects.filter(user=user).latest('enter')
            if last_attendance.enter is not None:
                if last_attendance.enter.day != datetime.today().day:
                    # Set the attendance time
                    new_attendance = Attendance.objects.create(user=user,
                                                               enter=datetime.now())
                    messages.success(request, {'user': pk,
                                               'text': 'حصور ثبت شد.'})

                else:
                    # toggle: then check for exit time.
                    if last_attendance.exit is None:
                        attendance_update = Attendance.objects.filter(id=last_attendance.id).update(exit=datetime.now())
                        messages.success(request, {'user': pk,
                                                   'text': 'ساعت خروج ثبت شد.'})
                    else:
                        messages.error(request, {'user': pk,
                                                 'text': 'سقبلا ساعت ورود/خروج ثبت شده است.'})
        except Exception as e:
            # Set the attendance time
            new_attendance = Attendance.objects.create(user=user,
                                                       enter=datetime.now())
            print(">> OK2")
            messages.success(request, {'user': pk,
                                       'text': 'حصور ثبت شد.'})

        resolve(url)
        return HttpResponseRedirect(url)
