from rest_framework.decorators import action
from .controllers import RestaurantController
from rest_framework.response import Response
from rest_framework import viewsets
from restaurantback.utility import *
from rest_framework import status
from .models import RestaurantDetails
from .serializers import RestaurantListSerializer


class RestaurantViewset(viewsets.ModelViewSet, RestaurantController):
	queryset = RestaurantDetails.objects.all()
	serializer_class = RestaurantListSerializer

	@action(detail=False, url_path="save-list")
	def save_restaurant_list(self, request):
		try:
			msg = self.save_restaurant_list_data(request)
			return Response(msg, status=status.HTTP_201_CREATED)
		except Exception as e:
			exception_detail(e)
			return Response({'status': 'error'}, status=status.HTTP_300_MULTIPLE_CHOICES)

	@action(detail=False, url_path="get-list", methods=['POST'])
	def get_restaurant_list(self, request):
		try:
			ret_obj = self.get_restaurant_list_data(request)
			return Response(ret_obj, status=status.HTTP_201_CREATED)
		except Exception as e:
			exception_detail(e)
			return Response({'success': 'False'}, status=status.HTTP_300_MULTIPLE_CHOICES)

	@action(detail=False, url_path="get-location", methods=['GET'])
	def get_restaurant_location(self, request):
		try:
			ret_obj = self.get_restaurant_location_data(request)
			return Response(ret_obj, status=status.HTTP_201_CREATED)
		except Exception as e:
			exception_detail(e)
			return Response({'success': 'False'}, status=status.HTTP_300_MULTIPLE_CHOICES)

