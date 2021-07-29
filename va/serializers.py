from django.contrib.contenttypes import fields
from django.db import models
from rest_framework import serializers
from generic_relations.relations import GenericRelatedField
from va.models import UserAccount
from va.models import Post
from va.models import (Cpu, Gpu, Ram, OrderItem, Custom,
                       Gamingpc, Pcpart, Pcprice, Pcdes)


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
        fields = ('id', 'specs', 'title', 'slug', 'price')


class gpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gpu
        fields = ('id', 'specs', 'title', 'slug', 'price')


class ramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ram
        fields = ('id', 'specs', 'title', 'slug', 'price')


class orderitemSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    content_object = GenericRelatedField({
        Cpu: cpuSerializer(),
        Gpu: gpuSerializer(),
        Ram: ramSerializer(),
    })

    class Meta:
        model = OrderItem
        fields = ('id', 'user', 'content_object',)

    def get_user(self, obj):
        return UserSerializer(obj.user).data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom
        fields = ('id', 'cpu', 'user', 'ram', 'gpu',)

    def get_item(self, obj):
        return cpuSerializer(obj.cpu).data

    def get_final_price(self, obj):
        return obj.get_total_item_price()


class PcpartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pcpart
        fields = ('id', 'name', 'wifi', 'blutooth', 'vr', 'stream')


class PcpriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pcprice
        fields = ('id', 'name', 'price', 'qua', 'ava')


class PcdesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pcdes
        fields = ('id', 'des1', 'des2')


class gamingpcSerializer(serializers.ModelSerializer):
    part = serializers.SerializerMethodField()
    des = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Gamingpc
        fields = ('id', 'name', 'cpu', 'gpu', 'ram',
                  'des', 'price', 'part')

    def get_part(self, obj):
        return PcpartSerializer(obj.part).data

    def get_des(self, obj):
        return PcdesSerializer(obj.des).data

    def get_price(self, obj):
        return PcpriceSerializer(obj.price).data
