from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, LoginView, UserProfileView, PredictionView, PredictionListView,
    PredictionDetailView, BlogListView, BlogDetailView, BlogCreateView,
    BlogBookmarkView, UserBookmarksView, ContactView, health_check, StatsView,
    ChatAPIView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),

    # User Profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('stats/', StatsView.as_view(), name='stats'),

    # Predictions
    path('predictions/', PredictionView.as_view(), name='prediction'),
    path('predictions/list/', PredictionListView.as_view(), name='prediction_list'),
    path('predictions/<int:pk>/', PredictionDetailView.as_view(), name='prediction_detail'),

    # Blogs
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/<int:blog_id>/bookmark/', BlogBookmarkView.as_view(), name='blog_bookmark'),
    path('bookmarks/', UserBookmarksView.as_view(), name='user_bookmarks'),

    # Contact
    path('contact/', ContactView.as_view(), name='contact'),

    # Health Check
    path('health/', health_check, name='health_check'),

    # Chat
    path('chat/', ChatAPIView.as_view(), name='chat_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)