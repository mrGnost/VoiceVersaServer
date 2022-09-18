from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from VoiceVersa.models import Audio, Voice, Submission
from VoiceVersa.serializers import AudioSerializer, UserSerializer, VoiceSerializer, SubmissionSerializer
from VoiceVersa.permissions import IsOwner
from VoiceVersa.stargan_api import process_audio
import logging


logger = logging.getLogger(__name__)


class AudioList(generics.ListCreateAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        audio = serializer.save(owner=self.request.user)
        name = audio.audio.name.split('/')[-1]
        process_audio(name, audio.voice)


class AudioDelete(generics.DestroyAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = [IsOwner | permissions.IsAdminUser]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration view.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """
        Post request to register a user
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "User": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class VoiceList(generics.ListAPIView):
    queryset = Voice.objects.all()
    serializer_class = VoiceSerializer


class VoiceAdd(generics.CreateAPIView):
    queryset = Voice.objects.all()
    serializer_class = VoiceSerializer
    permission_classes = [permissions.IsAdminUser]


class SubmissionAdd(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubmissionList(generics.ListAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAdminUser]


class SubmissionManipulate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAdminUser]
