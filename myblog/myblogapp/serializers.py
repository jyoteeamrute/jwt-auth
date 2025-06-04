from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model=User
        fields=['email','name','phone','password','password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        # if attrs['password']!=attrs['password2']:
        if password!=password2:
            raise serializers.ValidationError("Password and Confirm Password does not match")
        return attrs
    def create(self, validated_data):
        validated_data.pop('password2')  # remove password2 before passing to create_user
  
        return User.objects.create_user(**validated_data)
    
    
class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid email or password")    
# class UserRegistrationSerializer(serializers.ModelSerializer):
    # author = UserSerializer(read_only=True)
#     comments_count = serializers.SerializerMethodField()
#     likes_count = serializers.SerializerMethodField()

#     class Meta:
#         model = MyBlogPost
#         fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'comments_count', 'likes_count']

#     def get_comments_count(self, obj):
#         return obj.comments.count()

#     def get_likes_count(self, obj):
#         return obj.likes.count()

# class CommentSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = Comment
#         fields = ['id', 'post', 'user', 'text', 'created_at']

# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Like
#         fields = ['id', 'post', 'user', 'created_at']
            
