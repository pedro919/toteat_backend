from datetime import datetime, timedelta

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)

def months_betweeen_to_dates(from_date, to_date):
    if from_date.year == to_date.year:
        return to_date.month - from_date.month + 1
    else:
        return 12*(to_date.year - from_date.year) - to_date.month + from_date.month + 1

def analyse_monthly_sales(date, monthly_sales):
    response_json = {'date': f'{date.strftime("%m-%Y")}'}
    zones_count = {}
    zones_income = {}
    payments_count = {}
    payments_income = {}
    categories_count = {}
    categories_income = {}
    products_by_category_count = {}
    products_by_category_income = {}
    total_income = 0
    total_clients = 0
    total_time = 0

    for sale in monthly_sales:
        if sale['zone'] in zones_count:
            zones_count[sale['zone']] += 1
            zones_income[sale['zone']] += sale['total']
        else:
            zones_count[sale['zone']] = 1
            zones_income[sale['zone']] = sale['total']
        
        for payment in sale['payments']:
            if payment['type'] in payments_count:
                payments_count[payment['type']] += 1
                payments_income[payment['type']] += payment['amount']
            else:
                payments_count[payment['type']] = 1
                payments_income[payment['type']] = payment['amount']
        
        for product in sale['products']:
            total_product_income =  int(product['price']) * int(product['quantity'])
            if product['category'] in categories_count:
                categories_count[product['category']] += int(product['quantity'])                
                categories_income[product['category']] += total_product_income
                
                if product['name'] in products_by_category_count[product['category']]:
                    products_by_category_count[product['category']][product['name']] += int(product['quantity'])                    
                    products_by_category_income[product['category']][product['name']] += total_product_income
                else:
                    products_by_category_count[product['category']][product['name']] = int(product['quantity'])
                    products_by_category_income[product['category']][product['name']] = total_product_income

            else:
                categories_count[product['category']] = int(product['quantity'])
                categories_income[product['category']] = int(product['price']) * int(product['quantity'])
                products_by_category_count[product['category']] = {product['name']: int(product['quantity'])}
                products_by_category_income[product['category']] = {product['name']: total_product_income}
        
        total_income += sale['total']
        total_clients += sale['diners']
        total_time += (sale['date_closed'] - sale['date_opened']).total_seconds() / 60
    
    payment_list = []
    for payment_method in payments_count:
        payments_method_dict = {'name': payment_method, 'count': payments_count[payment_method]}
        payment_list.append(payments_method_dict)
        
    response_json['zones_count'] = zones_count
    response_json['zones_income'] = zones_income
    response_json['total_income'] = total_income
    response_json['total_clients'] = total_clients
    response_json['income_per_client'] = total_income/total_clients
    response_json['average_time_in_restaurant'] = total_time / len(monthly_sales)
    response_json['payments_count'] = payment_list
    response_json['payments_income'] = payments_income
    response_json['categories_count'] = categories_count
    response_json['categories_income'] = categories_income
    response_json['products_count'] = products_by_category_count
    response_json['product_income'] = products_by_category_income

    return response_json


def analyze_waiter_sales(sales):
    waiter_sales_count = {}
    waiter_sales_income = {}
    waiter_attended_clientes = {}
    response_json = []
    for sale in sales:
        if sale['waiter'] in waiter_sales_count:
            waiter_sales_count[sale['waiter']] += 1
            waiter_sales_income[sale['waiter']] += sale['total']
            waiter_attended_clientes[sale['waiter']] += sale['diners']
        else:
            waiter_sales_count[sale['waiter']] = 1
            waiter_sales_income[sale['waiter']] = sale['total']
            waiter_attended_clientes[sale['waiter']] = sale['diners']
    
    for person in waiter_sales_count:
        person_dictionary = {}
        person_dictionary['name'] = person
        person_dictionary['total_sales_count'] = waiter_sales_count[person]
        person_dictionary['total_sales_income'] = waiter_sales_income[person]
        person_dictionary['total_earned_tip'] = int(waiter_sales_income[person]) * 0.1
        person_dictionary['total_attended_clients'] = waiter_attended_clientes[person]
        response_json.append(person_dictionary)

    return response_json


def analyze_cashier_sales(sales):
    cashier_sales_count = {}
    cashier_sales_income = {}
    cashier_attended_clientes = {}
    response_json = []
    for sale in sales:
        if sale['cashier'] in cashier_sales_count:
            cashier_sales_count[sale['cashier']] += 1
            cashier_sales_income[sale['cashier']] += sale['total']
            cashier_attended_clientes[sale['cashier']] += sale['diners']
        else:
            cashier_sales_count[sale['cashier']] = 1
            cashier_sales_income[sale['cashier']] = sale['total']
            cashier_attended_clientes[sale['cashier']] = sale['diners']
    
    for person in cashier_sales_count:
        person_dictionary = {}
        person_dictionary['name'] = person
        person_dictionary['total_sales_count'] = cashier_sales_count[person]
        person_dictionary['total_sales_income'] = cashier_sales_income[person]
        person_dictionary['total_attended_clients'] = cashier_attended_clientes[person]
        response_json.append(person_dictionary)

    return response_json