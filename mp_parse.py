# Note: Assumes data.csv is sorted by user_id, date
import csv
import sys

SORTED_IN_FILE = sys.argv[1]

TIME_COL = 0; RUN_COL = 1; USERID_COL = 2; USERIP_COL = 3; REVENUE_COL = 4; SHOW_COL = 5
SYD_MELB_COL = 10


data = open(SORTED_IN_FILE).readlines()
data.pop(0).rstrip() #get rid of header
print "stream_start, stream_end, run_id, user_id, show, episode, ad_secs_sum, last_event"

for index, row in enumerate(data):
        if index == len(data) - 2: break

        n = index
        n1 = n + 1
        n2 = n + 2

        n_row = row.split(',')
        n1_row = data[n1].split(',')
        n2_row = data[n2].split(',')


        n_userid = n_row[USERID_COL]
        n1_userid = n1_row[USERID_COL]
        n2_userid = n2_row[USERID_COL]

        n_show = n_row[SHOW_COL].replace("\n", "")
        n1_show = n1_row[SHOW_COL].replace("\n", "")
        n2_show = n2_row[SHOW_COL].replace("\n", "")


        if n_userid == '': continue

        if '/show/' in n_show:
            # Streams start with /show/ and have either 1st next line or 2nd next line containing ad_duration or content_start
            if (n_userid == n1_userid and ('ad_duration' in n1_show or 'content_start' in n1_show)) \
            or (n_userid == n2_userid and ('ad_duration' in n2_show or 'content_start' in n2_show) and 'http' not in n1_show):
                stream_start = n_row[TIME_COL]
                run_id = n_row[RUN_COL]
                user_id = n_row[USERID_COL]
                fragments = n_show.split('/')
                show = fragments[4]
                episode = 'Movie' if len(fragments) <= 6 else fragments[5] + '-' + fragments[6]

                remaining_rows = data[n:]

                ad_secs_sum = 0
                last_event = ""
                stream_end = ""

                for i, row in enumerate(remaining_rows):
                    row = row.split(',')
                    if row[USERID_COL] != user_id: break # won't be same stream if user changes
                    ad_secs_sum = ad_secs_sum + int(row[REVENUE_COL])
                    last_event = row[SHOW_COL].rstrip()
                    stream_end = row[TIME_COL]
                    if i == len(remaining_rows) - 2 : break # make sure we don't fall off the end
                    if 'http' in remaining_rows[i+1]: break # streams stop the line preceeding the next http url

                if int(ad_secs_sum) > 0:
                    print '{},{},{},{},{},{},{},{}'.format(stream_start, stream_end, run_id, user_id, show, episode, ad_secs_sum, last_event)
