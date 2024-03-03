import requests
import redis
import json
import matplotlib.pyplot as plt
from datetime import datetime

class DataProcessor:
    def __init__(self, api_url, redis_host='localhost', redis_port=6379):
        """
            redis_host (str): Hostname of the Redis server (default: 'localhost')
            redis_port (int): Port of the Redis server (default: 6379)
        """
        self.api_url = api_url
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)

    def fetch_data_from_api(self):
        """Fetch JSON data from the specified API"""
        response = requests.get(self.api_url)
        if response.status_code == 200:
            data = response.json()
            print("Fetched data:")
            print(json.dumps(data, indent=2))
            return data
        else:
            print("Failed to fetch data from API")
            return None

    def insert_into_redis(self, data):
        """Insert JSON data into Redis"""
        for idx, item in enumerate(data):
            self.redis_client.set(f"data:{idx}", json.dumps(item))

    def perform_aggregation(self):
        """Perform aggregation on the stored data"""
        total_items = self.redis_client.dbsize()
        print(f"Total items stored in Redis: {total_items}")

    def search_data(self, query, data):
        """Search for data in fetched data based on a query"""
        matching_items = [item for item in data if query.lower() in str(item).lower()]
        if matching_items:
            print("Matching items found:")
            for item in matching_items:
                print(item)
        else:
            print("No matching items found")

    def process_data(self, data):
        """Process fetched data to extract version and added date"""
        api_versions = []
        api_dates = []
        for api, api_data in data.items():
            for version, version_data in api_data['versions'].items():
                api_versions.append(version)
                api_dates.append(version_data['added'])
        
        # Sort based on added date
        sorted_data = sorted(zip(api_versions, api_dates), key=lambda x: x[1], reverse=True)[:10]
        versions, added_dates = zip(*sorted_data)
        
        # Convert added dates to datetime objects
        added_dates = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ") for date in added_dates]
        
        return versions, added_dates

    def generate_chart(self, versions, added_dates):
        """Generate a chart based on versions and added dates"""
        plt.plot(added_dates, versions, marker='o', linestyle='-')
        plt.xlabel('Added Date')
        plt.ylabel('Version')
        plt.title('Top 10 APIs based on Version and Date')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    api_url = "https://api.apis.guru/v2/list.json"
    processor = DataProcessor(api_url)

    # Fetch data from API
    data = processor.fetch_data_from_api()

    if data:
        # Insert data into Redis
        processor.insert_into_redis(data)

        # Generate a chart based on versions and added dates for top 10 APIs
        versions, added_dates = processor.process_data(data)
        processor.generate_chart(versions, added_dates)

        # Aggregation
        processor.perform_aggregation()

        # Prompt user to search for data
        query = input("Enter query to search: ")
        processor.search_data(query, data) 

