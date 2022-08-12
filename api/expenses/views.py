from expenses.models import Expense

from expenses.serializers import ExpenseRegisterSerializer, ExpenseListSerializer, ExpenseUpdateSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import generics

from django_filters import FilterSet, AllValuesFilter, NumberFilter, DateFilter

from django.shortcuts import get_object_or_404



class ExpenseRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request): 
        request.data["user"] = request.user.id
        serializer = ExpenseRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        data = {
            'data': serializer.data,
            'msg':'Gasto registrado exitosamente.'
        }
        return Response(data, status=status.HTTP_201_CREATED)


class ExpensesListView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request): 
        expenses = Expense.objects.filter(user = request.user.id, status_delete=False)
        serializer = ExpenseListSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseFilter(FilterSet):
    from_date = DateFilter(field_name='expense_date', lookup_expr='gte') 
    to_date = DateFilter(field_name='expense_date', lookup_expr='lte')
    year = NumberFilter(field_name='expense_date', lookup_expr='year')
    month = NumberFilter(field_name='expense_date', lookup_expr='month')
    day = NumberFilter(field_name='expense_date', lookup_expr='day')
    label__class = AllValuesFilter(field_name='label__label_class') 
    
    class Meta:
        model = Expense
        fields = [
            'from_date', 
            'to_date', 
            'year', 
            'month', 
            'day',
            'label__class'
            ]


class FilterExpensesListView(generics.ListCreateAPIView): 
    permission_classes = [permissions.IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseListSerializer
    name = 'expense-list'
    filter_class = ExpenseFilter
    search_fields = (
        '^label__label_class',
    )
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user.id, status_delete=False)


class ExpenseUpdateView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, id): 
        try: 
            expense = Expense.objects.get(user = request.user.id, id=id)
            serializer = ExpenseUpdateSerializer(expense, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if expense.status_delete: 
                expense.status_delete = True
                return Response({'msg':'No se ha encontrado el gasto solicitado.'}, status=status.HTTP_404_NOT_FOUND)
            serializer.save() 
            data = {
                'data': serializer.data,
                'msg':'Se actualizó la información del gasto.'
            }
            return Response(data, status=status.HTTP_200_OK)
        except: 
            return Response({'msg':'Gasto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class ExpenseDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, id):
        try: 
            expense = get_object_or_404(Expense, user=request.user.id, id=id)
            if expense.status_delete: 
                expense.status_delete = True
                return Response({'msg':'Este gasto ya ha sido eliminado.'}, status=status.HTTP_404_NOT_FOUND)
            expense.status_delete=True
            expense.save()
            return Response({'msg': 'Se ha eliminado el gasto exitosamente.'}, status=status.HTTP_200_OK)
        except: 
            return Response({'msg':'Gasto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
