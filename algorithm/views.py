from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from algorithm.models import *
from algorithm.serializers import *
import networkx as nx
from algorithm.services import *
from algorithm.data_service import Data


# DATA = Data()


class CharacteristicViewSet(viewsets.ModelViewSet):
    """
    The api endpoint of the characteristics.
    """

    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer


class EdgeViewSet(viewsets.ModelViewSet):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ShortestPath(APIView):
    """
    The api endpoint of the characteristics.
    """

    def get(self, request):

        # Prepare the graph
        nodes = list(Characteristic.objects.values())
        edges = list(Edge.objects.values())
        graph = prepare_graph(nodes, edges)
        params = request.query_params
        if len(params) != 2:
            return Response("Please specify a source and a target.", status=status.HTTP_204_NO_CONTENT)
        else:
            source = params['source']
            target = params['target']
            length, path = shortest_path(graph, source, target)

            negation = False
            opposite = list(Characteristic.objects.filter(value=target).values())[0]['opposite']
            if opposite != '':
                length_neg, path_neg = shortest_path(graph, source, opposite)
                if 0 < length_neg < length:
                    negation = True
                    path = path_neg
                    length = length_neg

            response = {
                'length': length,
                'path': path,
                'negation': negation
            }

            return Response(response)
