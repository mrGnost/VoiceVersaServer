from django.contrib.auth.models import User
from rest_framework import generics, permissions
from VoiceVersa.models import Audio, Voice, Submission, Processing
from VoiceVersa.serializers import AudioSerializer, UserSerializer, \
    VoiceSerializer, SubmissionSerializer, ProcessingSerializer
from VoiceVersa.permissions import IsOwner
from VoiceVersa.stargan_api import process_audio
import logging


logger = logging.getLogger(__name__)


class AudioList(generics.ListCreateAPIView):
    serializer_class = AudioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Audio.objects.filter(owner=self.request.user)


class AudioDelete(generics.DestroyAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = [IsOwner | permissions.IsAdminUser]


class ProcessView(generics.CreateAPIView):
    queryset = Processing.objects.all()
    serializer_class = ProcessingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        audio = serializer.save()
        name = audio.url.name.split('/')[-1]
        print("name:", name)
        process_audio(name, audio.voice)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VoiceList(generics.ListAPIView):
    queryset = Voice.objects.all()
    serializer_class = VoiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class VoiceAdd(generics.CreateAPIView):
    queryset = Voice.objects.all()
    serializer_class = VoiceSerializer
    permission_classes = [permissions.IsAdminUser]


class VoiceManipulate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voice.objects.all()
    serializer_class = VoiceSerializer
    permission_classes = [permissions.IsAdminUser]


class SubmissionAdd(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubmissionList(generics.ListAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAdminUser]


class SubmissionManipulate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAdminUser]
