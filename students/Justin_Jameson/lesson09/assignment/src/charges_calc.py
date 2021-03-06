# -------------------------------------------------#
# # Title: charges calculator for Inventory management.
# # Dev:   unknown
# # Date:  4/17/2019
# # ChangeLog: (Who, What)
# Justin Jameson
# correct ouput to output line 20 'ouptu JSON file'
# in source.json removed extra comma on line 5884 from
# 'units_rented': 7,,
# imported logger
# 20190602 updating file to use decorators to induce logging.
# #-------------------------------------------------#

""" Returns total price paid for individual rentals """

import argparse
import json
import datetime
import math
import logging
import functools

logging.basicConfig(filename='charges_calc_updated.log', level=logging.DEBUG)
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler('charges_calc.log')
file_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(file_handler)
do_debug = input('Debug? Y/N: ')


def debug(func):
    """Print the function signature and return value"""
    if do_debug.lower() == 'y':
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            logging.debug(f"Calling {func.__name__}({signature})")
            value = func(*args, **kwargs)
            logging.info(f"{func.__name__!r} returned {value!r}")
            return value
        return wrapper_debug
    else:
        @functools.wraps(func)
        def debug_disabled(*args, **kwargs):
            # print("Debug has been disabled")
            returned_value = func(*args, **kwargs)
            return returned_value
        return debug_disabled


@debug
def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    return parser.parse_args()


@debug
def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            logging.warning('load_rentals_files threw an exception')
            exit(0)
    return data


@debug
def calculate_additional_fields(data):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            logging.warning('except block of calculate_add... this will exit the program without')
            exit(0)
    return data


@debug
def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
