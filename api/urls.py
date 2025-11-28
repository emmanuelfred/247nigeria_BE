from django.urls import path
from .views import signup,verify_identity, verify_email, login_view,update_profile,request_password_reset,verify_otp,reset_password ,resend_verification,update_password,update_email

urlpatterns = [
    path('signup/', signup),
    path('identity/<int:user_id>/', verify_identity),
    path('verify-email/<uid>/<token>/', verify_email),
    path("login/", login_view, name="login"),
    path("update-profile/", update_profile),
    path('forgot-password/', request_password_reset, name='forgot-password'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('reset-password/', reset_password, name='reset-password'),
    path('resend-verification/', resend_verification, name='resend-verification'),
    path("update-password/<int:user_id>/", update_password, name="update-password"),
    path("update-email/<int:user_id>/", update_email, name="update-email"),

    
]
