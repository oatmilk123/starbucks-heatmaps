import datetime
import httpx
import json
import july
from july.utils import date_range
import matplotlib.pyplot as plt
import calendar

headers = {
    "authority": "api.twitter.com",
    "accept": "*/*",
    "authorization": "Bearer TOKEN",
    "x-guest-token": "TOKEN",
    "x-csrf-token": "TOKEN",
}

params = {
    "include_profile_interstitial_type": "1",
    "include_blocking": "1",
    "include_blocked_by": "1",
    "include_followed_by": "1",
    "include_want_retweets": "1",
    "include_mute_edge": "1",
    "include_can_dm": "1",
    "include_can_media_tag": "1",
    "include_ext_has_nft_avatar": "1",
    "include_ext_is_blue_verified": "1",
    "include_ext_verified_type": "1",
    "skip_status": "1",
    "cards_platform": "Web-12",
    "include_cards": "1",
    "include_ext_alt_text": "true",
    "include_ext_limited_action_results": "false",
    "include_quote_count": "true",
    "include_reply_count": "1",
    "tweet_mode": "extended",
    "include_ext_collab_control": "true",
    "include_ext_views": "true",
    "include_entities": "true",
    "include_user_entities": "true",
    "include_ext_media_color": "true",
    "include_ext_media_availability": "true",
    "include_ext_sensitive_media_warning": "true",
    "include_ext_trusted_friends_metadata": "true",
    "send_error_codes": "true",
    "simple_quoted_tweet": "true",
    "q": '"caramel brulee" until:2022-01-01 since:2022-01-02',
    "tweet_search_mode": "live",
    "query_source": "typed_query",
    "count": "20",
    "requestContext": "launch",
    "pc": "1",
    "spelling_corrections": "1",
    "include_ext_edit_control": "true",
    "ext": "mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,enrichments,superFollowMetadata,unmentionInfo,editControl,collab_control,vibe",
}

url = "https://api.twitter.com/2/search/adaptive.json"

date_generator = (
    datetime.datetime(2022, 1, 1) + datetime.timedelta(days=i) for i in range(368)
)

data = []

from_date, until_date = next(date_generator).strftime("%Y-%m-%d"), next(
    date_generator
).strftime("%Y-%m-%d")

for i in range(366):
    params["q"] = f'"caramel brulee" until:{until_date} since:{from_date}'
    response = httpx.get(url, headers=headers, params=params)
    response_dict = json.loads(response.text)
    data.append(len(response_dict["globalObjects"]["tweets"].keys()))
    from_date, until_date = until_date, next(date_generator).strftime("%Y-%m-%d")


print(data)


dates = date_range("2022-01-01", "2022-12-31")

"""
Heatmap using july (horizontal, github style) -
"""

heatmap = july.heatmap(dates, data, title="Caramel Brulée!", cmap="github")
plt.savefig("heatmap2.png")

"""
Heatmap using matplotlib directly (vertical) -
"""

max_data, min_data = max(data), min(data)

days = list(range(1, 32))
months = list(calendar.month_name)[1:]

month_lens = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


start = 0
monthly_subsets = []
for i in month_lens:
    current_subset = data[start : start + i]
    if len(current_subset) < 31:
        current_subset += [0] * (31 - len(current_subset))
    monthly_subsets.append(current_subset)
    start += i

figure, axes = plt.subplots(figsize=(14, 8))
image = axes.imshow(monthly_subsets, cmap="Oranges")

axes.set_xticks(range(len(days)), days)
axes.set_yticks(range(len(months)), months)


cbar = figure.colorbar(image, ticks=[min_data, max_data], orientation="horizontal")
cbar.ax.set_xticklabels([min_data, max_data])

font = {"family": "serif", "color": "black", "size": 25}
cbar.set_label("Number of tweets about the drink (per day)", fontdict=font)
axes.set_title("How popular was the Caramel Brulée in 2022?", fontdict=font)

plt.xlabel("Days", fontdict=font)
plt.ylabel("Months", fontdict=font)
figure.tight_layout()
plt.savefig("heat_brulee.png")
