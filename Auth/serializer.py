from Auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6,write_only=True,required=True)

    

    class Meta:
        model = User
        fields = '__all__'

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)    