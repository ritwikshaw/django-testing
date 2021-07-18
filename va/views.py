from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core import serializers
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from itertools import chain
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from va.models import (
    Post,
    UserAccount,
    Cpu,
    Gpu,
    Ram,
    OrderItem,
    Custom,
)
from va.serializers import (
    postSerializer,
    RegisterSerializer,
    UserSerializer,
    OrderSerializer,
)


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class GetUserView(RetrieveAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = postSerializer


class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = postSerializer


class PostUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = postSerializer


class PostDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()


class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        slug = request.data.get('slug')
        if slug is None:
            return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)

        cpu = Cpu.objects.search(slug)
        gpu = Gpu.objects.search(slug)
        ram = Ram.objects.search(slug)
        queryset_chain = chain(
            cpu,
            gpu,
            ram
        )
        qs = sorted(queryset_chain,
                    key=lambda instance: instance.pk,
                    reverse=True)
        self.count = len(qs)  # since qs is actually a list
        for q in qs:
            order_item_qs = OrderItem.objects.filter(
                object_id=q.id,
                user=request.user,
            )
            if order_item_qs.exists():
                order_item = order_item_qs.first()
                order_item.quantity += 1
                order_item.save()
            else:
                order_item = OrderItem.objects.create(
                    content_object=q,
                    user=request.user,
                )
                order_item.save()

        return JsonResponse(serializers.serialize('json', qs), safe=False)
        # return Response(status=HTTP_200_OK)


class CreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_item = Custom.objects.create(
            user=request.user,
        )
        order_item.save()

        return Response(status=HTTP_200_OK)


class AddCpuView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order = Custom.objects.get(user=self.request.user)
        slug = request.data.get('slug')
        cpu = get_object_or_404(Cpu, slug=slug)
        order.cpu = cpu
        order.save()

        return Response(status=HTTP_200_OK)


class AddGpuView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order = Custom.objects.get(user=self.request.user)
        slug = request.data.get('slug')
        gpu = get_object_or_404(Gpu, slug=slug)
        order.gpu = gpu
        order.save()

        return Response(status=HTTP_200_OK)


class AddRamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order = Custom.objects.get(user=self.request.user)
        slug = request.data.get('slug')
        ram = get_object_or_404(Ram, slug=slug)
        order.ram = ram
        order.save()

        return Response(status=HTTP_200_OK)


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            order = Custom.objects.get(user=self.request.user)
            return order
        except ObjectDoesNotExist:
            return Response("You do not have an active order")
