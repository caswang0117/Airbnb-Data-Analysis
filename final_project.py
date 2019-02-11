"""
Cassie Wang
CSCI51P
05/02/2018
This program contains 6 different functions with which to sort through Tom SLee Airbnb Data. Functions create list
relating price to overall satisfaction; create dictionary that sorts room_ids to appropriate host_id; take a list
of file names and sort them oldest to newest, then sort prices of listings to appropriate room_id in chronological
order; find Spearman's rank correlation between price and listing rating; creates list with number of hosts with the
corresponding amount of listings as index; and finds listing with greatest change in price.

"""
from scipy.stats.stats import spearmanr


def price_satisfaction(filename):
    """
    Takes a string containing the name of a file and creates a list of lists (of type float) where each sublist
    contains exactly two items: the price and the overall_satisfaction
    Args:
        filename(str): name of file
    Returns:
        big_list(list): list of lists (of float) containing two items: the price and the overall satisfaction
    """
    file_in = open(filename, "r")
    file_in.readline()  # Reads header
    data = file_in.readlines()

    big_list = []
    # Reads each line of file and appends list of price and overall_satisfaction to big_list
    for line in data:
        split_line = line.split(",")
        if len(split_line) == 19:  # Checks data has all columns and no /n at end of file
            if split_line[8] != "" and int(split_line[8]) > 0:  # Only using data with at least one review
                corr = [] # Creates sublist for price and overall_satisfaction
                if split_line[9] != "" and split_line[13] != "":  # Checks if data is missing price or satisfaction
                    corr.append(float(split_line[13]))  # Appends price of listing
                    corr.append(float(split_line[9]))  # Appends overall_satisfaction of corresponding listing
                    big_list.append(corr)
    return big_list


def host_listings(filename):
    """
    Takes a string containing the name of a file. Creates and returns a dictionary where the keys are host_ids(int) and
    the values are a list of room_ids(int) associated with that host.
    Args:
        filename(str): name of file
    Returns:
        big_dict(dict): keys are host_ids(int) and values are a list of room_ids(int) associated with that host
    """
    file_in = open(filename, "r")
    file_in.readline()  # Reads header
    data = file_in.readlines()

    big_dict = {}
    for line in data:
        split_line = line.split(",")
        if len(split_line) == 19:  # Checks data has all columns and no /n at end of file
            if split_line[2] != "" and split_line[0] != "":  # Checks data is not missing host_ids or room_ids
                host_id = int(split_line[2])
                room_id = int(split_line[0])

                # Sorts all room_ids to corresponding host_id
                if host_id in big_dict:
                    big_dict[host_id].append(room_id)  # If host_id already key, appends room_id
                # If host_id not already key, creates empty list for value and appends room_ids to value
                else:
                    big_dict[host_id] = []  # Value of key is supposed to be a list of room_ids
                    big_dict[host_id].append(room_id)
    return big_dict


def room_prices(filename_list, roomtype):
    """
    Takes a list of filenames (str) and the room type to search for (str) and returns a dictionary where the keys are
    room_ids (int) and the values are a list of the prices (float) for that listing over time, from the oldest
    data to the most recent.
    Args:
        filename_list(list): list of filenames(str)
        roomtype(str): type of room of listing. Either "Entire home/apt", "Private room", or "Shared room"
    Returns:
        price_dict(dict): keys are room_ids (int) and values are a list of the prices (float) for that listing over time,
        from oldest data to most recent
    """
    date_dict = {}
    chronological_filenames = []

    # Use date in file name to sort files from oldest to newest
    for filename in filename_list:
        # Reads date in reverse and flips back to normal
        reverse_date = filename[-5:-15:-1]
        date = reverse_date[::-1]

        year = date[:4]
        month = date[5:7]
        day = date[8:10]

        # Creates number composed of date features to sort in ascending order
        comb_date = year+month+day

        # Sorts file names by date in dictionary
        if comb_date in date_dict:
            date_dict[comb_date].append(filename)
        else:
            date_dict[comb_date] = []
            date_dict[comb_date].append(filename)

    chronological_dates = sorted(date_dict)  # Sorts keys of date_dict (dates) from oldest to newest

    # Creates list of file names sorted chronologically
    for elem in chronological_dates:
        chronological_filenames += date_dict[elem]  # Adds values from date_dict (file names) based on sorted dates

    price_dict = {}
    for filename in chronological_filenames:
        file_in = open(filename, "r")
        file_in.readline()  # Reads header
        data = file_in.readlines()

        for line in data:
            split_line = line.split(",")
            if len(split_line) == 19:  # Checks data has all columns and no /n at end of file
                if split_line[3] and split_line[0] and split_line[13] != "": # Checks room_id, price, roomtype exist
                    if split_line[3] == roomtype:  # Only takes data for specified roomtype
                        room_id = int(split_line[0])
                        price = float(split_line[13])

                        # Adds price of listing to corresponding room_id from oldest to new
                        if room_id in price_dict:
                            price_dict[room_id].append(price)
                        else:
                            price_dict[room_id] = []
                            price_dict[room_id].append(price)
    return price_dict


