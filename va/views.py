from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Q
from itertools import chain
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
)
from va.serializers import (
    postSerializer,
    RegisterSerializer,
    UserSerializer,
    cpuSerializer,
    gpuSerializer,
    ramSerializer,
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
