# This script can be used the query the RestAPI of a k8s Deployment Cluster without needing to set up Postman.

import requests
import json
def main():
  accessUrl = input("Please enter the gunicorn access point URL of your deployment cluster's RESTServer: ")
  if (not accessUrl[len(accessUrl) - 1] == '/'):
    accessUrl += '/'
  if (not (accessUrl.startswith('http://') or accessUrl.startswith('https://'))):
    accessUrl = 'http://' + accessUrl
  authToken = input("Please enter the Auth Token of your RESTServer: ")
  modelName = input("Please enter the model name as shown under the Model Registry: ")
  modelVersion = input("Please enter the model version number: ")
  print("\n")
  work = input("Please enter 1 if the ride is during work hours (Mon-Fri, 8am to 5pm), enter 0 otherwise: ")
  startLat = input("Please indicate the latitude of the pickup point (between 40.550 and 40.925): ")
  startLong = input("Please indicate the longitude of the pickup point (between -73.750 and -75.250): ")
  endLat = input("Please indicate the latitude of the dropoff point (between 40.550 and 40.925): ")
  endLong = input("Please indicate the longitude of the dropoff point (between -73.750 and -75.250): ")
  miles = input("Please indicate the approx trip distance in miles: ")
  weekday = input("Please enter 1 if the trip will occur on a weekday, 0 otherwise: ")
  hour = input("Please indicate what hour of day the trip occurred (range: 0 to 23): ")

  url = accessUrl + modelName + "/" + modelVersion + "/predict?X-Auth-Token=" + authToken
  url = accessUrl + modelName + "/" + modelVersion + "/predict?X-Auth-Token=" + authToken

  payload = "{\r\n    \"use_scoring\": true,\r\n    \"scoring_args\": {\r\n        \"work\": " + work + "," \
            "\r\n        \"startstationlatitude\": " + startLat + "," \
            "\r\n        \"startstationlongitude\": " + startLong + "," \
            "\r\n        \"endstationlatitude\": " + endLat + "," \
            "\r\n        \"endstationlongitude\": " + endLong + "," \
            "\r\n        \"trip_distance\": " + miles + "," \
            "\r\n        \"weekday\": " + weekday + "," \
            "\r\n        \"hour\": " + hour + "" \
            "\r\n    }\r\n}"
  headers = {
    'X-Auth-Token': authToken,
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)


  print((json.loads(response.text)['output']).partition('\n')[0])


if __name__ == '__main__':
  main()