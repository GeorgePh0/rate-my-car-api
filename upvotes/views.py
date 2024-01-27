from rest_framework import generics, permissions, serializers
from .models import Upvote
from .serializers import UpvoteSerializer
from rmc_api.permissions import IsOwnerOrReadOnly


class UpvoteListView(generics.ListCreateAPIView):
    
    serializer_class = UpvoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Upvote.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UpvoteDetail(generics.RetrieveDestroyAPIView):

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = UpvoteSerializer
    queryset = Upvote.objects.all()
