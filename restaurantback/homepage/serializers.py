from .models import *
from rest_framework import serializers


class RestaurantListSerializer(serializers.ModelSerializer):
	cost_symbol = serializers.CharField(source="currency.symbol")
	rating_text = serializers.CharField(source="rating.text")
	rating_color = serializers.SerializerMethodField()

	class Meta:
		model = RestaurantDetails
		fields = ('id', 'rest_id', 'rest_name', 'avg_cost', 'cost_symbol', 'has_tbl', 'has_online', 'agreegate',
				  'rating_text', 'rating_color', 'votes')

	def get_rating_color(self, obj):
		try:
			color = obj.rating.color
			return color.replace(' ', '')
		except Exception as e:
			print(e.args)
			return ''

class CuisineListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Cuisine
		fields = ('id', 'name')


class CurrencyListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Currency
		fields = ('id', 'name', 'symbol')


class RatingListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Rating
		fields = ('id', 'text', 'color')


class CuisineMappingSerializer(serializers.ModelSerializer):
	cuisine_name = serializers.CharField(source="cuisine.name")

	class Meta:
		model = CuisineMapping
		fields = ('id', 'cuisine', 'cuisine_name', 'rest_id')


class RestaurantLocationSerializer(serializers.ModelSerializer):

	class Meta:
		model = RestaurantLocation
		fields = ('id', 'rest_id', 'country_code', 'city', 'address', 'locality', 'locality_verbose', 'longitude',
				  'latitude')