from .models import *
from restaurantback.utility import *
import csv
from .serializers import *
from django.core.paginator import Paginator
from django.db.models import Q


class RestaurantController():

    def save_restaurant_list_data(self, request):
        """
        function to save the list of data present in the csv sheet
        1. checking the data is already present or not
        2. opening the csv and making the dict for cuisine_list, currency and rating
        3. after making the three list calling a function to save all the three data
        4. if success then saving the data of restaurant detaoils and location data
        :param request: request data
        :return: success and error message
        """
        try:
            msg = 'Data set already present'
            data_count = RestaurantDetails.objects.filter().count()
            if data_count == 0:
                rest_headers, rest_loc_dict = self.get_rest_location_key_value_list()
                if rest_headers and rest_loc_dict:
                    with open('homepage/csv_files/restaurants.csv') as f:
                        reader = csv.reader(f)
                        detail_headers = next(reader)
                        cuisine_index = detail_headers.index('Cuisines')
                        currency_index = detail_headers.index('Currency')
                        rating_color_index = detail_headers.index('Rating color')
                        detail_dict = {
                            'cuisine_list': [],
                            'currency': {},
                            'rating': {}
                        }
                        restaurant_data = []
                        for read in reader:
                            restaurant_data.append(read)
                            detail_dict['cuisine_list'].extend([n for n in read[cuisine_index].split(', ')
                                                                if n not in detail_dict['cuisine_list'] and n])
                            temp_currency = read[currency_index].split('(')
                            detail_dict['currency'][temp_currency[0]] = temp_currency[1][:-1]

                            detail_dict['rating'][read[rating_color_index]] = read[rating_color_index+1]
                    success = self.save_rest_cuisine_currency_rating_data(detail_dict)
                    if success:
                        self.save_restaurant_details(restaurant_data, rest_loc_dict)
                return {'status': 'success'}
        except Exception as e:
            exception_detail(e)



    def get_rest_location_key_value_list(self):
        """
        function to get the key value list pf location for each and every restaurant id
        1. opening the csv and reading the data and making a dict where jey as restaurant ida and value
            as the whole data
        :return:
        """
        temp_dict = {}
        headers = []
        try:
            with open('homepage/csv_files/restaurant_add.csv') as f:
                reader = csv.reader(f)
                headers = next(reader)
                for data in reader:
                    temp_dict[data[0]] = data
        except Exception as e:
            exception_detail(e)
        return headers, temp_dict

    def save_rest_cuisine_currency_rating_data(self, detail_dict):
        """
        function to save all the three cuisine_list, currency and rating
        1. calling all the three function to save all the data
        :param detail_dict:
        :return:
        """
        try:
            self.save_cuisine_data(detail_dict['cuisine_list'])
            self.save_currency_data(detail_dict['currency'])
            self.save_rating_data(detail_dict['rating'])
            return True
        except Exception as e:
            exception_detail(e)
            return False

    def save_cuisine_data(self, cuisine_list):
        """
        function to save cuisines data
        1. making the objects of cuisines and making a lisy of data
        2.  using bulk_create saving into the database
        :param cuisine_list:
        :return:
        """
        try:
            create_list = []
            for data in cuisine_list:
                obj = Cuisine()
                obj.name = data
                create_list.append(obj)
            if create_list:
                Cuisine.objects.bulk_create(create_list)
        except Exception as e:
            exception_detail(e)


    def save_currency_data(self, currency):
        """
        function to save currency data
        1. making the objects of currency and making a lisy of data
        2.  using bulk_create saving into the database
        :param cuisine_list:
        :return:
        """
        try:
            create_list = []
            for name, symbol in currency.items():
                obj = Currency()
                obj.name = name
                obj.symbol = symbol
                create_list.append(obj)
            if create_list:
                Currency.objects.bulk_create(create_list)
        except Exception as e:
            exception_detail(e)


    def save_rating_data(self, rating):
        """
        function to save rating data
        1. making the objects of rating and making a list of data
        2.  using bulk_create saving into the database
        :param cuisine_list:
        :return:
        """
        try:
            create_list = []
            for color,text in rating.items():
                obj = Rating()
                obj.text = text
                obj.color = color
                create_list.append(obj)
            if create_list:
                Rating.objects.bulk_create(create_list)
        except Exception as e:
            exception_detail(e)


    def save_restaurant_details(self, restaurant_data, rest_loc_dict):
        """
        function to save the restaurant details
        1. getting the cuisines data and making key valkue pair of it
        2. getting the currency data and making key valkue pair of it
        3. getting the rating data and making key valkue pair of it
        4. iterating over each nd every restaurant data and saving into the Database
        5. savig the mapping and restaurant location to database
        :param restaurant_data:
        :param rest_loc_dict:
        :return:
        """
        try:
            cusines_obj = Cuisine.objects.filter()
            cusines_serializer = CuisineListSerializer(cusines_obj, many=True)
            cusines_dict = get_key_value_pair(cusines_serializer.data, key='name')

            currency_obj = Currency.objects.filter()
            currency_serializer = CurrencyListSerializer(currency_obj, many=True)
            currency_dict = get_key_value_pair(currency_serializer.data, key='name')

            rating_obj = Rating.objects.filter()
            rating_serializer = RatingListSerializer(rating_obj, many=True)
            rating_dict = get_key_value_pair(rating_serializer.data, key='color')

            cusines_create_list = []
            location_create_list = []

            for data in restaurant_data:
                obj = RestaurantDetails()
                obj.rest_id = data[0]
                obj.rest_name = data[1]
                obj.avg_cost = data[3]
                obj.currency_id = currency_dict.get(data[4].split('(')[0]).get('id')
                if data[5].lower() == 'yes':
                    obj.has_tbl = True
                elif data[5].lower() == 'no':
                    obj.has_tbl = False
                if data[6].lower() == 'yes':
                    obj.has_online = True
                elif data[6].lower() == 'no':
                    obj.has_online = False
                obj.agreegate = data[7]
                obj.rating_id = rating_dict.get(data[8]).get('id')
                obj.votes = data[10]
                obj.save()
                rest_id = obj.id
                cusines_create_list.extend(self.save_cuisine_mapping_data(rest_id, cusines_dict, data[2]))
                location_create_list.extend(self.save_restaurant_location_detail(rest_id, rest_loc_dict, data[0]))
            if cusines_create_list:
                CuisineMapping.objects.bulk_create(cusines_create_list)
            if location_create_list:
                RestaurantLocation.objects.bulk_create(location_create_list)
        except Exception as e:
            exception_detail(e)



    def save_cuisine_mapping_data(self, rest_id, cusines_dict, cuisines):
        """
        function to save cusines data into DB
        1. making a list and sending each and every object to the calling part
        :param rest_id:
        :param cusines_dict:
        :param cuisines:
        :return:
        """
        create_list = []
        try:
            if cuisines:
                for data in cuisines.split(', '):
                    obj = CuisineMapping()
                    obj.rest_id = rest_id
                    obj.cuisine_id = cusines_dict.get(data, {}).get('id', None)
                    create_list.append(obj)
        except Exception as e:
            exception_detail(e)
        return create_list

    def save_restaurant_location_detail(self, rest_id_save, rest_loc_dict, rest_id):
        """
        function to save the restaurant location detail to DB
        1. making object opf restaurant location and returning to calling part
        :param rest_id_save:
        :param rest_loc_dict:
        :param rest_id:
        :return:
        """
        try:
            loc_data = rest_loc_dict.get(rest_id)
            obj = RestaurantLocation()
            obj.rest_id = rest_id_save
            obj.country_code = loc_data[1]
            obj.city = loc_data[2]
            obj.address = loc_data[3]
            obj.locality = loc_data[4]
            obj.locality_verbose = loc_data[5]
            obj.longitude = loc_data[6]
            obj.latitude = loc_data[7]
            return [obj]
        except Exception as e:
            exception_detail(e)


    def get_restaurant_list_data(self, request):
        """
        function to get the list of data need for presentation
        1. getting the post data and checking that there is page, search_str and per page
        2. if search str making a Q filter too filter the data from the DB
        3. making a paginator object
        4. querying the cusinemapping and making the key value pair of it and after setting it into the
            restaurant detail , sending to frontend
        :param request:
        :return:
        """
        try:
            post_data = request.data
            per_page = post_data.get('per_page', 12)
            page_no = post_data.get('page_no', 1)
            sort_val = post_data.get('sort')
            search_filter = Q()
            search_str = post_data.get('search_str')
            if search_str:
                cuisines_rest_id_list = CuisineMapping.objects.filter(cuisine__name__icontains=search_str). \
                    values_list('rest_id', flat=True)
                cuisines_rest_id_list = list(set(cuisines_rest_id_list))
                search_filter = Q(rest_name__icontains = search_str) | Q(id__in=cuisines_rest_id_list)
            sort_by = self.get_sort_value(sort_val)
            obj = RestaurantDetails.objects.filter(search_filter).order_by(sort_by)

            pagi = Paginator(obj, per_page)
            page_obj = pagi.page(page_no)
            rest_obj = page_obj.object_list

            serializer = RestaurantListSerializer(rest_obj, many=True)
            rest_data = serializer.data
            rest_ids = get_id_list_from_db_obj(rest_obj, key='id')

            cuisines_map_obj = CuisineMapping.objects.filter(rest__id__in=rest_ids)
            cuisines_map_serializer = CuisineMappingSerializer(cuisines_map_obj, many=True)
            cuisines_map_dict = {}
            for map_data in cuisines_map_serializer.data:
                if not cuisines_map_dict.get(map_data.get('rest_id')):
                    cuisines_map_dict[map_data.get('rest_id')] = []
                cuisines_map_dict[map_data.get('rest_id')].append(map_data.get('cuisine_name'))
            for val in rest_data:
                val['cuisines'] = ', '.join(cuisines_map_dict.get(val.get('id'), []))
            data = {
                'page': page_no,
                'count': pagi.count,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'start_index': page_obj.start_index(),
                'end_index': page_obj.end_index(),
                'last_page': pagi.num_pages,
                'result': rest_data
            }
            return {'status': 'success', 'data': data}
        except Exception as e:
            exception_detail(e)


    def get_restaurant_location_data(self, request):
        """
        function to get restaurant location details
        1. queryong the table and getting the data
        2. serializing it and sending to frontend
        :param request:
        :return:
        """
        try:
            rest_id = request.GET.get('rest_id')
            if rest_id:
                loc_obj = RestaurantLocation.objects.get(rest_id=rest_id)
                serializer = RestaurantLocationSerializer(loc_obj)
                data = serializer.data
                return {'status': 'success', 'data': data}
        except Exception as e:
            exception_detail(e)
            return {'status': 'error'}


    def get_sort_value(self, value):
        """
        function to get the sort name for sorting the data
        1. checking that value is there or not
        2. changing the value of sort on basis of that
        :param value:
        :return: sort key
        """
        try:
            if value not in ["", " ", None, 'undefined', 'null']:
                value_arr = value.split(" ")
                if len(value_arr) > 1 and value_arr[0].lower() == 'not':
                    return '-'+value_arr[1]
                else:
                    return value_arr[0]
        except Exception as e:
            exception_detail(e)
        return 'id'