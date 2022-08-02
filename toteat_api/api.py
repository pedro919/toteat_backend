from ninja import NinjaAPI
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .api_functions import months_betweeen_to_dates, analyse_monthly_sales, analyze_waiter_sales, analyze_cashier_sales

api = NinjaAPI()

f = open('toteat_api/data/ventas.json')
data = json.load(f)

for element in data:
    element['date_closed'] = datetime.strptime(element['date_closed'], '%Y-%m-%d %H:%M:%S')
    element['date_opened'] = datetime.strptime(element['date_opened'], '%Y-%m-%d %H:%M:%S')

sorted_data = sorted(data, key=lambda x: x['date_closed'])

@api.get("/hello")
def hello(request):
    return "Hello world"


@api.get("/monthly_sales")
def calculate_monthly_sales(request):
    response = []
    start_date = sorted_data[0]['date_closed'].date()
    end_date = sorted_data[-1]['date_closed'].date()
    number_of_months = months_betweeen_to_dates(start_date, end_date)
    actual_date = start_date.replace(day=1)
    for i in range(number_of_months):
        monthly_sales = list(filter(lambda x: (x['date_closed'].month == actual_date.month) and (x['date_closed'].year == actual_date.year), sorted_data))
        monthly_sales_response = analyse_monthly_sales(actual_date, monthly_sales)
        response.append(monthly_sales_response)
        actual_date = actual_date + relativedelta(months=1)

    return response


@api.get("/total_sales_by_waiter")
def calculate_sales_by_waiter(request):
    response = analyze_waiter_sales(sorted_data)
    return response


@api.get("/monthly_sales_by_waiter")
def calculate_monthly_sales_by_waiter(request):
    response = []
    start_date = sorted_data[0]['date_closed'].date()
    end_date = sorted_data[-1]['date_closed'].date()
    number_of_months = months_betweeen_to_dates(start_date, end_date)
    actual_date = start_date.replace(day=1)
    for i in range(number_of_months):
        monthly_sales = list(filter(lambda x: (x['date_closed'].month == actual_date.month) and (x['date_closed'].year == actual_date.year), sorted_data))
        monthly_sales_response = analyze_waiter_sales(monthly_sales)
        response.append({'date': f'{actual_date.strftime("%m-%Y")}', 'waiters_sales': monthly_sales_response})

    return response


@api.get("/total_sales_by_cashier")
def calculate_sales_by_cashier(request):
    response = analyze_cashier_sales(sorted_data)
    return response


@api.get("/monthly_sales_by_cashier")
def calculate_monthly_sales_by_cashier(request):
    response = []
    start_date = sorted_data[0]['date_closed'].date()
    end_date = sorted_data[-1]['date_closed'].date()
    number_of_months = months_betweeen_to_dates(start_date, end_date)
    actual_date = start_date.replace(day=1)
    for i in range(number_of_months):
        monthly_sales = list(filter(lambda x: (x['date_closed'].month == actual_date.month) and (x['date_closed'].year == actual_date.year), sorted_data))
        monthly_sales_response = analyze_cashier_sales(monthly_sales)
        response.append({'date': f'{actual_date.strftime("%m-%Y")}', 'cashiers_sales': monthly_sales_response})

    return response