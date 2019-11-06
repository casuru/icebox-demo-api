from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):


    def create(self, validated_data):

        return User.objects.create_user(**validated_data)


    def update(self, user, validated_data):


        user.email = validated_data.get("email", user.email)
        user.username = validated_data.get("username", user.username)
        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name = validated_data.get("last_name", user.last_name)

        user.save()

        if validated_data.get("password", None) is not None:

            password = validated_data.get("password")

            user.set_password(password)
            user.save() 


        return user


    class Meta:

        model = User
        fields = "__all__"

        extra_kwargs = {

            "password": {
                "write_only": True
            },
            "email":{
                "required": True
            }
        }