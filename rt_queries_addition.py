from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from db_config import pymongo_db


class Roundtable_Query:

    def get_participant_list_rt(self, rt_id):
        """This method is for getting participant list of RT"""

        query = [
            {'$match': {'roundtable_id': ObjectId(rt_id)}},
            {"$match": {"action": {"$in": ['JOIN', 'VIEW']}}},
            {"$lookup": {
                'from': 'users',
                'localField': 'user_id',
                'foreignField': '_id',
                'as': 'user_data',
            }},

            {'$unwind': {'path': '$user_data',
                         'preserveNullAndEmptyArrays': True}},
            {'$group': {
                '_id': '$user_data._id',
                'name': {'$first': '$user_data.name'},
                'username': {'$first': '$user_data.username'},
                'designation': {'$first': '$designation'}

            }}
        ]

        mydb, mycol = pymongo_db()
        res = mycol.aggregate(query)
        # res = RTAnalytics.objects.mongo_aggregate(query)
        res = list(res)
        res = loads(dumps(res, indent=2))
        return res

    #
    # def getPublicRtListV1(self, user_id, paginate=""):
    #     helper = GenericHelper()
    #     # today_date = helper.convert_current_date_to_utczonedata()
    #     # today_date_end = helper.convert_current_date_to_utczonedata()
    #
    #     utcval = None
    #     time_zone_type = None
    #     utc_date = None
    #
    #     if utcval is None:
    #         utcval = 'UTC'
    #
    #     if time_zone_type is None:
    #         time_zone_type = 'Asia/Kolkata'
    #
    #     from_zone = tz.gettz(utcval)
    #     to_zone = tz.gettz(time_zone_type)
    #     if utc_date is None:
    #         utc = datetime.utcnow()
    #     else:
    #         if isinstance(utc_date, str):
    #             utc = datetime.strptime(utc_date, '%Y-%m-%d %H:%M:%S')
    #         else:
    #             utc = datetime.strftime(utc_date, '%Y-%m-%d %H:%M:%S')
    #             utc = datetime.strptime(utc_date, '%Y-%m-%d %H:%M:%S')
    #
    #     utc = utc.replace(tzinfo=from_zone)
    #     central = utc.astimezone(to_zone)
    #     central = datetime.strftime(central, "%Y-%m-%d %H:%M:%S")
    #     central = datetime.strptime(central, "%Y-%m-%d %H:%M:%S")
    #
    #     today_date = central
    #     today_date_end = central
    #     today_date += datetime.timedelta(minutes=5)
    #     print(today_date_end, "today_date_end>>>>>>>>>")
    #     userid = user_id
    #     if userid == "":
    #         return "User Details Not Found."
    #
    #     is_confirmed_match = {"$match": {'confirmation.is_confirmed': 1}}
    #     private_match = {"$match": {"open_to_all": {"$eq": "public"}}}
    #     rtsort = {"$sort": {"start": -1}}
    #
    #     match = {"$match": {"$or": [{"owner.user_id": ObjectId(userid)},
    #                                 {"speakers": {
    #                                     "$elemMatch": {
    #                                         "user_id": ObjectId(userid),
    #                                         "deleted_at.status": {"$eq": 0},
    #                                         "has_confirmed": {"$in": [0, 1]}
    #                                     }
    #                                 }
    #                                 },
    #                                 {"moderator": {
    #                                     "$elemMatch": {
    #                                         "user_id": ObjectId(userid),
    #                                         "deleted_at.status": {"$eq": 0},
    #                                         "has_confirmed": {"$in": [0, 1]}
    #                                     }
    #                                 }},
    #                                 {"owner": {"$eq": {"user_id": ObjectId(userid)}}},
    #                                 {"audience": {
    #                                     "$elemMatch": {
    #                                         "user_id": ObjectId(userid),
    #                                         "invited_flag": {"$eq": 1},
    #                                         "deleted_at.status": {"$eq": 0},
    #                                         "has_confirmed": {"$in": [0, 1]}
    #                                     }
    #                                 }
    #                                 },
    #                                 ]}}
    #
    #     limit = 10
    #     skip = 0
    #     if paginate != "":
    #         limit = paginate['limit']
    #         skip = paginate['skip']
    #
    #     skipfilter = {"$skip": skip}
    #     limitfilter = {"$limit": limit}
    #
    #     rtsort = {"$sort": {"created_at": -1}}
    #
    #     query = [
    #         {
    #             "$match": {
    #                 "deleted_at.is_deleted": 0
    #             }
    #         },
    #         match,
    #         private_match,
    #         is_confirmed_match,
    #
    #         {"$addFields": {
    #             "moderator": {
    #                 "$filter": {
    #                     "input": "$moderator",
    #                     "as": "moderator",
    #                     "cond": {
    #                         "$and": [
    #                             {"$eq": ["$$moderator.deleted_at.status", 0]},
    #                         ]
    #                     }
    #                 }
    #             },
    #             'audience': {
    #                 "$filter": {
    #                     "input": "$audience",
    #                     "as": "audience",
    #                     "cond": {
    #                         "$and": [
    #                             {"$eq": ["$$audience.user_id", ObjectId(userid)]},
    #                             {"$eq": ["$$audience.deleted_at.status", 0]},
    #                             {"$ne": ["$$audience.has_confirmed", 2]}
    #                         ]
    #                     }
    #                 }
    #             },
    #
    #             "speakers": {
    #                 "$filter": {
    #                     'input': "$speakers",
    #                     'as': "speakers",
    #                     'cond': {
    #                         "$and": [
    #                             {'$eq': ["$$speakers.deleted_at.status", 0]},
    #                             {'$ne': ["$$speakers.has_confirmed", 2]}
    #                         ]
    #                     }
    #                 }
    #             },
    #             "start": "$utc_time.start",
    #             "end": "$utc_time.end",
    #             "all_users": {"$setUnion": [
    #                 {"$ifNull": ["$moderator", []]},
    #                 {"$ifNull": ["$speakers", []]},
    #                 {"$ifNull": ["$audience", []]},
    #                 ["$owner"]
    #             ]},
    #             "active_flag": {
    #                 "$cond": [
    #                     {
    #                         "$and": [
    #                             {
    #                                 "$lte": [
    #                                     "$utc_time.start",
    #                                     today_date
    #                                 ]
    #                             },
    #                             {
    #                                 "$gte": [
    #                                     "$utc_time.end",
    #                                     today_date_end
    #                                 ]
    #                             }
    #                         ]
    #                     },
    #                     True,
    #                     False
    #                 ]
    #
    #             },
    #             "upcoming_flag": {
    #
    #                 "$cond": [
    #                     {
    #                         "$gte": [
    #                             "$utc_time.start",
    #                             today_date
    #                         ]
    #                     },
    #                     True,
    #                     False
    #                 ]
    #
    #             },
    #             "happened_flag": {
    #
    #                 "$cond": [
    #                     {
    #                         "$lte": [
    #                             "$utc_time.end",
    #                             today_date_end
    #                         ]
    #                     },
    #                     True,
    #                     False
    #                 ]
    #
    #             },
    #         }},
    #         {"$addFields": {
    #             "speakers": {
    #                 "$filter": {
    #                     "input": "$speakers",
    #                     "as": "speakers",
    #                     "cond": {"$ne": ["$$speakers", {}]}
    #                 }
    #             },
    #             "audience": {
    #                 "$filter": {
    #                     "input": "$audience",
    #                     "as": "audience",
    #                     "cond": {"$ne": ["$$audience", {}]}
    #                 }
    #             },
    #
    #             "accepted_count": "$accepted_count",
    #             "rejected_count": "$rejected_count",
    #             "roundtable_code": "$roundtable_code",
    #             "viewer_count": "$viewer_count",
    #             "invite_count": "$invite_count",
    #             "req_visitor_count": "$req_visitor_count",
    #             "last_request_user": "$last_req",
    #             "is_cancelled": "$is_cancelled",
    #             "broadcast_live_flag": "$broadcast_live",
    #             "reminder_set": {"$in": [ObjectId(userid), {"$ifNull": ['$requested_user_reminders', []]}]},
    #             "invite_requested": {"$in": [ObjectId(userid), {"$ifNull": ['$req_visitor_invitations', []]}]},
    #
    #             "moderator_flag": {'$eq': [{'$arrayElemAt': ['$moderator.user_id', 0]}, ObjectId(userid)]},
    #             "speaker_flag": {"$gt": [{
    #                 "$size": {
    #                     "$filter": {
    #                         "input": "$speakers",
    #                         "as": "user",
    #                         "cond": {
    #                             "$and": [
    #                                 {"$eq": ["$$user.user_id", ObjectId(userid)]},
    #                             ]
    #
    #                         }
    #                     }
    #                 }
    #             }, 0]},
    #
    #             "owner_flag": {"$eq": ["$owner.user_id", ObjectId(userid)]},
    #             "was_invited": {'$gt':
    #                                 [{'$size':
    #                                       {'$filter':
    #                                            {"input": '$all_users',
    #                                             "as": 'user',
    #                                             "cond":
    #                                                 {'$and':
    #                                                      [{'$eq': ['$$user.user_id', ObjectId(userid)]},
    #                                                       {'$ne': ['$$user.has_confirmed', 2]},
    #                                                       {"$eq": [{'$ifNull': ["$$user.deleted_at.status", 0]}, 0]}
    #
    #                                                       ]}}}},
    #                                  0]},
    #
    #         }},
    #         {"$unset": "audience"},
    #         {"$unwind": {"path": "$speakers",
    #                      "preserveNullAndEmptyArrays": True}},
    #         {"$lookup": {
    #             "from": "users",
    #             "localField": "speakers.user_id",
    #             "foreignField": "_id",
    #             "as": "speakers_user",
    #         }},
    #
    #         {"$lookup": {
    #             "from": "users",
    #             "localField": "moderator.user_id",
    #             "foreignField": "_id",
    #             "as": "moderator_user",
    #         }},
    #         {"$lookup": {
    #             "from": "users",
    #             "localField": "owner.user_id",
    #             "foreignField": "_id",
    #             "as": "owner_user",
    #         }},
    #         {'$group': {
    #             '_id': '$_id',
    #             'name': {'$first': '$name'},
    #             'owner_flag': {'$first': '$owner_flag'},
    #             'moderator_flag': {'$first': '$moderator_flag'},
    #             'speaker_flag': {'$first': '$speaker_flag'},
    #             'active_flag': {'$first': '$active_flag'},
    #             'accepted_count': {'$first': '$accepted_count'},
    #             'agora_channel': {'$first': '$agora_channel'},
    #             'agora_token': {'$first': '$agora_token'},
    #             'email_list': {'$first': '$email_list'},
    #             'phone_list': {"$first": "$phone_list"},
    #             "is_cancelled": {"$first": "$is_cancelled"},
    #             "followers": {"$first": "$followers"},
    #             "following": {"$first": "$following"},
    #             "happened_flag": {"$first": "$happened_flag"},
    #             "is_cancelled": {"$first": "$is_cancelled"},
    #             'past_rtid': {'$first': '$past_rtid'},
    #             'r_type': {'$first': '$r_type'},
    #             'rejected_count': {'$first': '$rejected_count'},
    #             'reminder_set': {'$first': '$reminder_set'},
    #             'req_visitor_count': {'$first': '$req_visitor_count'},
    #             'req_visitor_invitations': {'$first': '$req_visitor_invitations'},
    #             'requested_user_reminders': {'$first': '$requested_user_reminders'},
    #             'roundtable_code': {'$first': '$roundtable_code'},
    #             'req_visitor_count': {'$first': '$req_visitor_count'},
    #             "created_at": {"$first": "$created_at"},
    #             "recording": {"$first": "$recording"},
    #
    #             'was_invited': {'$first': '$was_invited'},
    #             'media': {'$first': '$media'},
    #             'doc_media': {'$first': '$doc_media'},
    #             'description': {'$first': '$description'},
    #             'start': {'$first': '$utc_time.start'},
    #             'end': {'$first': '$utc_time.end'},
    #             "time": {'$first': "$utc_time", },
    #             "upcoming_flag": {'$first': "$upcoming_flag", },
    #             "userid_list": {'$first': "$userid_list", },
    #             "invite_requested": {'$first': "$invite_requested", },
    #             'tags': {'$first': '$tags'},
    #             "viewer_count": {"$first": "$viewer_count"},
    #             "invite_count": {"$first": "$invite_count"},
    #             "join_count": {"$first": "$join_count"},
    #             "user_views_count": {"$first": "$user_views_count"},
    #             "rejected_count": {"$first": "$rejected_count"},
    #             "broadcast_live_flag": {"$first": "$broadcast_live"},
    #             'category': {'$first': '$category'},
    #             'speakers': {'$addToSet': {
    #                 'name': {'$arrayElemAt': ['$speakers_user.name',
    #                                           0]},
    #                 'username': {'$arrayElemAt': ['$speakers_user.username'
    #                     , 0]},
    #                 'email': {'$arrayElemAt': ['$speakers_user.email',
    #                                            0]},
    #                 'phone_number': {'$arrayElemAt': ['$speakers_user.phone_number'
    #                     , 0]},
    #                 'user_id': {'$arrayElemAt': ['$speakers_user._id',
    #                                              0]},
    #                 'has_confirmed': '$speakers.has_confirmed',
    #                 'bio': '$speakers.bio',
    #                 'already_invited': '$speakers.already_invited',
    #                 'index': '$speakers.index',
    #                 'type': '$speakers.type',
    #             }},
    #
    #             'moderator': {'$first': {
    #                 'name': {'$arrayElemAt': ['$moderator_user.name',
    #                                           0]},
    #                 'username': {'$arrayElemAt': ['$moderator_user.username'
    #                     , 0]},
    #                 'email': {'$arrayElemAt': ['$moderator_user.email',
    #                                            0]},
    #                 'phone_number': {'$arrayElemAt': ['$moderator_user.phone_number'
    #                     , 0]},
    #                 'user_id': {'$arrayElemAt': ['$moderator_user._id',
    #                                              0]},
    #                 'bio': {'$arrayElemAt': ['$moderator.bio', 0]},
    #                 'has_confirmed': {'$arrayElemAt': ['$moderator.has_confirmed'
    #                     , 0]},
    #                 'm_type': {'$arrayElemAt': ['$moderator.m_type'
    #                     , 0]},
    #             }},
    #             'owner': {'$first': {
    #                 'name': {'$arrayElemAt': ['$owner_user.name', 0]},
    #                 'username': {'$arrayElemAt': ['$owner_user.username'
    #                     , 0]},
    #                 'email': {'$arrayElemAt': ['$owner_user.email',
    #                                            0]},
    #                 'phone_number': {'$arrayElemAt': ['$owner_user.phone_number'
    #                     , 0]},
    #                 'user_id': {'$arrayElemAt': ['$owner_user._id',
    #                                              0]},
    #                 'anonymous_flag': '$owner.anonymous',
    #             }},
    #             'open_to_all': {'$first': '$open_to_all'},
    #
    #         }},
    #         {"$addFields": {
    #             "speakers": {"$filter": {"input": "$speakers",
    #                                      "as": "speakers",
    #                                      "cond": {"$ne": ["$$speakers", {}]},
    #                                      }},
    #         }},
    #         rtsort,
    #         skipfilter,
    #         limitfilter
    #     ]
    #
    #     from db_config import pymongo_db
    #     mydb = pymongo_db()
    #     res = mydb.aggregate(query, allowDiskUse=True)
    #     #res = RoundT.objects.mongo_aggregate(query, allowDiskUse=True)
    #     res = list(res)
    #     res = loads(dumps(res, indent=2))
    #     if res and len(res) > 0:
    #         return res
    #     else:
    #         return ''
    #
