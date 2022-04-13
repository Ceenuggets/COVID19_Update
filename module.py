import datetime


def sort_names(new_cases):
    sorted_names = [{'label': i, 'value': i} for i in new_cases['Country_Other'].sort_values(ascending=True).unique()]
    return sorted_names


def get_cases(new_cases, chosen_name):

    country = new_cases[new_cases['Country_Other'] == chosen_name]
    country_total_per_day = []
    for date in get_dates(new_cases):
        total = country[date].str.replace('+', '', regex=False).str.replace(',', '', regex=False).fillna(0).astype(int)
        country_total_per_day.append(int(total))

    return country_total_per_day


def get_dates(new_cases):
    dates = new_cases.columns.to_list()
    dates = dates[1:]

    return dates


def format_date(list_date):
    x_date_format = [datetime.datetime.strptime(x[:-7], "%b").strftime('%b') + '-' + x[-7:-5] + '-' + x[
       -4:] if '_' in x else datetime.datetime.strptime(x[:-2], "%B").strftime('%b') + '-' + x[-2:] + '-' + '2020'
                     for x in list_date]
    return x_date_format

