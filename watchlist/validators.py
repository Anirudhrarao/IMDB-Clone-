from rest_framework import serializers

def is_capitalized(value: str):
    if not value.istitle():
        raise serializers.ValidationError("First word of movie name should be capital.")