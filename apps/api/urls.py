from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('webhook/<str:source_type>/', views.AgentWebhookView.as_view(), name='webhook'),
    path('health/', views.HealthCheckView.as_view(), name='health'),
]
