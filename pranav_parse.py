# Note: Assumes data.csv is sorted by user_id, date
import csv
import sys

SORTED_IN_FILE = sys.argv[1]


last_current_show = None
last_event = None
start_time = None
end_time = None
user_id = None
variation_id = None
revenue_sum = 0


TIME_COL = 0
VARIATION_COL = 1
USER_ID_COL = 2
REVENUE_COL = 4
CURRENT_SHOW_COL = 5

with open(SORTED_IN_FILE, 'rb') as csvfile:
    csvfile.readline()
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        data_current_show = row[CURRENT_SHOW_COL]
        current_user_id = row[USER_ID_COL]
        if data_current_show.startswith('http://') and '/show/' in data_current_show:
            if (last_current_show != data_current_show) or (current_user_id != user_id):
                if last_current_show and last_current_show.endswith('#autoplay'):
                    # print details
                    fragments = last_current_show.split('/')
                    show = fragments[4]
                    episode = 'Movie' if len(fragments) <= 6 else fragments[5] + '-' + fragments[6]
                    if int(revenue_sum) > 0: # add this to take out zero duration streams
                        print '{},{},{},{},{},{},{},{}'.format(start_time, end_time, variation_id, user_id, show, episode, revenue_sum, last_event)

            # reset current show
            last_current_show = data_current_show
            user_id = row[USER_ID_COL]
            variation_id = row[VARIATION_COL]
            start_time = row[TIME_COL]
            revenue_sum = 0
        last_event = row[CURRENT_SHOW_COL]
        end_time = row[TIME_COL]
        revenue_sum += float(row[REVENUE_COL]) if row[REVENUE_COL].isdigit() else 0
