#File: Q3_SanFranSantaFe.py
#Description: Extract data about all meetup groups in Santa Fe and San Francisco
#Date: Jan 30th, 2016
#Author: Chaitra Kamath

import requests #to extract data 
import pandas as pd #data frame type data manipulations
from geopy.geocoders import Nominatim #to geocode
import matplotlib.pyplot as plt #plot data
import time

api_key = 'my_api_key'
cities = ['Santa Fe','San Francisco']
last_event_rsvp, next_event_rsvp,category, primary_topic, city, country, name, ratings, members, last_event, next_event, created_date, membership_fees, group_name = [],[], [], [],  [], [], [], [], [], [], [], [], [], []
geolocator = Nominatim()

def load_results(params):
	request = requests.get("http://api.meetup.com/2/groups",params=params)
	data = request.json()
	return data


def extract_data():
	for c in cities:
		per_page = 200
		offset = 0
		num_output_records = per_page
		while (num_output_records == per_page):
			address, (latitude, longitude) = geolocator.geocode(c)
			response = load_results({'lat': latitude, 'lon': longitude, 'radius': 25, 'offset': offset, 'key': api_key})
			#print ('response:', response)
			time.sleep(60)
			offset += 1
			for group in response['results']:
				if 'category' in group:
					category.append(group['category']['name'])
				else:
					category.append('None')
				if 'last_event' in group:
					last_event.append(group['last_event']['name'])
					last_event_rsvp.append(group['last_event']['yes_rsvp_count'])
				else:
					last_event.append('')
					last_event_rsvp.append('')
				if 'membership_dues' in group:
					membership_fees.append(group['membership_dues']['fee'])
				else:
					membership_fees.append(0)
				if 'next_event' in group:
					next_event.append(group['next_event']['name'])
					next_event_rsvp.append(group['next_event']['yes_rsvp_count'])
				else:
					next_event.append('')
					next_event_rsvp.append('')
				if 'primary_topic' in group:
					primary_topic.append(group['primary_topic'])
				else: 
					primary_topic.append('')
				city.append(group['city'])
				country.append(group['country'])
				ratings.append(group['rating'])
				created_date.append(group['created'])
				members.append(group['members'])
				group_name.append(group['name'])
			num_output_records = response['meta']['count']
		results_df = pd.DataFrame([group_name, city, country, ratings, created_date, members, last_event, next_event, category, primary_topic,membership_fees, last_event_rsvp, next_event_rsvp]).T 
		results_df.columns = ['group_name', 'city', 'country', 'ratings', 'created_date', 'members', 'last_event', 'next_event', 'category', 'primary_topic','membership_fees', 'last_event_rsvp', 'next_event_rsvp']
		results_df.to_csv('SanFran_SantaFe_Meetup_Data.csv')
		time.sleep(1)

if __name__=="__main__":
        extract_data()


