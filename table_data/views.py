import datetime
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.utils import timezone

from table_data.forms import DepartmentForm, EmployeeForm
from table_data.models import Employee, Department, VerifyOtp
from .djnago_email_server import send, email
from .utils import send_email, generate_otp

LOGIN_URL = "/login/"


def send_mail(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        html_content = request.POST.get('html')
        recipient = request.POST.get('recipient').split(',')
        print(recipient)
        send(subject=subject, message=message, html_message=html_content, recipients=recipient)
        return redirect('/home/')
    template = loader.get_template('email_page.html')
    return HttpResponse(template.render({}, request))


def send_EmailMessage(request):
    context = {}
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        reply_to = request.POST.get('reply_to')
        try:
            cc = request.POST.get('cc').split(',')
            to = request.POST.get('to').split(',')
            bcc = request.POST.get('bcc').split(',')
            email(subject=subject, body=body, to=to, cc=cc, bcc=bcc, reply_to=reply_to)

            return redirect('/home/')
        except Exception as ex:
            print(ex)
            context['error'] = "please enter valid email"
    template = loader.get_template('email_message.html')
    return HttpResponse(template.render(context, request))


def forget_password_views(request):
    context = {}
    if request.method == 'POST':
        email_id = request.POST.get('email')
        try:
            user = User.objects.get(email=email_id)
        except:
            context['error'] = "Please enter valid email id"
        else:
            if user is not None:
                try:
                    verify_otp = VerifyOtp.objects.get(user=user)
                    if verify_otp.exp > timezone.localtime(timezone.now()):
                        otp = verify_otp.otp
                    else:
                        verify_otp.delete()
                        otp = None
                except:
                    otp = None

                if otp is None:
                    otp = generate_otp()
                    exp = timezone.localtime(timezone.now()) + datetime.timedelta(minutes=15)
                    obj = VerifyOtp(otp=otp, user=user, exp=exp)
                    obj.save()

                send_email(otp, email_id)
                return redirect(f'/code/{user.id}')
    template = loader.get_template('forget_page.html')
    return HttpResponse(template.render(context, request))


def resend_otp_view(id):
    user = User.objects.get(id=id)
    obj = VerifyOtp.objects.get(user=user)
    exp = obj.exp
    otp = obj.otp
    email_id = user.email
    if exp > timezone.localtime(timezone.now()):
        send_email(otp, email_id)
    elif exp < timezone.localtime(timezone.now()):
        obj.delete()
        otp = generate_otp()
        exp = timezone.localtime(timezone.now()) + datetime.timedelta(minutes=15)
        obj = VerifyOtp(otp=otp, user=user, exp=exp)
        obj.save()
        send_email(otp, email_id)
    return redirect(f'/code/{id}')


def code_views(request, id):
    context = {
        'id': id,
    }
    user = User.objects.get(id=id)
    if request.method == 'POST':
        msg = request.POST.get('code')
        try:
            user = User.objects.get(id=id)
        except Exception as e:
            print(e)

        obj = VerifyOtp.objects.get(user=user)
        expiry = obj.exp
        code = str(obj.otp)
        if msg == code:
            if expiry < timezone.localtime(timezone.now()):
                context['greater15'] = "Your Last OTP was Expired, Please Resend OTP"
            else:
                login(request, user)
                obj.delete()
                return redirect('/password/')
        else:
            context['error'] = " Please Enter Valid OTP"

    template = loader.get_template('code_page.html')
    return HttpResponse(template.render(context, request))


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/employee/')
    context = {}
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('/home/')
        else:
            context['error_msg'] = 'Invalid Login'

    template = loader.get_template('login_page.html')
    return HttpResponse(template.render(context, request))


def logout_view(request):
    logout(request)

    return redirect('/login/')


@login_required(login_url=LOGIN_URL)
def home_view(request):
    emp = Employee.objects.all().order_by('-id')[:5]
    dep = Department.objects.all().order_by('-id')[:5]
    context = {
        'emp': emp,
        'dep': dep,
    }
    user = request.user
    if user.first_name is not None:
        result = user.first_name
    elif user.last_name is not None:
        result = user.last_name
    else:
        result = user.username
    context['uname'] = result
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_URL)
def pass_change_view(request):
    user = request.user
    context = {}
    if request.method == 'POST':
        pas = request.POST.get('pas')
        c_pass = request.POST.get('c_pas')
        if pas != c_pass:
            context['error'] = "Please enter Match Password"
        else:
            user.set_password(pas)
            user.save()
            context['changed'] = " Password Changed Successfully"
    template = loader.get_template('change_password.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_URL)
def emp_table(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    template = loader.get_template('employee_table.html')
    emp_list = Employee.objects.all()
    age_filter = request.GET.get('Age_filter')
    if age_filter == "young":
        emp_list = emp_list.filter(age__gt=18, age__lte=50)
    elif age_filter == 'minor':
        emp_list = emp_list.filter(age__lte=18)
    elif age_filter == 'senior':
        emp_list = emp_list.filter(age__gt=50)

    salary_filter = request.GET.get('sl_filter')
    if salary_filter == 'lt20':
        emp_list = emp_list.filter(salary__lt=20000)
    elif salary_filter == 'lt50':
        emp_list = emp_list.filter(salary__lte=50000, salary__gt=20000)
    elif salary_filter == 'gt50':
        emp_list = emp_list.filter(salary__gt=50000)
    context = {
        "Employee_list": emp_list,
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url="/home/")
def add_emp_view(request):
    dep_list = Department.objects.all()
    context = {
        "Department_list": dep_list
    }
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/employee/')
    form = EmployeeForm()
    context['form'] = form
    template = loader.get_template('add_employee.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url="/home/")
def edit_emp_view(request, id):
    dep_list = Department.objects.all()
    emp = Employee.objects.get(id=id)
    context = {
        'emp': emp,
        "Department_list": dep_list
    }
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()

        return redirect('/employee/')
    else:
        form = EmployeeForm(instance=emp)
    context["form"] = form
    template = loader.get_template('add_employee.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url="/home/")
def dep_table(request):
    template = loader.get_template('department.html')
    dep_list = Department.objects.all().values()
    context = {
        "Department_list": dep_list
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="/login/")
def add_dep_view(request):
    context = {}
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/department/')
    form = DepartmentForm()
    context['form'] = form
    template = loader.get_template('add_department.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url="/home/")
def edit_dep_view(request, id):
    dep = Department.objects.get(id=id)
    context = {
        'dep': dep
    }
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dep)
        if form.is_valid():

            form.save()
        context['msg'] = "Department updated successfully."
    else:
        form = DepartmentForm(instance=dep)
    context['form'] = form
    template = loader.get_template('add_department.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url="/home/")
def delete_dep_view(id):
    try:
        dep = Department.objects.get(id=id)
        dep.delete()
    except:
        pass
    return redirect('/department/')


@login_required(login_url="/home/")
def delete_emp_view(id):
    try:
        dep = Employee.objects.get(id=id)
        dep.delete()
    except:
        pass
    return redirect('/employee/')
