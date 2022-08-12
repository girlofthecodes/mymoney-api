from expenses.serializers import ExpenseListSerializer
from incomes.serializers import IncomeListSerializer
from savings.serializers import SavingListSerializer

from expenses.views import FilterExpensesListView
from incomes.views import FilterIncomesListView
from savings.views import FilterSavingListView


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Get(APIView):
    def get(self, request):
        ff_expense = FilterExpensesListView()
        ff_income = FilterIncomesListView()
        ff_saving = FilterSavingListView()

        ff_expense.request = request
        ff_income.request = request
        ff_saving.request = request

        expense_filtered = ff_expense.filter_queryset(ff_expense.get_queryset()) 
        income_filtered = ff_income.filter_queryset(ff_income.get_queryset()) 
        saving_filtered = ff_saving.filter_queryset(ff_saving.get_queryset())
        
        suma_expense = 0 
        suma_income = 0
        suma_saving = 0 
        for filtro_expense in expense_filtered.values('expense_amount'):   
            for i in filtro_expense.values(): 
                suma_expense = suma_expense + i
        for filtro_income in income_filtered.values('income_amount'): 
            for i in filtro_income.values(): 
                suma_income = suma_income + i
        for filtro_saving in saving_filtered.values('saving_amount'): 
            for i in filtro_saving.values(): 
                suma_saving = suma_saving + i
        serializer_expense = ExpenseListSerializer(expense_filtered, many=True)
        serializer_income = IncomeListSerializer(income_filtered, many=True)
        serializer_saving = SavingListSerializer(saving_filtered, many=True)
        data = {
            'expense': serializer_expense.data,
            'income': serializer_income.data,
            'saving': serializer_saving.data, 
            'total_expense': suma_expense,
            'total_income': suma_income,
            'total_saving': suma_saving,
        }
        return Response(data, status=status.HTTP_200_OK)
