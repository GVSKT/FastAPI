import datetime
from bson.objectid import ObjectId
from dateutil import tz
import pytz
from pytz import timezone as pytzone
import pandas as pd
from datetime import timedelta
from db_config import db_conn

database = db_conn()

class FetchTopRoundTablesAndShows:

    def __init__(self):
        self.rt_collections = database.roundtables
        self.post_collection = database.posts
        self.settings_collections = database.settings

    def get_popular_shows_owner_ids(self):
        show_user = self.settings_collections.find_one({'type': 'POPULAR_SHOWS'})
        data = {}
        if show_user:
            data['user_ids'] = show_user['sub_type']['popular_shows']
            data['limit'] = show_user['sub_type']['rt_limit']
            data['head_count'] = show_user['sub_type']['head_count']
        return data

    def get_popular_rt_owner_ids(self):
        rt_user = self.settings_collections.find_one({'type': 'POPULAR_RT'})
        data = {}
        if rt_user:
            data['user_ids'] = rt_user['sub_type']['popular_rt']
            data['limit'] = rt_user['sub_type']['rt_limit']
            data['head_count'] = rt_user['sub_type']['head_count']

        return data

    # def get_active_rt(self, type, api_type, popular_shows_user_id=[]):
    #
    #     helper = GenericHelper()
    #     today_date = helper.convert_current_date_to_utczonedata()
    #     today_date += datetime.timedelta(minutes=5)
    #
    #     if type == "future":
    #         round_tables = list(self.rt_collections.find({"is_cancelled": 0, "deleted_at.is_deleted": 0,
    #                                                       "open_to_all": "public"} and
    #                                                      {"utc_time.start": {"$lte": today_date}}
    #                                                      and {"media_recording": {"$exists": True, "$ne": []}},
    #                                                      {
    #                                                          "_id": 1,
    #                                                          "user_views_count": 1,
    #                                                          "moderator.user_id": 1,
    #                                                          "owner.user_id": 1,
    #                                                          "utc_time.start": 1,
    #                                                          "utc_time.end": 1,
    #                                                      }).sort("utc_time.start", -1))
    #     else:
    #         if api_type == "popular_shows":
    #             data = self.get_popular_shows_owner_ids()
    #         else:
    #             data = self.get_popular_rt_owner_ids()
    #
    #         if not popular_shows_user_id:
    #             user_ids = data.get('user_ids')
    #         else:
    #             user_ids = [popular_shows_user_id]
    #         cond = {
    #             "$and": [
    #                 {"is_cancelled": 0, "deleted_at.is_deleted": 0},
    #                 {
    #                     "$or": [
    #                         {"owner.user_id": {'$in': user_ids}},
    #                         {"moderator.user_id": {'$in': user_ids}}
    #                     ]
    #                 },
    #                 {"utc_time.start": {"$lte": today_date}},
    #                 {"open_to_all": "public"},
    #                 {"media_recording": {"$exists": True, "$ne": []}},
    #             ]
    #         }
    #         round_tables = list(self.rt_collections.find(cond,
    #                                                      {
    #                                                          "_id": 1,
    #                                                          "user_views_count": 1,
    #                                                          "moderator.user_id": 1,
    #                                                          "owner.user_id": 1,
    #                                                          "utc_time.start": 1,
    #                                                          "utc_time.end": 1,
    #                                                      }).sort("utc_time.start", -1))
    #
    #     rts = {}
    #     for row in round_tables:
    #         user_id = ""
    #         end_time = ""
    #
    #         if row.get('owner') and 'user_id' in row['owner']:
    #             user_id = row['owner']['user_id']
    #
    #         if row.get('utc_time') and 'end' in row['utc_time']:
    #             end_time = row['utc_time']['end']
    #
    #         is_live = False
    #         if end_time and today_date <= end_time:
    #             is_live = True
    #
    #         rts[str(row['_id'])] = {
    #             "_id": row['_id'],
    #             "user_id": user_id,
    #             "join_count": row.get('user_views_count', 0),
    #             "post_count": 0,
    #             "is_live": is_live,
    #         }
    #     return rts

    def get_post_count(self, rts):
        posts = list(self.post_collection.find({"round_table_data.round_table_id": {"$exists": True}},
                                               {"round_table_data.round_table_id": 1}))
        post = {}
        for row in posts:
            rt_id = row['round_table_data']['round_table_id']
            if rt_id not in post:
                post[rt_id] = 0
            post[rt_id] += 1

        for row in post:
            if str(row) in rts:
                rts[str(row)]['post_count'] = post[row]
        return rts

    def sort_by_join_count_and_post_count(self, rts):
        rts_list = []
        for idx in rts:
            rts_list.append(rts[idx])

        out = pd.DataFrame(rts_list)
        return out

    def get_top_round_tables(self, user_ids=None):

        data_type = "current"
        if not user_ids:
            data = self.get_popular_rt_owner_ids()

            if not data.get('user_ids'):
                data_type = "future"

            limit = data.get('limit')
            head_count = data.get('head_count')
        else:
            limit = 5
            head_count = 5

        rts = self.get_active_rt(data_type, "popular_rt", user_ids)
        if rts:
            active_rt = self.get_post_count(rts)
            out = self.sort_by_join_count_and_post_count(active_rt)
            result = out.sort_values(by=['is_live', 'join_count', 'post_count'],
                                     ascending=[False, False, False]).groupby('user_id').head(head_count).values
            ids = list(result[:int(limit)])

            roundtable_ids = []
            for i in ids:
                roundtable_ids.append(i[0])
            return roundtable_ids
        else:
            return []

    def top_shows_by_user(self, df, limit, head_count):

        df['no_of_rt'] = df.groupby('_id')['_id'].transform('count')
        df['total_sum'] = df['join_count'] + df['post_count']
        result = df.groupby('user_id', as_index=False).sum('total_sum').sort_values(
            ['total_sum', 'post_count'], ascending=[False, False]).head(int(head_count))
        ids = list(result['user_id'][:int(limit)])

        return ids

    def top_shows(self, df, limit):

        df['no_of_rt'] = df.groupby('_id')['_id'].transform('count')
        result = df.groupby('user_id', as_index=False). \
            agg({'join_count': 'mean', 'post_count': 'mean', 'no_of_rt': 'count'}).sort_values(
            ['join_count', 'post_count'], ascending=[False, False]).head(10)
        result['participants_per'] = result['no_of_rt'] * 100 / result['join_count']
        result['post_per_person'] = result['participants_per'] * 100 / result['post_count']
        data = result.sort_values('post_per_person', ascending=False)
        ids = list(data['user_id'][:int(limit)])

        return ids

    def get_popular_shows(self):
        data_type = "future"
        limit = 5
        data = self.get_popular_shows_owner_ids()
        if data.get('user_ids'):
            data_type = "current"
            user_ids = data.get('user_ids')

        limit = data.get('limit')
        head_count = data.get('head_count')

        rts = self.get_active_rt(data_type, "popular_shows")
        active_rt = self.get_post_count(rts)
        df = self.sort_by_join_count_and_post_count(active_rt)
        if data_type == "future":
            ids = self.top_shows(df, limit)
        else:
            ids = self.top_shows_by_user(df, limit, head_count)
        user_ids = []
        for i in ids:
            user_ids.append(i)

        return user_ids

