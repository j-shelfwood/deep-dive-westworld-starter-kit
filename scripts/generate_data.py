# Import required libraries again due to previous error
import random
import pandas as pd
from shapely.geometry import Point, Polygon
import json
import numpy as np


# Function to generate a random point within a given polygon (previously defined, redefining due to previous error)
def generate_random_point_in_polygon(polygon):
    minx, miny, maxx, maxy = polygon.bounds
    while True:
        point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(point):
            return point
        
# Function to generate a random point around a given point (previously defined, redefining due to previous error)
def generate_random_point_around(poi, radius=50):
    angle = random.uniform(0, 2 * 3.141592653589793)
    distance = random.uniform(0, radius)
    x = poi['longitude'] + distance * np.cos(angle)
    y = poi['latitude'] + distance * np.sin(angle)
    return Point(x, y)

# Redefine the Park class to encapsulate related data and behavior
class Park:
    def __init__(self, start_date, end_date):
        self.start_date = pd.Timestamp(start_date)
        self.end_date = pd.Timestamp(end_date)
        self.visitors = []
        self.incidents = []
        self.unresolved_incidents = []

    def create_incident(self, day_start, incident_type, severity, point_of_interest):
        timestamp = day_start + pd.Timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
        incident_data = {
            'incident_id': f'INC-{day_start.date()}-{len(self.incidents) + 1}',
            'timestamp': timestamp,
            # Assuming you have some way to generate or pick the latitude and longitude
            'latitude': random.uniform(0, 100),
            'longitude': random.uniform(0, 100),
            'type': incident_type,
            'severity': severity,
            'point_of_interest': point_of_interest
        }
        return incident_data

    def generate_correlated_incidents(self, day_start, incident_types, severity_levels):
        for incident in self.incidents:
            if incident['type'] == 'Malfunction' and random.choice([True, False]):
                new_incident = self.create_incident(day_start, 'Host Destroyed', 'High', incident['point_of_interest'])
                self.incidents.append(new_incident)

    def resolve_or_escalate_incidents(self):
        for incident in self.unresolved_incidents:
            if random.choice([True, False]):  # Randomly resolve or escalate
                incident['severity'] = 'Critical'
            else:
                self.unresolved_incidents.remove(incident)
    
    def generate_visitors(self, high_season_dates, winter_dates):
        date_range = pd.date_range(self.start_date, self.end_date)
        
        for day_start in date_range:
            total_visitors = random.randint(100, 300)
            if day_start in high_season_dates:
                total_visitors += random.randint(100, 200)
            
            male_factor = 0.6 if day_start in winter_dates else 0.5
            male_visitors = int(total_visitors * male_factor)
            female_visitors = total_visitors - male_visitors

            visitor_data = {
                'Date': day_start,
                'Total_Visitors': total_visitors,
                'Male_Visitors': male_visitors,
                'Female_Visitors': female_visitors
            }
            self.visitors.append(visitor_data)
            
    def generate_incidents(self, points_of_interest, island_shape, incident_types, severity_levels):
        date_range = pd.date_range(self.start_date, self.end_date)
        
        for day_start in date_range:
            day_visitors = next(item for item in self.visitors if item["Date"] == day_start)
            total_visitors = day_visitors["Total_Visitors"]
            male_visitors = day_visitors["Male_Visitors"]
            num_incidents = int(total_visitors / 80) + int(male_visitors / 160)
            day_of_week = day_start.weekday()

            if day_of_week >= 5:  # It's a weekend
                num_incidents += config['weekend_modifier']

            if day_of_week == 0:  # It's a Monday
                num_incidents += config['monday_modifier']

            self.resolve_or_escalate_incidents()
            
            # Generate incidents around Points of Interest (POIs)
            for _ in range(num_incidents):
                self.generate_incident_around_poi(day_start, points_of_interest, incident_types, severity_levels)
            
            self.generate_correlated_incidents(day_start, incident_types, severity_levels)
                
            # Generate random incidents around the island
            random_incidents_today = random.randint(1, 4)
            for _ in range(random_incidents_today):
                self.generate_random_incident(day_start, island_shape, points_of_interest, incident_types, severity_levels)

    def generate_incident_around_poi(self, day_start, points_of_interest, incident_types, severity_levels):

        violent_pois = [p for p in points_of_interest if p['narrative_level'] == 'violent']
        
        poi = random.choice([p for p in violent_pois if p.get('type') != 'facility'])

        incident_point = generate_random_point_around(poi)
        
        # Determine incident type and severity based on narrative level and POI
        if poi['narrative_level'] == 'violent':
            incident_type = random.choices(incident_types, weights=[1, 1, 3, 1, 1])[0]
            severity = random.choices(severity_levels, weights=[1, 1, 2, 1])[0]
        elif poi['narrative_level'] == 'peaceful':
            incident_type = random.choices(incident_types, weights=[3, 2, 1, 1, 1])[0]
            severity = 'Low'
        else:
            incident_type = random.choice(incident_types)
            severity = random.choice(severity_levels)

        day_visitors = next(item for item in self.visitors if item["Date"] == day_start)
        if day_visitors['Male_Visitors'] > day_visitors['Female_Visitors']:
            if random.choice([True, False]):
                incident_type = 'Host Destroyed'
                severity = 'High'

        # Timestamp within the day
        timestamp = day_start + pd.Timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        incident_data = {
            'incident_id': f'INC-{day_start.date()}-{len(self.incidents) + 1}',
            'timestamp': timestamp,
            'latitude': incident_point.y,
            'longitude': incident_point.x,
            'type': incident_type,
            'severity': severity,
            'point_of_interest': poi['title']
        }
        self.incidents.append(incident_data)

    def generate_random_incident(self, day_start, island_shape, points_of_interest, incident_types, severity_levels):
        incident_point = generate_random_point_in_polygon(island_shape)
        poi = random.choice(points_of_interest)  # Just for naming, not influencing the incident
        
        incident_type = random.choice(incident_types)
        severity = random.choice(severity_levels)
        
        # Timestamp within the day
        timestamp = day_start + pd.Timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        incident_data = {
            'incident_id': f'INC-{day_start.date()}-{len(self.incidents) + 1}',
            'timestamp': timestamp,
            'latitude': incident_point.x,
            'longitude': incident_point.y,
            'type': incident_type,
            'severity': severity,
            'point_of_interest': poi['title']
        }
        self.incidents.append(incident_data)

    def to_json(self, visitor_file_path, incident_file_path):
        visitor_df = pd.DataFrame(self.visitors)
        incident_df = pd.DataFrame(self.incidents)
        
        visitor_df.to_json(visitor_file_path, orient='records', date_format='iso')
        incident_df.to_json(incident_file_path, orient='records', date_format='iso')

