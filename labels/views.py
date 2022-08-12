from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from labels.models import Label
from labels.serializers import LabelRegisterSerializer

from django.shortcuts import get_object_or_404

# Create your views here.

#Labels 
class LabelRegisterView(APIView): 
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request): 
        request.data['user']=request.user.id
        serializer= LabelRegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        label_data = {
                'data': serializer.data,
                'msg': 'Etiqueta registrada exitosamente'
        }

        return Response(label_data, status=status.HTTP_201_CREATED)


class LabelsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        labels = Label.objects.filter(user = request.user.id, status_delete=False)
        serializer = LabelRegisterSerializer(labels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FilterLabelsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LabelRegisterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['label_type', 'label_class', 'label_color']
    def get_queryset(self):
        return Label.objects.filter(user=self.request.user.id, status_delete=False)


class LabelUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, id):
        try:
            label = Label.objects.get(user=request.user.id, id=id)
            serializer = LabelRegisterSerializer(label, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if label.status_delete:
                label.status_delete = True
                return Response({'msg':'Etiqueta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
            serializer.save()         
            data = {
                'data': serializer.data,
                'msg': 'Se actualizó la etiqueta correctamente.'
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({'msg': 'No se ha encontrado la etiqueta.'}, status=status.HTTP_404_NOT_FOUND)


class LabelDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, id):
        try: 
            label = get_object_or_404(Label, user=request.user.id, id=id)
            if label.status_delete: 
                label.status_delete = True
                return Response({'msg':'La etiqueta ya ha sido eliminada.'}, status=status.HTTP_404_NOT_FOUND)
            label.status_delete=True
            label.save()
            return Response({'msg': 'Se ha eliminado la etiqueta exitosamente.'}, status=status.HTTP_200_OK)
        except: 
            return Response({'msg': 'No se ha encontrado la etiqueta.'}, status=status.HTTP_404_NOT_FOUND)