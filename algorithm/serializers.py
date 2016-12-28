from algorithm.models import *
from rest_framework import serializers


class CharacteristicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Characteristic
        fields = ('value', 'opposite')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('value', 'sub_groups')


class EdgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Edge
        fields = ('weight', 'source', 'destination', 'is_negative')
