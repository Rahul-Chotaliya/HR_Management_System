from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('employee/', views.emp_table, name='emp_table'),
    path('department/', views.dep_table, name='dep_table'),
    path('department/add/', views.add_dep_view, name='add_dep'),
    path('department/<int:id>/edit/', views.edit_dep_view, name='edit_dep'),
    path('department/<int:id>/delete/', views.delete_dep_view, name='delete_dep'),
    path('employee/<int:id>/edit/', views.edit_emp_view, name='edit_emp'),
    path('employee/<int:id>/delete/', views.delete_emp_view, name='edit_dep'),
    path('employee/add/', views.add_emp_view, name='add_emp'),
    path('password/', views.pass_change_view, name='pass_change'),
    path('email/', views.send_mail, name='send_mail'),
    path('email_message/', views.send_EmailMessage, name='email_message'),
    path('forget/', views.forget_password_views, name='forget_page'),
    path('resend_otp/<int:id>/', views.resend_otp_view, name='resend_otp'),
    path('code/<int:id>/', views.code_views, name='code_page'),
]
