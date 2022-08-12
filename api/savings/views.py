from savings.models import Saving
from savings.serializers import SavingListSerializer, SavingRegisterSerializer, SavingUpdateSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics

from django_filters import FilterSet, NumberFilter, DateFilter
from django.shortcuts import get_object_or_404


# Create your views here.
class SavingRegisterView(APIView): 
    permissions_classes = [permissions.IsAuthenticated]
    def post(self, request): 
        request.data['user'] = request.user.id
        serializer = SavingRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'data': serializer.data,
            'msg':'Ahorro registrado exitosamente.'
        }
        return Response(data, status=status.HTTP_200_OK)

        
class SavingListView(APIView): 
    permissions_classes = [permissions.IsAuthenticated]
    def get(self, request): 
        saving = Saving.objects.filter(user = request.user.id, status_delete=False)
        serializer = SavingListSerializer(saving, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SavingFilter(FilterSet): 
    from_saving_date = DateFilter(field_name='saving_date', lookup_expr='gte')
    to_saving_date = DateFilter(field_name='saving_date', lookup_expr='lte')

    year = NumberFilter(field_name='saving_date', lookup_expr='year')  
    month = NumberFilter(field_name='saving_date', lookup_expr='month') 
    day = NumberFilter(field_name='saving_date', lookup_expr='day') 

    class Meta: 
        model = Saving
        fields = [
            'from_saving_date', 
            'to_saving_date', 
            'year', 
            'month', 
            'day',
        ]


class FilterSavingListView(generics.ListCreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    queryset = Saving.objects.all()
    serializer_class = SavingListSerializer
    name = 'saving-list'
    filter_class = SavingFilter
    def get_queryset(self):
        return Saving.objects.filter(user=self.request.user.id, status_delete=False)


class SavingUpdateView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, id): 
        try: 
            saving = Saving.objects.get(user = request.user.id, id=id)
            serializer = SavingUpdateSerializer(saving, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if saving.status_delete: 
                saving.status_delete = True
                return Response({'msg':'No se ha encontrado el ahorro solicitado.'}, status=status.HTTP_404_NOT_FOUND)
            serializer.save() 
            data = {
                'data': serializer.data,
                'msg':'Se actualizó la información del ahorro.'
            }
            return Response(data, status=status.HTTP_200_OK)
        except: 
            return Response({'msg':'Ahorro no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class SavingDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, id):
        try: 
            saving = get_object_or_404(Saving, user=request.user.id, id=id)
            if saving.status_delete: 
                saving.status_delete = True
                return Response({'msg':'Este ahorro ya ha sido eliminado.'}, status=status.HTTP_404_NOT_FOUND)
            saving.status_delete=True
            saving.save()
            return Response({'msg': 'Se ha eliminado el ahorro exitosamente.'}, status=status.HTTP_200_OK)
        except: 
            return Response({'msg':'Ahorro no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
