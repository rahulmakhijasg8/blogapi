from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer, UserRegisterSerializer,LoginSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters import rest_framework
from .permissions import IsAuthor, HasApiToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"username": user.username, "email": user.email}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.create(serializer.validated_data)
        return Response({"token": token}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostFilter(rest_framework.FilterSet):
    class Meta:
        model = Post
        fields = ['author', 'created_at']

class PostsViewset(ModelViewSet):
    serializer_class = PostSerializer
    filterset_class = PostFilter

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            self.permission_classes = [IsAuthenticated, IsAuthor] 
        elif self.request.method == 'POST':
            self.permission_classes = [HasApiToken]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()