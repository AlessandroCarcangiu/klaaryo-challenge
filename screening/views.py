from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Candidate
from .serializers import CandidateSerializer
from .tasks import run_screening


class CandidateCreateView(generics.CreateAPIView):
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        candidate = serializer.save()
        run_screening.delay(str(candidate.id))


class CandidateDetailView(generics.RetrieveAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
