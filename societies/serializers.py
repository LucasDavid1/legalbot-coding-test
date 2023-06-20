from rest_framework import serializers
from societies.models import Society, Partner, Administrator, Faculty


class SocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Society
        fields = '__all__'


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'


class PartnerAdministratorSerializer(serializers.Serializer):
    partners = PartnerSerializer(many=True)
    administrators = AdministratorSerializer(many=True)
