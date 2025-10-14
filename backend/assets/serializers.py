from rest_framework import serializers
from .models import AssetInstance, AssetModel, Room, Building


class BuildingSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('id', 'name')


class RoomSimpleSerializer(serializers.ModelSerializer):
    building = BuildingSimpleSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'room_code', 'building')


class AssetModelSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetModel
        fields = ('id', 'model_name')


class AssetInstanceMapSerializer(serializers.ModelSerializer):
    asset_model = AssetModelSimpleSerializer(read_only=True)
    room = RoomSimpleSerializer(read_only=True)
    building = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    class Meta:
        model = AssetInstance
        fields = (
            'id',
            'tag',
            'label',
            'is_active',
            'asset_model',
            'room',
            'building',
            'latitude',
            'longitude',
            'description',
        )

    def get_building(self, obj):
        if getattr(obj, 'room', None) and getattr(obj.room, 'building', None):
            return BuildingSimpleSerializer(obj.room.building).data
        return None

    def _find_coord(self, obj, names):
        room = getattr(obj, 'room', None)
        building = getattr(room, 'building', None) if room else None
        for target in (room, building):
            if not target:
                continue
            for n in names:
                val = getattr(target, n, None)
                if val not in (None, ''):
                    try:
                        return float(val)
                    except Exception:
                        pass
        return None

    def get_latitude(self, obj):
        return self._find_coord(obj, ('latitude', 'lat', 'geo_lat'))

    def get_longitude(self, obj):
        return self._find_coord(obj, ('longitude', 'lon', 'lng', 'geo_lon'))