def correlation(l):
    """
    Takes a list that is the output of function price_satisfaction and returns the correlation between the price and
    rating, using a Spearman's rank correlation. A correlation of 0 means no relationship, a positive result means the
    variables are directly related, and a negative result means the variables are inversely related.
    Args:
        l(list): the output of price_satisfaction that is a list containing two items: the price and the overall
        satisfaction
    Returns:
        listing_counts(list): the correlation and p-value for the Spearman's rank correlation for the correlation
        between the price and rating for listings
    """
    price = []
    rating = []

    # Create two lists – one with all prices of listing and one with all ratings
    for pair in l:
        price.append(pair[0])  # Index into price
        rating.append(pair[1])  # Index into rating
    return spearmanr(price,rating)


def num_listings(dict):
    """
    Takes as input a dictionary that is in the format of the dictionary returned by function host_listings. Returns a
    list l where l[i] is the number of hosts that have exactly i listings.
    Args:
         dict(dict): dictionary returned by host_listings, where keys are host_ids (int) and values are a list of
         room_ids (int) associated with that host
    Returns:
        listing_counts(list): list where l[i] is the number of hosts that have exactly i listings
    """
    listing_counts = []
    listing_dict = {}

    # Creates dict counting number of listings per host
    for key in dict:
        count = len(dict[key])  # Number of listings specified by number of room_ids per host_id in dict
        if count in listing_dict:
            listing_dict[count] += 1  # If already multiple hosts with that number of listings, increases count
        else:
            listing_dict[count] = 1  # Sets count to one if first host with that many listings

    # Sorts keys of listing_dict (specifying number of listings) in ascending order
    sorted_listings = sorted(listing_dict)

    # Creates list where number of listings corresponds to index, 0 included if no hosts with that number of listings
    for i in range(0, sorted_listings[-1]+1): # Needs to include highest number of listings
        # For numbers of listings that no one has, sets count to 0
        if i not in listing_dict:
            listing_counts.append(0)
        else:
            listing_counts.append(listing_dict[i])
    return listing_counts


def price_change(dict):
    """
    Takes as input a dictionary in the format returned from the function room_prices and returns a tuple with three
    elements with the maximum percent change for the set of properties in the dictionary, the starting price for that
    property, and the ending price for that property (in that order).
    Args:
        dict(dict): dictionary returned by room_prices where the keys are room_ids (int) and the values are a list of
        the prices (float) for that listing over time, from oldest data to most recent
    Returns:
        (tuple): a tuple with three elements in the following order: the maximum percent change for the set of
        properties in the dictionary, the starting price for that property, and the ending price for that property.
    """
    tuple_list = []

    # Creates list of tuples
    for key in dict:
        start_price = dict[key][0]  # Oldest listing price
        end_price = dict[key][-1]  # Most recent listing price
        change = ((end_price - start_price) / start_price)*100 # To find percentage of price change
        price_tuple = (change, start_price, end_price)
        tuple_list.append(price_tuple)

    # Sorts through all tuples for the one with greatest price_change
    max_change = 0  # Sets original price_change to 0
    for item in tuple_list:
        # If price_change is greatest observed yet, sets max_tuple equal to that tuple
        if item[0] > max_change:
            max_change = item[0]
            max_tuple = tuple_list.index(item)  # Return tuple with greatest change in price
    return tuple_list[max_tuple]  # Returns entire tuple at the correct index


if __name__ == "__main__":
    main()