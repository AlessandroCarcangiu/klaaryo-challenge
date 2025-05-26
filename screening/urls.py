from django.urls import path
from .views import CandidateCreateView, CandidateDetailView

urlpatterns = [
    path('candidates/', CandidateCreateView.as_view(), name='candidate-create'),
    path('candidates/<uuid:id>/', CandidateDetailView.as_view(), name='candidate-detail'),
]
