from django.db import models


class Currency(models.Model):
	name = models.CharField(max_length=255)
	symbol = models.CharField(max_length=10)

	class Meta:
		db_table = 'currency'


class Rating(models.Model):
	text = models.CharField(max_length=20)
	color = models.CharField(max_length=30)

	class Meta:
		db_table = 'rating'


class Cuisine(models.Model):
	name = models.TextField(max_length=100)

	class Meta:
		db_table = 'cuisines'


class RestaurantDetails(models.Model):
	rest_id = models.BigIntegerField()
	rest_name = models.CharField(max_length=300)
	avg_cost = models.IntegerField(default=0)
	currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
	has_tbl = models.BooleanField(blank=True, null=True)
	has_online = models.BooleanField(blank=True, null=True)
	agreegate = models.FloatField()
	rating = models.ForeignKey(Rating, on_delete=models.DO_NOTHING)
	votes = models.BigIntegerField(default=0)

	class Meta:
		db_table = 'rest_detail'


class CuisineMapping(models.Model):
	cuisine = models.ForeignKey(Cuisine, on_delete=models.DO_NOTHING)
	rest = models.ForeignKey(RestaurantDetails, on_delete=models.DO_NOTHING)

	class Meta:
		db_table = 'cuisine_mapping'


class RestaurantLocation(models.Model):
	rest = models.ForeignKey(RestaurantDetails, on_delete=models.DO_NOTHING)
	country_code = models.SmallIntegerField()
	city = models.CharField(max_length=255)
	address = models.TextField()
	locality = models.CharField(max_length=255)
	locality_verbose = models.CharField(max_length=255)
	longitude = models.CharField(max_length=20)
	latitude = models.CharField(max_length=20)

	class Meta:
		db_table = 'rest_location'