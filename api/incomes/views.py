from incomes.models import Income

from incomes.serializers import IncomeRegisterSerializer, IncomeListSerializer, IncomeUpdateSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics

from django_filters import FilterSet, AllValuesFilter, DateFilter, NumberFilter

from django.shortcuts import get_object_or_404



class IncomeRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        
        request.data["user"] = request.user.id
        serializer = IncomeRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        data = {
            'data': serializer.data,
            'msg':'Ingreso registrado exitosamente.'
        }
        return Response(data, status=status.HTTP_201_CREATED)

class IncomeListView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request): 
        incomes = Income.objects.filter(user = request.user.id, status_delete=False)
        serializer = IncomeListSerializer(incomes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IncomeFilter(FilterSet):
    from_date = DateFilter(field_name='income_date', lookup_expr='gte') #Para filtrar por semana.
    to_date = DateFilter(field_name='income_date', lookup_expr='lte') 
    year = NumberFilter(field_name='income_date', lookup_expr='year')
    month = NumberFilter(field_name='income_date', lookup_expr='month')
    day = NumberFilter(field_name='income_date', lookup_expr='day')
    label__class = AllValuesFilter(field_name='label__label_class') 
    label__color = AllValuesFilter(field_name='label__label_color')
    

    class Meta:
        model = Income
        fields = [
            'from_date', 
            'to_date', 
            'year', 
            'month', 
            'day',
            'label__class',
            'label__color'
            ]


class FilterIncomesListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset =Income.objects.all()
    serializer_class = IncomeListSerializer
    name = 'income-list'
    filter_class = IncomeFilter
    search_fields = (
        '^label__label_class',
        '^label__label_color',
    )
    def get_queryset(self):
        return Income.objects.filter(user=self.request.user.id, status_delete=False)


class IncomeUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, id): 
        try: 
            income = Income.objects.get(user = request.user.id, id=id)
            serializer = IncomeUpdateSerializer(income, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if income.status_delete: 
                income.status_delete = True
                return Response({'msg':'No se ha encontrado el ingreso solicitado.'}, status=status.HTTP_404_NOT_FOUND)
            serializer.save() 
            data = {
                'data': serializer.data,
                'msg':'Se actualizó la información del ingreso.'
            }
            return Response(data, status=status.HTTP_200_OK)
        except: 
            return Response({'msg':'Ingreso no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class IncomeDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, id):
        try:
            income = get_object_or_404(Income, user=request.user.id, id=id)
            if income.status_delete: 
                income.status_delete = True
                return Response({'msg':'Este ingreso ya ha sido eliminado.'}, status=status.HTTP_404_NOT_FOUND)
            income.status_delete=True
            income.save()
            return Response({'msg': 'Se ha eliminado el ingreso exitosamente.'}, status=status.HTTP_200_OK)
        except: 
            return Response({'msg':'Ingreso no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
