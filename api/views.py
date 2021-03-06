from datetime import datetime

from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer, RecordSerializer

MONTH = datetime.now().month
DAY = datetime.now().day


class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.records.filter(created__month=MONTH).all()

    @action(detail=False, url_path='total-spend')
    def total(self, request):
        user_records = self.request.user.records.all()
        total_spend = user_records.aggregate(Sum('amount'))
        total_spend_per_month = (
            user_records.filter(created__month=MONTH).aggregate(Sum('amount'))
        )
        total_spend_per_category = (
            user_records
            .order_by('-total')
            .values('category')
            .annotate(total=Sum('amount'))
        )
        total_spend_per_day = (
            user_records.filter(created__day=DAY).aggregate(Sum('amount'))
        )
        return Response({
            'total': total_spend['amount__sum'],
            'current_month': total_spend_per_month['amount__sum'],
            'current_day': total_spend_per_day['amount__sum'],
            'summary': total_spend_per_category}
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
