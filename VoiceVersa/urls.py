from django.urls import path, include
from VoiceVersa import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('audio/', views.AudioList.as_view()),
    path('audio/<int:pk>/', views.AudioDelete.as_view()),
    path('process/', views.ProcessView.as_view()),
    path('voices/', views.VoiceList.as_view()),
    path('add_voice/', views.VoiceAdd.as_view()),
    path('voices/<int:pk>/', views.VoiceManipulate.as_view()),
    path('request/', views.SubmissionAdd.as_view()),
    path('submissions/', views.SubmissionList.as_view()),
    path('submissions/<int:pk>', views.SubmissionManipulate.as_view()),
    path('users/', views.UserList.as_view()),
    path('register/', views.UserRegistrationView.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('login/', obtain_auth_token, name='login'),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

format_suffix_patterns(urlpatterns)
