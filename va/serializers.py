from rest_framework import serializers
# Register serializer
from va.models import UserAccount
from va.models import Post
from va.models import (Cpu, Gpu, Ram)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'password', 'first_name',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = UserAccount.objects.create_user(validated_data['email'],     password=validated_data['password'],
                                               first_name=validated_data['first_name'],)
        return user
# User serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'


class postSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'des', 'title', 'user')


class cpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cpu
        fields = ('id', 'specs', 'title', 'slug')


class gpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gpu
        fields = ('id', 'specs', 'title', 'slug')


class ramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ram
        fields = ('id', 'specs', 'title', 'slug')
