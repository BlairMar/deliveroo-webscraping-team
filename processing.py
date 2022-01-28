
import pandas as pd
from uploads import Upload

def process(data):
    df = pd.DataFrame.from_dict(data)
    # df.columns = ['tags', 'name', 'image_path', 'uuid', 'url', 'rating']
    
    #pd.options.mode.chained_assignment = None
    def list_to_string(my_list):
        if not my_list:
            return None
        else:
            return my_list[0]
    def list_of_items_by_word(*args):

        lis = [list_to_string([strings for strings in tags for arg in args if
                            arg in strings]) for tags in df['tags']]
        remove_from_tags_by_list(lis)
        return lis


    def remove_from_tags_by_list(list_1):
        [tags.remove(val) for val in list_1 for tags in df['tags'] if val in tags]


    def remove_from_tags_by_string(string_1, string_2='ignore', string_3='ignore', string_4='ignore'):
        [tags.remove(val) for tags in df['tags']
        for val in tags if string_1 in val or string_2 in val or string_3 in val or string_4 in val]


    def string_replacer(column, original, replacement=''):
        df[column] = df[column].str.replace(original, replacement)

    # Problem! Rating column not added for all addresses
    

    if 'rating' in df:    
        rating = list_of_items_by_word('Excellent', 'Very good', 'Good')
        remove_from_tags_by_string('(', ')')
        missing_rating = pd.isnull(df["rating"])
        df["rating"][missing_rating] = rating


        string_replacer('rating', 'Excellent')
        string_replacer('rating', 'Very good')
        string_replacer('rating', 'Good')

    min_spend = list_of_items_by_word('minimum')
    df['minimum_spend'] = min_spend
    string_replacer('minimum_spend', '£')
    string_replacer('minimum_spend', 'minimum')
    string_replacer('minimum_spend', 'No', '0')


    closing = list_of_items_by_word('Closes at', 'Open until')
    df['closing_time'] = closing
    string_replacer('closing_time', 'Closes at', ' ')
    string_replacer('closing_time', 'Open until', ' ')

    opening = list_of_items_by_word('Opens at')
    df['opening_time'] = opening

    distance = list_of_items_by_word("miles away", 'mile away')
    df['distance'] = distance
    string_replacer('distance', 'miles away')
    string_replacer('distance', 'mile away')

    delivery_charge = list_of_items_by_word('delivery')
    df['delivery_charge'] = delivery_charge
    df['delivery_charge'] = df['delivery_charge'].str.replace('£', '')
    df['delivery_charge'] = df['delivery_charge'].str.replace('delivery', '')
    df['delivery_charge'] = df['delivery_charge'].str.replace('Free', '0')

    # rawtagslist = []

    # for lis in df['tags']:
    #     for string in lis:
    #         if string in rawtagslist:
    #             pass
    #         elif 'Info' in string or 'View map' in string or 'Delivered by' in string or 'order' in string or 'Editions' in string:
    #             pass
    #         elif ' ' in string:
    #             if any(chr.isdigit() for chr in string) == True and 'min' not in string:
    #                 pass
    #             else:
    #                 rawtagslist.append(string)
    #         else:
    #             rawtagslist.append(string)

    # for tags in df['tags']:
    #     for string in tags:
    #         if string in rawtagslist:
    #             pass
    #         else:
    #             tags.remove(string)

    remove_from_tags_by_string('View map', 'Editions', 'Delivered by', 'updates')

    delivery_time = list_of_items_by_word('-', 'min')
    df['delivery_time'] = delivery_time
    string_replacer('delivery_time', 'min')
    
    return df

def upload_images(df, directory):
    upload = Upload()
    df['image_s3_key'] = df.apply(lambda entry: upload.upload_file(entry['image_path'], directory=directory))