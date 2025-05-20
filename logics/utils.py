import datetime
import re
from typing import List
import locale


def convert_to_int(num_str):
    try:
        # Remove spaces and attempt to convert to an integer
        cleaned_num_str = num_str.replace(" ", "")
        return int(cleaned_num_str)
    except (ValueError, TypeError):
        # Return 0 if conversion fails due to non-numeric value or invalid input
        return 0


def phone_number_input_update(phone_number: str):
    # Remove parentheses, spaces, and other non-numeric characters
    cleaned_number = re.sub(r'\D', '', phone_number)
    # Add the country code prefix
    return '+998' + cleaned_number


def format_price_as_str(price: int):
    # Format the number with comma separators and replace commas with spaces
    return "{:,}".format(price).replace(',', ' ')


def format_datetime_uz(dt: datetime.datetime):
    if dt:
        locale.setlocale(locale.LC_TIME, 'uz_UZ.UTF-8')
        return dt.strftime('%Y-yil %-d-%b %H:%M')
    return ""


def get_formated_phone_number(phone_number: str):
    if phone_number.startswith("+998") and len(phone_number) == 13:
        return f"{phone_number[:4]} ({phone_number[4:6]}) {phone_number[6:9]} {phone_number[9:11]} {phone_number[11:]}"
    else:
        return phone_number if phone_number else "-"
