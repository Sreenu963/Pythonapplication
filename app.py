import redis
import json
import matplotlib.pyplot as plt
from api import TechnologyCompanyAPI  

class DataProcessor:
    def __init__(self, data, redis_host, redis_port):
        """
        Initialize the DataProcessor with data, and Redis connection details.

        Args:
            data (list): The data to process.
            redis_host (str): The host of the Redis server.
            redis_port (int): The port of the Redis server.
        """
        self.data = data
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)

    def insert_into_redisjson(self):
        """
        Insert JSON data into RedisJSON.
        """
        for item in self.data:
            self.redis_client.set(item['id'], json.dumps(item))

    def generate_chart(self):
        """
        Generate a bar chart showing the distribution of product prices.
        """
        categories = set(item['category'] for item in self.data)
        category_prices = {category: [] for category in categories}

        for item in self.data:
            category_prices[item['category']].append(item['price'])

        plt.figure(figsize=(10, 6))
        for category, prices in category_prices.items():
            plt.hist(prices, bins=20, alpha=0.5, label=category)

        plt.xlabel('Price')
        plt.ylabel('Frequency')
        plt.title('Price Distribution by Category')
        plt.legend()
        plt.show()

    def perform_aggregation(self):
        """
        Perform aggregation on the provided data.

        Returns:
            dict: Aggregation results including total count, average price, and price range.
        """
        total_count = len(self.data)
        total_price = sum(item['price'] for item in self.data)
        average_price = total_price / total_count
        min_price = min(item['price'] for item in self.data)
        max_price = max(item['price'] for item in self.data)

        return {
            'total_count': total_count,
            'average_price': average_price,
            'price_range': {'min_price': min_price, 'max_price': max_price}
        }

    def search_data(self, query):
        """
        Search for data based on the given query.

        Args:
            query (str): The search query.

        Returns:
            list: List of items matching the query.
        """
        # Search for items where the name or description contains the query string
        results = [item for item in self.data if query.lower() in item.get('name', '').lower() or query.lower() in item.get('description', '').lower()]
        return results

if __name__ == "__main__":
    # Mock data generation
    mock_data = TechnologyCompanyAPI.get_products(100)

    # Print generated data
    print("Generated Data:")
    for item in mock_data:
        print(item)

    # Redis connection details
    redis_host = "localhost"
    redis_port = 6379

    # Data processing
    processor = DataProcessor(mock_data, redis_host, redis_port)
    processor.insert_into_redisjson()
    processor.generate_chart()
    aggregation_result = processor.perform_aggregation()
    print("Aggregation Result:", aggregation_result)

    # Search data
    search_query = input("Enter search query: ")
    search_results = processor.search_data(search_query)
    print("Search Results:", search_results)
