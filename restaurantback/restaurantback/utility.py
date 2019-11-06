import traceback


def get_key_value_pair(data, key='id'):
	temp_dict = {}
	try:
		for val in data:
			temp_dict[val.get(key)] = val
	except Exception as e:
		exception_detail(e)
	return temp_dict


def get_id_list_from_db_obj(list_data, key='id'):
	temp_list = []
	try:
		for data in list_data:
			temp_list.append(getattr(data, key))
	except Exception as e:
		exception_detail(e)
	return temp_list

def exception_detail(e):
	try:
		print(e)
		print('exception -> ', traceback.format_exc())
	except Exception as e:
		print(e.args)


