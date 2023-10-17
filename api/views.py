from datetime import datetime, timedelta

from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from django.shortcuts import get_object_or_404

from .models import Category, CustomUser
from .serializers import (
    CategoryUserSerializer, RecordUserSerializer,
    RecordAdminSerializer, CategoryAdminSerializer, CustomUserSerializer)
from .permissions import IsAdminUser


class RecordViewSet(viewsets.ModelViewSet):
    """Вьюсет для записей расходов"""
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        user = self.request.user
        if user.is_admin:
            return RecordAdminSerializer
        return RecordUserSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        month = datetime.now().month
        return self.request.user.records.filter(
            created__month=month).order_by('-created').all()

    @action(detail=False, url_path='total-spend')
    def total(self, request):
        period = request.query_params.get('period', 'day')

        now = datetime.now()
        user_records = self.request.user.records.all

        if period == 'month':
            month = now.month
            total_spend_per_period = user_records().filter(created__month=month, created__year=now.year)
        elif period == 'week':
            start_week = now - timedelta(days=now.weekday())
            total_spend_per_period = user_records().filter(created__date__gte=start_week)
        elif period == 'day':
            day = now.day
            total_spend_per_period = user_records().filter(
                created__day=day, created__month=now.month, created__year=now.year)
        else:
            total_spend_per_period = user_records()

        total_spend_per_category = total_spend_per_period.values(
            'category__category_name').annotate(total=Sum('amount'))

        return Response({
            'period': period,
            'total_per_period': total_spend_per_period.aggregate(Sum('amount'))['amount__sum'],
            'summary': total_spend_per_category
        })


class CategoryViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        user = self.request.user
        if user.is_admin:
            return CategoryAdminSerializer
        return CategoryUserSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Category.objects.all()
        return user.categories.all()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAdminUser, ]
    queryset = CustomUser.objects.all()

# TODO: fix this problem with currency
    @action(methods=['POST', 'GET'], detail=False, permission_classes=[AllowAny, ])
    def my_currency(self, request):
        try:
            user = self.request.user
        except Exception as err:
            raise NotAuthenticated from err

        if request.method == 'POST':
            currency = request.data.get('currency', 'RUB')
            user.currency = currency
            user.save()
            return Response({'currency': f'{currency}'})

        return Response({'currency': f'{user.currency}'})
