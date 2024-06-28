from rest_framework import serializers
from watchlist.models import WatchList, StreamPlatform, Review 

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist',)
        
class WatchListSerializer(serializers.ModelSerializer): 
    platform = serializers.CharField(source='platform.name', read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"
    
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"     


        