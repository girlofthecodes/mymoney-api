from rest_framework import serializers

from labels.models import Label

class LabelRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = [
            'user',
            'id',
            'label_name',
            'label_type',
            'label_class',
            'label_color',
            'label_description',
        ]

