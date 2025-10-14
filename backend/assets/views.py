from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .models import AssetInstance
from .serializers import AssetInstanceMapSerializer

class AssetInstanceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint returning instances. Includes a map-ready serializer.
    """
    queryset = AssetInstance.objects.select_related('asset_model', 'room', 'room__building').all()
    serializer_class = AssetInstanceMapSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def map(self, request):
        """
        /api/instances/map/  -> returns all instances in map-ready JSON
        """
        qs = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)