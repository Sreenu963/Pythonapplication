import json
import requests
import redis
import matplotlib.pyplot as plt

class DataProcessor:
    def __init__(self, api_url, redis_host, redis_port, redis_db):
    
        # DataProcessor with API URL and Redis connection details.
        self.api_url = api_url
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)

    def fetch_data_from_api(self):
        """Fetch JSON data from the API."""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error fetching data from API:", e)
            return None

    def insert_into_redis(self, data):
        """Insert JSON data into RedisJSON."""
        try:
            for key, value in data.items():
                self.redis_client.jsonset(key, '.', json.dumps(value))
        except redis.exceptions.RedisError as e:
            print("Error inserting data into Redis:", e)

    def generate_chart(self, data):
        """Generate a matplotlib chart based on data."""
        try:
            plt.plot(data)
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.title('Data Chart')
            plt.show()
        except Exception as e:
            print("Error generating chart:", e)

    def perform_aggregation(self, data):
        """Perform aggregation on data."""
        try:
            total = sum(data)
            average = total / len(data)
            return total, average
        except Exception as e:
            print("Error performing aggregation:", e)
# Search for data in a list based on a given query.
    def search_data(self, data, query):
        
        try:
           
            results = [item for item in data if query.lower() in item.get('name', '').lower()]
            return results
        except Exception as e:
            print("Error searching data:", e)
if __name__ == "__main__":
    # DataProcessor with mock API URL and Redis connection details
    processor = DataProcessor(api_url="http://127.0.0.1:5000/users",
                              redis_host="localhost",
                              redis_port=6379,
                              redis_db=0)

    # Fetch data from sophisticated mock API
    data = processor.fetch_data_from_api()
    if data:
        print("Data from API:", data)

        processor.generate_chart([1, 2, 3, 4, 5])

        # Aggregation
        total, average = processor.perform_aggregation([1, 2, 3, 4, 5])
        print("Total:", total)
        print("Average:", average)

        # List to store all search results
        all_results = []

        # Enter search query
        while True:
            query = input("Enter search query (Enter 'q' to quit): ")
            if query.lower() == 'q':
                break

            # Search data
            results = processor.search_data(data, query)
            print("Search Results:")
            if results:
                for result in results:
                    print(result)
                    all_results.append(result)
            else:
                print("No results found for query:", query)
        
        # Save all search results to search_results.txt file
        with open("search_results.txt", "w") as file:
            file.write(json.dumps(all_results))
