import facebook
from collections import OrderedDict

# Common Education 

def common_edu(token):
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	friends = graph.get_connections("me", "friends")['data']

	friends_education = {friend['name']: graph.get_connections(friend['id'], "education")['data'] for friend in friends}
	my_edu = [school['school']['name'] for school in profile['education']]

	friends_education = [school['school']['name'] for school in friends_education['name'] for name in friends_education]
	print friends_education
	count = [len(set(f_edu) & set(my_edu)) for f_edu in friends_education]

	return sum(count)

# Obtaining User Profile and Friends objects from given Token

token = "EAACEdEose0cBAG8whg1HNTtV9LZBGyZCgZAtY3PoxEOwvpAZBqhjE8Gy4LTIxVYZCm3oBABimEOoDkaWZBcMSvTNEcIXh2IfdNu3qBgOFmTZBYlXoZAHMoVW4a7OKb3D5VXqLUVNAymxAMTWsOMyNkdJIOKbZBFiUPeK32oJw63gXCmU9F4156ejCSF17T8Sh9AAZD"

graph = facebook.GraphAPI(token)

user = "652062428215786"
profile = graph.get_object(user)

friends = graph.get_connections(user, "friends")['data']

user_name = profile['name']

friends_names = [friend['name'] for friend in friends]

friends_posts = { friend['name'] : 0 for friend in friends }

# Posts and Photos that friends tag User in 

posts_tagged_by_others = graph.get_connections(user, "posts", fields='from')['data']

for posts_tagged_by_other in posts_tagged_by_others:
	name = posts_tagged_by_other['from']['name']
	if user_name != name:
		if name in friends_names:
			friends_posts[name]+=70
		else:
			friends_posts[name]=70

friends_photos = { friend['name'] : 0 for friend in friends }

photos_tagged_by_others = graph.get_connections(user, "photos", fields='from')['data']

for photos_tagged_by_other in photos_tagged_by_others:
	name = photos_tagged_by_other['from']['name']
	if user_name != name:
		if name in friends_names:
			friends_photos[name]+=70


friends_likes = { friend['name'] : 0 for friend in friends }

# Likes by friends for User's posts

likes_tagged_by_others = graph.get_connections(user, "photos", fields="likes")['data']
for likes_tagged_by_other in likes_tagged_by_others:
	names = likes_tagged_by_other['likes']['data']
	for name in names:
		name1 = name['name']
		if user_name != name1:
			if name1 in friends_names:
				friends_likes[name1]+=3.5

# Comments by friends for User's posts

friends_likes1 = friends_likes
profile = graph.get_object(user)
user_name=profile['name']
posts = graph.get_connections(user,'posts',limit=100)['data']
friends_comments = { friend['name'] : 0 for friend in friends }
friends_pagelikes = { friend['name'] : 0 for friend in friends }

for i in posts:
	name=i['from']['name']
	if user_name != name:
		friends_comments[name]+=10

# Common Pages liked 

my_likes = [ like['name']
             	for like in graph.get_connections("652062428215786", "likes")['data'] ]
friends_likes = {friend['name']: graph.get_connections(friend['id'], "likes")['data'] for friend in friends}
for friend in friends:
	common_likes = list(set(my_likes) & set(friends_likes))
	count=len(common_likes)
	if count<5:
		friends_pagelikes[friend['name']]=10
	else:
		if count<20:
			friends_pagelikes[friend['name']]=20
		else:
			friends_pagelikes[friend['name']]=50

# Computing Total Score and Displaying 

total = { friend['name'] : 0 for friend in friends}
for name in friends_names:
	total[name] = friends_pagelikes[name]
for name in friends_names:
	total[name] += friends_comments[name]
for name in friends_names:
	total[name] += friends_likes1[name]
for name in friends_names:
	total[name] += friends_posts[name]
for name in friends_names:
	total[name] += friends_photos[name]
for name in friends_names:
	total[name] = str(total[name])
for name in friends_names:
	print name + " : " + total[name]