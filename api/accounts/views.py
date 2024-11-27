from accounts.models import Account

from accounts.serializers import AccountRegisterSerializer

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

# Create your views here.
class AccountRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        request.data["user"] = request.user.id
        serializer = AccountRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        data = {
            'data': serializer.data,
            'msg':'Cuenta registrada exitosamente.'
        }
        return Response(data, status=status.HTTP_201_CREATED)

class AccountsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = Account.objects.filter(user = request.user.id, status_delete = False)
        serializer = AccountRegisterSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class AccountIDListView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        try: 
            user = Account.objects.get(user = request.user.id, id=id, status_delete = False)
            serializer = AccountRegisterSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except: 
            return Response({'msg':'La cuenta no existe'},status=status.HTTP_404_NOT_FOUND)


class AccountUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, id):
        account = Account.objects.get(user = request.user.id, id=id)
        serializer = AccountRegisterSerializer(account, data=request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        if account.status_delete: 
            account.status_delete = True
            return Response({'msg':'Cuenta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        serializer.save() 
        data = {
            'data': serializer.data,
            'msg':'Se actualizó la información de la cuenta.'
        }
        return Response(data, status=status.HTTP_200_OK)

class AccountDeleteView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, id): 
        try: 
            account = get_object_or_404(Account, user = request.user.id, id=id)
            if account.status_delete: 
                account.status_delete = True
                return Response({'msg':'La cuenta ya ha sido eliminada.'}, status=status.HTTP_404_NOT_FOUND)
            account.status_delete = True
            account.save()
            return Response({'msg':'Se ha eliminado la cuenta con éxito.'}, status=status.HTTP_200_OK)
        except: 
            return Response({'msg':'Cuenta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
