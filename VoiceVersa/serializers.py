from rest_framework import serializers
from VoiceVersa.models import Audio, Voice, Submission
from django.contrib.auth.models import User


class AudioSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    audio = serializers.FileField()

    class Meta:
        model = Audio
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        audio = {
            "url": representation.pop("audio"),
            "size": instance.audio.size,
            "name": instance.audio.name,
        }
        representation['audio'] = audio
        return representation


class UserSerializer(serializers.ModelSerializer):
    audio = serializers.PrimaryKeyRelatedField(many=True, queryset=Audio.objects.all(), required=False)

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'audio']

    def create(self, validated_data, **kwargs):
        """
        Overriding the default create method of the Model serializer.
        """
        print(validated_data)
        user = User(
            username=validated_data["username"]
        )
        password = validated_data["password"]
        user.set_password(password)
        user.save()
        return user


class VoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voice
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    archive = serializers.FileField()

    class Meta:
        model = Submission
        fields = '__all__'
