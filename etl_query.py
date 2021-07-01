#query for table tweet_user
tweet_user_query = """insert into "twitter"."tweet_user" \
("id", \
"id_str", \
"name", \
"screen_name", \
"location", \
"description", \
"url", \
"protected", \
"followers_count", \
"friends_count", \
"listed_count", \
"created_at", \
"favourites_count", \
"utc_offset", \
"geo_enabled", \
"verified", \
"statuses_count", \
"lang", \
"contributors_enabled", \
"is_translator", \
"profile_background_color", \
"profile_background_image_url", \
"profile_background_tile", \
"profile_image_url", \
"profile_image_url_https", \
"profile_link_color", \
"profile_sidebar_border_color", \
"profile_sidebar_fill_color", \
"profile_text_color", \
"profile_use_background_image", \
"default_profile", \
"default_profile_image", \
"following", \
"follow_request_sent", \
"notifications", \
"translator_type") \
values 
(%(id)s, \
%(id_str)s, \
%(name)s, \
%(screen_name)s, \
%(location)s, \
%(description)s, \
%(url)s, \
%(protected)s, \
%(followers_count)s, \
%(friends_count)s, \
%(listed_count)s, \
%(created_at)s, \
%(favourites_count)s,\
%(utc_offset)s, \
%(geo_enabled)s, \
%(verified)s, \
%(statuses_count)s, \
%(lang)s, \
%(contributors_enabled)s, \
%(is_translator)s, \
%(profile_background_color)s, \
%(profile_background_image_url)s, \
%(profile_background_tile)s, \
%(profile_image_url)s, \
%(profile_image_url_https)s, \
%(profile_link_color)s, \
%(profile_sidebar_border_color)s, \
%(profile_sidebar_fill_color)s, \
%(profile_text_color)s, \
%(profile_use_background_image)s, \
%(default_profile)s, \
%(default_profile_image)s, \
%(following)s, %(follow_request_sent)s,\
%(notifications)s,\
%(translator_type)s) \
on conflict do nothing"""

#query for table : tweet
tweet_query = """insert into "twitter"."tweet" \
("id",\
"id_str",\
"user_id", \
"created_at", \
"text", \
"source", \
"truncated", \
"lang", \
"retweet_count", \
"quote_count", \
"reply_count", \
"in_reply_to_status_id", \
"in_reply_to_status_id_str", \
"in_reply_to_user_id", \
"in_reply_to_user_id_str")
values \
(%(id)s, \
%(id_str)s, \
%(user_id)s, \
%(created_at)s, \
%(text)s, \
%(source)s, \
%(truncated)s, \
%(lang)s, \
%(retweet_count)s, \
%(quote_count)s, \
%(reply_count)s, \
%(in_reply_to_status_id)s, \
%(in_reply_to_status_id_str)s, \
%(in_reply_to_user_id)s, \
%(in_reply_to_user_id_str)s)\
on conflict do nothing"""

#query for table : retweeted_tweet
rt_query = """insert into "twitter"."retweeted_tweet" \
("tweet_id", \
"retweeted_id", \
"retweet_user", \
"retweet_text") \
values \
(%(tweet_id)s, \
%(retweeted_id)s,\
%(retweet_user)s,\
%(retweet_text)s) \
on conflict do nothing"""

#query for table : quoted_tweet
qt_query = """insert into "twitter"."quoted_tweet" \
("tweet_id", \
"quoted_id", \
"quoted_user",\
"quoted_text") \
values \
(%(tweet_id)s, \
%(quoted_id)s, \
%(quoted_user)s,\
%(quoted_text)s) \
on conflict do nothing"""

#query for table : hashtag
hashtag_query = """insert into "twitter"."hashtags" \
("tweet_id", \
"hashtag") \
values \
(%(tweet_id)s, \
%(hashtag)s) \
on conflict do nothing"""

#query for table : symbol
symbol_query = """insert into "twitter"."symbol" \
("tweet_id",\
"symbol") \
values \
(%(tweet_id)s, \
%(symbol)s) \
on conflict do nothing"""

#query for table : place
place_query = """insert into "twitter"."place" \
("url", \
"place_type", \
"name", \
"full_name", \
"country_code", \
"country", \
"coordinates", \
"tweet_id") \
values \
(%(url)s, \
%(place_type)s, \
%(name)s, \
%(full_name)s, \
%(country_code)s, \
%(country)s, \
%(coordinates)s, \
%(tweet_id)s) \
 on conflict do nothing"""

#query for table : media
media_query = """insert into "twitter"."media" \
("id", \
"id_str", \
"media_url", \
"media_url_https", \
"display_url", \
"expanded_url", \
"type", \
"tweet_id") \
values \
(%(id)s, \
%(id_str)s, \
%(media_url)s, \
%(media_url_https)s, \
%(display_url)s, \
%(expanded_url)s, \
%(type)s, \
%(tweet_id)s) \
on conflict do nothing"""

#query for table : mention
mention_query = """insert into "twitter"."user_mentions" \
("screen_name", \
"name", \
"id", \
"id_str", \
"tweet_id") \
values \
(%(screen_name)s, \
%(name)s, \
%(id)s, \
%(id_str)s, \
%(tweet_id)s) \
on conflict do nothing"""