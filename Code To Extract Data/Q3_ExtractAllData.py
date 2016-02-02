#File: Q3_ExtractAllData.py
#Description: Extract all open data related to categories, groups, members and events via Meetup API
#Date: Jan 31st, 2016
#Author: Chaitra Kamath

import requests #to extract data 
import pandas as pd #data frame type data manipulations
from geopy.geocoders import Nominatim #to geocode
import matplotlib.pyplot as plt #plot data
import time

api_key = 'my_api_key'
cities = ['Santa Fe','San Francisco']

def load_category(params):
	request = requests.get('http://api.meetup.com//2/categories',params=params)
	data = request.json()
	return data

category_id, category_name = [], []
def extract_category():
	for c in cities:
		per_page = 200
		offset = 0
		num_output_records = per_page
		while (num_output_records == per_page):
			address, (latitude, longitude) = geolocator.geocode(c)
			response = load_category({'lat': latitude, 'lon': longitude, 'radius': 25, 'offset': offset, 'key': api_key})
			#print ('response:', response)
			time.sleep(6)
			offset += 1
			for category in response['results']:
				category_id.append(category['id'])
				category_name.append(category['name'])
			num_output_records = response['meta']['count']
	categories_df = pd.DataFrame([category_id, category_name]).T 
	categories_df.columns = ['category_id', 'category_name']
	categories_df.to_csv('Categories.csv')
	time.sleep(6)

def load_groups(params):
	request = requests.get('http://api.meetup.com//2/groups',params=params)
	data = request.json()
	return data

group_category_id, group_category_name, group_created_date, group_description, group_id, group_member_count, group_name, group_organizer, group_rating, group_primary_topic, group_url_name, group_topics = [], [], [],[], [], [],[], [], [], [], [], []
def extract_groups():
	for c in cities:
		per_page = 200
		offset = 0
		num_output_records = per_page
		while (num_output_records == per_page):
			address, (latitude, longitude) = geolocator.geocode(c)
			response = load_groups({'lat': latitude, 'lon': longitude, 'radius': 25, 'offset': offset, 'key': api_key})
			time.sleep(6)
			offset += 1
			for group in response['results']:
				group_category_id.append(group['category']['id'])
				group_category_name.append(group['category']['name'])
				group_created_date.append(group['created'])
				group_description.append(group['description'])
				group_id.append(group['id'])
				group_member_count.append(group['members'])
				group_name.append(group['name'])
				group_organizer.append(group['organizer']['name'])
				group_rating.append(group['rating'])
				group_primary_topic.append(group['primary_topic'])
				group_url_name.append(group['url_name'])
				group_topics.append(group['topics'])
			num_output_records = response['meta']['count']
	groups_df = pd.DataFrame([group_category_id, group_category_name, group_created_date, group_description, group_id, group_member_count, group_name, group_organizer, group_rating, group_primary_topic, group_url_name, group_topics]).T 
	groups_df.columns = ['group_category_id', 'group_category_name', 'group_created_date', 'group_description', 'group_id', 'group_member_count', 'group_name', 'group_organizer', 'group_rating', 'group_primary_topic', 'group_url_name', 'group_topics']
	groups_df.to_csv('Groups.csv')
	time.sleep(6)

def load_members(params):
	request = requests.get('http://api.meetup.com//2/members',params=params)
	data = request.json()
	return data

member_bio, member_gender, member_id, member_joined, member_membership_count, member_name, member_topics, member_status = [], [], [], [], [], [], [], []
def extract_members():
	for gid in group_id:
		per_page = 200
		offset = 0
		num_output_records = per_page
		while (num_output_records == per_page):
			response = load_members({'group_id':gid, 'offset': offset, 'key': api_key})
			time.sleep(6)
			for member in response['results']:
				member_bio.append(member['bio'])
				member_gender.append(member['gender'])
				member_id.append(member['id'])
				member_joined.append(member['joined'])
				if 'membership_count' in member:
					member_membership_count.append(member['membership_count'])
				else:
					member_membership_count.append(0)
				member_name.append(member['name'])
				member_topics.append(member['topics'])
				member_status.append(member['status'])
			num_output_records = response['meta']['count']
	members_df = pd.DataFrame([member_bio, member_gender, member_id, member_joined, member_membership_count, member_name, member_topics, member_status]).T 
	members_df.columns = ['member_bio', 'member_gender', 'member_id', 'member_joined', 'member_membership_count', 'member_name', 'member_topics', 'member_status']
	members_df.to_csv('Members.csv')
	time.sleep(6)

def load_events(params):
	request = requests.get('http://api.meetup.com//2/open_events',params=params)
	data = request.json()
	return data

event_comment_count, event_description, event_distance, event_hosts, event_fee, event_group_id, event_category_id, event_headcount, event_name, event_maybe_rsvp_count, event_rsvp_limit, event_status, event_trending_rank, event_yes_rsvp_count = [], [], [], [], [], [], [], [], [], [], [], [], [], []
def extract_events(category_id_list):
	"""Find events by geo location or by category"""
	if searchByCity:
		for c in cities:
			per_page = 200
			offset = 0
			num_output_records = per_page
			while (num_output_records == per_page):
				address, (latitude, longitude) = geolocator.geocode(c)
				response = load_events({'lat': latitude, 'lon': longitude, 'radius': 25, 'offset': offset, 'key': api_key, 'fields': 'comment_count'})
				time.sleep(6)
				offset += 1
	else:
		for c_id in category_id_list:
			per_page = 200
			offset = 0
			num_output_records = per_page
			while (num_output_records == per_page):
				response = load_events({'category': c_id, 'offset': offset, 'key': api_key, 'fields': 'comment_count'})
				time.sleep(6)
				offset += 1

			for event in response['results']:
				event_comment_count.append(event['comment_count'])
				event_description.append(event['decription'])
				event_distance.append(event['distance'])
				event_duration.append(event['duration'])
				event_hosts.append(event['event_hosts']['member_name'])
				if 'fee' in event:
					event_fee.append(event['fee']['amount'])
				else:
					event_fee.append(0)
				event_group_id.append(event['group']['id'])
				event_category_id.append(event['group']['category']['id'])
				if 'headcount' in event:
					event_headcount.append(event['headcount'])
				else:
					event_headcount.append(0)
				event_name.append(event['name'])
				event_maybe_rsvp_count.append(event['maybe_rsvp_count'])
				event_rsvp_limit.append(event['rsvp_limit'])
				event_status.append(event['status'])
				event_trending_rank.append(event['trending_rank'])
				event_yes_rsvp_count.append(event['yes_rsvp_count'])
			num_output_records = response['meta']['count']
	events_df = pd.DataFrame([event_comment_count, event_description, event_distance, event_hosts, event_fee, event_group_id, event_category_id, event_headcount, event_name, event_maybe_rsvp_count, event_rsvp_limit, event_status, event_trending_rank, event_yes_rsvp_count])
	events_df.columns = ['event_comment_count', 'event_description', 'event_distance', 'event_hosts', 'event_fee', 'event_group_id', 'event_category_id', 'event_headcount', 'event_name', 'event_maybe_rsvp_count', 'event_rsvp_limit', 'event_status', 'event_trending_rank', 'event_yes_rsvp_count']
	events_df.to_csv('Events.csv')
	time.sleep(6)












