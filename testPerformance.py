import requests
from concurrent import futures
import time

def make_api_call(url):
    startTime = time.time()
    response = requests.get(url)
    endTime = time.time()
    responseTime = endTime - startTime
    
    return response.json(), responseTime

#Enter API URL
api_url = "http://FakeAPIURL/api/resource"

# Number of concurrent API calls to be made
numRequests = 50

#Holds time taken for all requests to complete
totalResponseTime = 0
# Holds the Average time for all requests
avgResponseTime = 0

# Array to store results of API calls
responses = []

with futures.ThreadPoolExecutor(max_workers=numRequests) as executor:
    # Adding API calls to the executor to be run concurrently
    future_to_url = {executor.submit(make_api_call, api_url): api_url for _ in range(numRequests)}
    
    # Getting results
    for future in futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data, responseTime = future.result()
            responses.append((data, responseTime))
            # Adding each responses time taken to the total
            totalResponseTime = totalResponseTime + responseTime

        except Exception as exc:
            print(f"Error occurred for {url}: {exc}")

# Printing responses
for response, responseTime in responses:
    print("Response: ", response)
    print("Response Time: ", responseTime)
    
print("Total Response Time: ", totalResponseTime)
# Calculating Average Responsetime
avgResponseTime = totalResponseTime / numRequests
#Round to 2 decimal places, more readable
avgResponseTime = round(avgResponseTime, 2)
print("Average Response Time: ", avgResponseTime)