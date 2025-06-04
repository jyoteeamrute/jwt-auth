from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

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



User = get_user_model()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist")
        return value

    def create_reset_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, data):
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            payload = AccessToken(data['token'])
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            data['user'] = user
        except Exception as e:
            raise serializers.ValidationError("Invalid or expired token")
        return data

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['password'])
        user.save()
    
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
            
