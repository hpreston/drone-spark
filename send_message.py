#!/usr/bin/env python
'''
This is the Python Code for a drone.io plugin to send messages using Cisco Spark
'''

import drone
import requests
import os

spark_urls = {
    "messages": "https://api.ciscospark.com/v1/messages",
    "rooms": "https://api.ciscospark.com/v1/rooms",
    "people": "https://api.ciscospark.com/v1/people"
}

drone_env = {}

spark_headers = {}
spark_headers["Content-type"] = "application/json"

def get_roomId(payload):
    '''
    Determine the roomId to send the message to.
    '''

    # If an explict roomId was provided as a varg, verify it's a valid roomId
    if ("roomId" in payload["vargs"].keys()):
        if verify_roomId(payload["vargs"]["roomId"]):
            return payload["vargs"]["roomId"]
    # If a roomName is provided, send to room with that title
    elif ("roomName" in payload["vargs"].keys()):
        # Try to find room based on room name
        response = requests.get(
            spark_urls["rooms"],
            headers = spark_headers
        )
        rooms = response.json()["items"]
        # print("Number Rooms: " + str(len(rooms)))
        for room in rooms:
            # print("Room: " + room["title"])
            if payload["vargs"]["roomName"] == room["title"]:
                return room["id"]

    # If no valid roomId could be found in the payload, raise error
    raise(LookupError("roomId can't be determined"))

def verify_roomId(roomId):
    '''
    Check if the roomId provided is valid
    '''
    url = "%s/%s" % (spark_urls["rooms"], roomId)

    response = requests.get(
        url,
        headers = spark_headers
    )

    if response.status_code == 200:
        return True
    else:
        return False

def load_drone_env_variables(payload):
    '''
    Bring in standard environment variables passed by Drone
    '''

    global drone_env

    # Fron container environment variables...
    # drone_env["DRONE"] = os.getenv("DRONE")
    # drone_env["DRONE_REPO"] = os.getenv("DRONE_REPO")
    # drone_env["DRONE_BRANCH"] = os.getenv("DRONE_BRANCH")
    # drone_env["DRONE_COMMIT"] = os.getenv("DRONE_COMMIT")
    # drone_env["DRONE_DIR"] = os.getenv("DRONE_DIR")
    # drone_env["DRONE_BUILD_NUMBER"] = os.getenv("DRONE_BUILD_NUMBER")
    # drone_env["DRONE_PULL_REQUEST"] = os.getenv("DRONE_PULL_REQUEST")
    # drone_env["DRONE_JOB_NUMBER"] = os.getenv("DRONE_JOB_NUMBER")
    # drone_env["DRONE_TAG"] = os.getenv("DRONE_TAG")
    #
    # drone_env["CI"] = os.getenv("CI")
    # drone_env["CI_NAME"] = os.getenv("CI_NAME")
    # drone_env["CI_REPO"] = os.getenv("CI_REPO")
    # drone_env["CI_BRANCH"] = os.getenv("CI_BRANCH")
    # drone_env["CI_COMMIT"] = os.getenv("CI_COMMIT")
    # drone_env["CI_BUILD_NUMBER"] = os.getenv("CI_BUILD_NUMBER")
    # drone_env["CI_PULL_REQUEST"] = os.getenv("CI_PULL_REQUEST")
    # drone_env["CI_JOB_NUMBER"] = os.getenv("CI_JOB_NUMBER")
    # drone_env["CI_BUILD_DIR"] = os.getenv("CI_BUILD_DIR")
    # drone_env["CI_BUILD_URL"] = os.getenv("CI_BUILD_URL")
    # drone_env["CI_TAG"] = os.getenv("CI_TAG")

    # From Payload
    drone_env["DRONE"] = True
    drone_env["DRONE_REPO"] = payload["repo"]["full_name"]
    drone_env["DRONE_BRANCH"] = payload["build"]["branch"]
    drone_env["DRONE_COMMIT"] = payload["build"]["commit"]
    drone_env["DRONE_DIR"] = payload["workspace"]["path"]
    drone_env["DRONE_BUILD_NUMBER"] = payload["build"]["number"]
    drone_env["DRONE_PULL_REQUEST"] = ""
    drone_env["DRONE_JOB_NUMBER"] = payload["build"]["number"]
    # drone_env["DRONE_TAG"] = payload["build"]["tag"]

    drone_env["CI"] = True
    drone_env["CI_NAME"] = "drone"
    drone_env["CI_REPO"] = payload["repo"]["full_name"]
    drone_env["CI_BRANCH"] = payload["build"]["branch"]
    drone_env["CI_COMMIT"] = payload["build"]["commit"]
    drone_env["CI_BUILD_NUMBER"] = payload["build"]["number"]
    drone_env["CI_PULL_REQUEST"] = ""
    drone_env["CI_JOB_NUMBER"] = payload["build"]["number"]
    drone_env["CI_BUILD_DIR"] = payload["workspace"]["path"]
    drone_env["CI_BUILD_URL"] = payload["repo"]["link_url"]
    # drone_env["CI_TAG"] = payload["build"]["tag"]

def message_var_exchange(message):
    '''
    Until better templating is included, rough and dirty code to
    swap $$VAR details with environment variables.
    '''

    for env in drone_env.items():
        if env[1]: message = message.replace("$" + env[0], str(env[1]))

    return message

def debug_actions(roomId, message):
    '''
    For testing
    '''

    spark_message = {
        "roomId": roomId,
        "text": "Debug: \n \n " + message
    }

    response = requests.post(
        spark_urls["messages"],
        headers=spark_headers,
        json=spark_message)

def main():
    payload = drone.plugin.get_input()
    vargs = payload["vargs"]

    # Pull in Drone Environment Variables
    load_drone_env_variables(payload)
    # Replace any $VAR references in the message
    vargs["message"] = message_var_exchange(vargs["message"])

    # Prepare headers and message objects
    spark_headers["Authorization"] = "Bearer %s" % (vargs["auth_token"])
    spark_message = {}


    # Determine destination for message
    try:
        # First look for a valid roomId or roomName
        roomId = get_roomId(payload)
        spark_message["roomId"] = roomId
    except LookupError:
        # See if a personEmail was provided
        if "personEmail" in vargs.keys():
            spark_message["toPersonEmail"] = vargs["personEmail"]
        else:
            raise(LookupError("Requires valid roomId, roomName, or personEmail to be provided.  "))

    # Debug payload
    # debug_actions(roomId, str(payload))
    #
    debug_message = {
        "roomId": roomId,
        "text": "Debug: \n \n " + str(payload)
    }

    response = requests.post(
        spark_urls["messages"],
        headers=spark_headers,
        json=debug_message)

    spark_message["markdown"] = vargs["message"]
    # print(spark_message)

    # Send message through Spark
    response = requests.post(
        spark_urls["messages"],
        headers = spark_headers,
        json = spark_message)
    # print(response.json())
    # print(str(response.status_code))

    # If the message posting didn't work correctly...
    if response.status_code != 200:
        print(response.json()["message"])
        raise(SystemExit("Something went wrong..."))


if __name__ == "__main__":
    main()

