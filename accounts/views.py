from django.contrib import messages

from django.http import HttpResponseRedirect
from django.utils.datetime_safe import datetime
from django.views import generic
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm
from accounts.models import Attendance, CustomUser

NO_RECORD = 'card'
ENTER_TIME_IS_REGISTERED = 'card bg-success'
EXIT_TIME_IS_REGISTERED = 'card bg-danger text-white'
ATTENDANCE_TIME_IS_RECORD = 'card bg-light'


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
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
        users = CustomUser.objects.filter(is_superuser=False).all()

        user_info = []
        for user in users:
            info = {'id': user.id,
                    'avatar': user.avatar,
                    'name': user.get_full_name(),
                    'last_login': user.last_login,
                    'status': get_status(user)}
            try:
                info['enter'], info['exit'], _ = attendance_helper(user)
            except Attendance.DoesNotExist:
                info['enter'], info['exit'] = '', ''
            user_info.append(info)
        context['users'] = user_info
        return context


def get_status(user: CustomUser):
    try:
        enter_time, exit_time, _ = attendance_helper(user)
        if enter_time is not None:
            if enter_time == datetime.today().day:
                return ENTER_TIME_IS_REGISTERED
            else:
                return EXIT_TIME_IS_REGISTERED if exit_time is None else ATTENDANCE_TIME_IS_RECORD
    except Attendance.DoesNotExist:
        pass
    return NO_RECORD


def apply_attendance(request, pk):
    if request.method == "GET":
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        user = CustomUser.objects.get(pk=pk)
        from django.urls import resolve
        url = request.GET.get("next")
        try:
            # If datetime is today and the time of attendance has not been set before.
            enter_time, exit_time, attendance_id = attendance_helper(user)
            if enter_time is not None:
                if enter_time != datetime.today().day:
                    # Set the attendance time
                    Attendance.objects.create(user=user,
                                              enter=datetime.now())
                    messages.success(request, {'user': pk,
                                               'text': 'حصور ثبت شد.'})

                else:
                    # toggle: then check for exit time.
                    if exit_time is None:
                        Attendance.objects.filter(id=attendance_id).update(exit=datetime.now())
                        messages.success(request, {'user': pk,
                                                   'text': 'ساعت خروج ثبت شد.'})
                    else:
                        messages.error(request, {'user': pk,
                                                 'text': 'قبلا ساعت ورود/خروج ثبت شده است.'})
        except KeyError:
            # Set the attendance time
            Attendance.objects.create(user=user,
                                      enter=datetime.now())
            messages.success(request, {'user': pk,
                                       'text': 'حصور ثبت شد.'})

        resolve(url)
        return HttpResponseRedirect(url)


def attendance_helper(user: CustomUser):
    try:
        attendance = user.attendance.filter(user=user).latest('enter')
        enter_time = attendance.enter.strftime('%H:%M:%S')
        exit_time = ''  # TODO attendance.exit.strftime('%H:%M:%S')
        return enter_time, exit_time, attendance.id
    except Attendance.DoesNotExist:
        return '', '', 0