# Continue the configuration parameters with a new config dictionary
config = {
    'start_date': '2023-09-01',
    'end_date': '2024-08-30',
    'high_season_dates': pd.date_range('2023-12-20', '2024-01-10').union(pd.date_range('2023-07-01', '2023-08-31')),
    'winter_dates': pd.date_range('2023-11-01', '2024-02-28'),
    'weekend_modifier': 2,
    'monday_modifier': -1,
    'incident_types': ['Malfunction', 'Narrative ended', 'Host Destroyed', 'Decor destroyed', 'Terrain destroyed'],
    'severity_levels': ['Low', 'Medium', 'High', 'Critical'],
    'visitor_file_path': 'data/visitor_data.json',
    'incident_file_path': 'data/incident_reports.json'
}

# Load points of interest from data/points_of_interest.json
with open('data/points_of_interest.json') as f:
    points_of_interest = json.load(f)

# Load the island polygon
with open('objects/island.json', 'r') as f:
    island_data = json.load(f)
island_shape = Polygon(island_data['features'][0]['geometry']['coordinates'][0])

# Main script
if __name__ == '__main__':
    # Initialize Park object
    westworld_park = Park(config['start_date'], config['end_date'])
    
    # Generate visitor data
    westworld_park.generate_visitors(config['high_season_dates'], config['winter_dates'])
    
    # Generate incidents
    westworld_park.generate_incidents(points_of_interest, island_shape, config['incident_types'], config['severity_levels'])
    
    # Export to JSON (commented out to prevent file operations)
    westworld_park.to_json(config['visitor_file_path'], config['incident_file_path'])