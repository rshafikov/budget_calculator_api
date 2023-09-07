from datetime import datetime

from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, CustomUser
from .serializers import (CategorySerializer, RecordSerializer,
                          AdminCategorySerializer, CustomUserSerializer)
from .permissions import IsAdminUser


class RecordViewSet(viewsets.ModelViewSet):
    """Вьюсет для записей расходов"""
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        month = datetime.now().month
        return self.request.user.records.filter(created__month=month).all()

    @action(detail=False, url_path='total-spend')
    def total(self, request):
        month = datetime.now().month
        day = datetime.now().day
        user_records = self.request.user.records.all()
        total_spend = user_records.aggregate(Sum('amount'))
        total_spend_per_month = (
            user_records.filter(created__month=month).aggregate(Sum('amount'))
        )
        total_spend_per_category = (
            user_records
            .values('category')
            .annotate(total=Sum('amount'))
        )
        total_spend_per_day = (
            user_records.filter(created__day=day).aggregate(Sum('amount'))
        )
        return Response({
            'total': total_spend['amount__sum'],
            'current_month': total_spend_per_month['amount__sum'],
            'current_day': total_spend_per_day['amount__sum'],
            'summary': total_spend_per_category}
        )


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        user = self.request.user
        if user.is_admin:
            return AdminCategorySerializer
        return CategorySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Category.objects.all()
        return user.categories.all()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser, ]
    queryset = CustomUser.objects.all()
