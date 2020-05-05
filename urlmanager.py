# This File Contains Functions For Building
# Custom Urls For Craigslist Searches:

def urlManager(region, owner):
    if owner == 'owner':
        owner = 'cto'
    elif owner == 'all':
        owner = 'cta'
    elif owner == 'dealer':
        owner = 'ctd'
    else:
        owner = 'cta'
    return 'https://{}.craigslist.org/search/{}?'.format(region, owner)

def postedToday():
  return 'postedToday=1'

def addDistance(search_distance):
    end_url = 'search_distance={}&'.format(search_distance)
    return end_url

def addPostal(postal_code):
    end_url = 'postal={}&'.format(postal_code)
    return end_url

def addMinPrice(min_price):
    end_url = 'min_price={}&'.format(min_price)
    return end_url

def addMaxPrice(max_price):
    end_url = 'max_price={}&'.format(max_price)
    return end_url

def addMakeModel(auto_make_model):
    split_make_model = auto_make_model.split()
    format_by = '+'
    formatted_make_model = format_by.join(split_make_model)
    end_url = 'auto_make_model={}&'.format(formatted_make_model)
    return end_url

def addMinYear(min_auto_year):
    end_url = 'min_auto_year={}&'.format(min_auto_year)
    return end_url

def addMaxYear(max_auto_year):
    end_url = 'max_auto_year={}&'.format(max_auto_year)
    return end_url

def addMinMilage(min_auto_miles):
    end_url = 'min_auto_miles={}&'.format(min_auto_miles)
    return end_url

def addMaxMilage(max_auto_miles):
    end_url = 'max_auto_miles={}&'.format(max_auto_miles)
    return end_url

if __name__ == '__main__':
    base_url = (urlManager('sfbay', 'owner') + 
                            postedToday() +
                            addMinPrice('200') + 
                            addMaxPrice('2000'))
    print(base_url)
    
    