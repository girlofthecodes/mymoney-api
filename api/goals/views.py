from goals.models import Goal

from goals.serializers import GoalRegisterSerializer, GoalListSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from django.shortcuts import get_object_or_404



# Create your views here.
class GoalRegisterView(APIView): 
    queryset = Goal.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request): 
        request.data['user'] = request.user.id
        serializer = GoalRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    
        serializer.save()
        data = {
            'data': serializer.data, 
            'msg': 'Meta registrada exitosamente.'
        }
        return Response(data, status=status.HTTP_201_CREATED)
    

class GoalListview(APIView): 
    permission_calsses = [permissions.IsAuthenticated]
    def get(self, request): 
        goal = Goal.objects.filter(user = request.user.id, status_delete=False)
        serializer = GoalListSerializer(goal, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
class GoalUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, id): 
        try: 
            goal = Goal.objects.get(user = request.user.id, id=id)
            serializer = GoalRegisterSerializer(goal, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if goal.status_delete:
                goal.status_delete = True
                return Response({'msg':'No se ha encontrado la meta solicitada.'}, status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            data = {
                'data': serializer.data,
                'msg': 'Se actualizó la información de la meta.'
            }
            return Response(data, status=status.HTTP_200_OK)
        except: 
            return Response({'msg':'Meta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)


class GoalDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, id):
        try: 
            goal = get_object_or_404(Goal, user=request.user.id, id=id)
            if goal.status_delete: 
                goal.status_delete = True
                return Response({'msg':'Esta meta ya ha sido eliminada.'}, status=status.HTTP_404_NOT_FOUND)
            goal.status_delete=True
            goal.save()
            return Response({'msg': 'Se ha eliminado la meta exitosamente.'}, status=status.HTTP_200_OK)
        except: 
            return Response({'msg':'Meta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
