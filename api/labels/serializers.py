from rest_framework import serializers

from labels.models import Label

class LabelRegisterSerializer(serializers.ModelSerializer):
    labelName = serializers.CharField(source="label_name")
    labelType = serializers.CharField(source="label_type")
    labelClass = serializers.CharField(source="label_class")
    labelColor = serializers.CharField(source="label_color")
    labelDescription = serializers.CharField(source="label_description")
    
    class Meta:
        model = Label
        fields = [
            'user',
            'id',
            'labelName',
            'labelType',
            'labelClass',
            'labelColor',
            'labelDescription',
        ]

