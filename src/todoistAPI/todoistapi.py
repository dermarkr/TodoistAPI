import datetime
import requests
import json
import logging
import sys

from src.todoistAPI.utils import convert_time


class TodoistAPI:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.todoist_api_url = "https://api.todoist.com/sync/v9/"
        self.api_header = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        pass

    def sync_call(self, resources: list = None) -> dict:
        """
        Makes an API call and returns the resources passed in
        If nothing is passed in returns all resources
        """

        if resources is None:
            resources = list()

        url = self.todoist_api_url + "sync"

        data = 'sync_token=*&resource_types='

        if not resources:
            data += "[\"all\"]"
        else:
            data += "["
            for resource in resources:
                data += "\"{}\", ".format(resource)

            data = data[:-2]
            data += "]"

        logging.debug("data for url call '{}'".format(data))

        response = requests.post(url, headers=self.api_header, data=data)

        if response.status_code == 200:
            logging.info("Returning List of Projects")
            return response.json()
        else:
            logging.error(
                "A {} error was encountered when trying to connect to todoist".format(
                    response.status_code
                )
            )
            sys.exit()

    def get_project_info(self, project_id: str) -> dict:
        """
        Makes an API call to get all the information for the project
        This incudes all the open tasks
        https://developer.todoist.com/sync/v9/#get-project-data
        """
        data = {"project_id": project_id}

        url = self.todoist_api_url + "projects/get"

        response = requests.post(url, headers=self.api_header, data=data)

        if response.status_code == 200:
            logging.info(
                "Returning List of Items in Project with id {}".format(project_id)
            )
            return response.json()
        else:
            logging.error(
                "A {} error was encountered when trying to connect to todoist".format(
                    response.status_code
                )
            )
            sys.exit()

    def get_project_data(self, project_id: str) -> dict:
        """
        Makes an API call to get all the information for the project
        This incudes all the open tasks
        https://developer.todoist.com/sync/v9/#get-project-data
        """
        data = {"project_id": project_id}

        url = self.todoist_api_url + "projects/get_data"

        response = requests.post(url, headers=self.api_header, data=data)

        if response.status_code == 200:
            logging.info(
                "Returning List of Items in Project with id {}".format(project_id)
            )
            return response.json()
        else:
            logging.error(
                "A {} error was encountered when trying to connect to todoist".format(
                    response.status_code
                )
            )
            sys.exit()

    def get_closed_tasks(self, **kwargs) -> dict:
        """
        Makes an API call to get closed tasks based on provided filters
        https://developer.todoist.com/sync/v9/#get-all-completed-items
        """

        data = dict()

        for key, value in kwargs.items():
            data[key] = value

        url = self.todoist_api_url + "completed/get_all"

        response = requests.post(url, headers=self.api_header, data=data)

        if response.status_code == 200:
            logging.info("Returning List of Closed Items based on filters".format(data))
            return response.json()
        else:
            logging.error(
                "A {} error was encountered when trying to connect to todoist".format(
                    response.status_code
                )
            )
            sys.exit()

    def get_item_info(self, item_id: int) -> dict:
        """
        Returns detailed information item including notes and the project details
        """

        logging.info("Making Item Info API call for item {}".format(item_id))

        data = {"item_id": int(item_id)}

        url = "https://api.todoist.com/sync/v9/items/get"

        response = requests.post(url, headers=self.api_header, data=data)

        if response.status_code == 200:
            logging.info("Returning detailed information on Item id {}".format(data))
            return response.json()
        else:
            logging.error(
                "A {} error was encountered when trying to connect to todoist".format(
                    response.status_code
                )
            )
            sys.exit()

    def get_archived_items(self, **kwargs) -> dict:
        """
        Gets detailed information on archived items (up to 20 items at a time)
        https://developer.todoist.com/sync/v9/#get-completed-items
        """
        logging.info("Fetting archived items with APIcall using '{}'".format(kwargs))
        needed_ids = ["project_id", "section_id", "task_id"]
        task_id = None
        data = dict()
        for key, value in kwargs.items():
            data[key] = value

            if key in needed_ids:
                task_id = (key, value)

        if not task_id:
            logging.error("Missing id for archived item")
            exit()

        url = self.todoist_api_url + "archive/items?{}={}".format(task_id[0], task_id[1])

        logging.info(url)

        response = requests.post(url, headers=self.api_header, data=data)

        if response.status_code == 200:
            logging.info("Returning List of Closed Items based on filters".format(data))
            return response.json()
        else:
            logging.error(
                "A {} error was encountered when trying to connect to todoist".format(
                    response.status_code
                )
            )
            sys.exit()

    def get_archived_items_parents(self, **kwargs) -> dict:
        """
        Gets detailed information on archived items (up to 20 items at a time)
        https://developer.todoist.com/sync/v9/#get-completed-items-with-a-list-of-parent-ids
        """
        logging.info("Fetting archived items with APIcall using '{}'".format(kwargs))

        data = dict()
        for key, value in kwargs.items():
            data[key] = value
        url = self.todoist_api_url + "archive/items_many?parent_ids={}".format(json.dumps(kwargs["ids"]))

        print(url)

        logging.info(url)

        response = requests.post(url, headers=self.api_header, data=data)

        if response.status_code == 200:
            logging.info("Returning List of Closed Items based on filters".format(data))
            return response.json()
        else:
            logging.error(
                "A {} error was encountered when trying to connect to todoist".format(
                    response.status_code
                )
            )
            sys.exit()    

    def get_all_archived(
        self, start_time: datetime.datetime, user_timezone: str, **kwargs
    ) -> dict:
        """
        Goes through pages with the get_archived_items until the start_time is hit
        """

        logging.info(
            "Getting all archived items since '{start_time}' with args '{kwargs}'".format(
                start_time=start_time, kwargs=kwargs
            )
        )
        archived = {"items": list(), "completed_info": list(), "total": 0}

        archived_return = self.get_archived_items(**kwargs)

        def _add_items_and_check_expired(items: list):
            archived_items = list()
            passed_start_time = False

            for item in items:
                logging.debug("Checking item for expiry: '{}'".format(item.keys()))
                # if not "complete_at" in item or not item["completed_at"]:
                #     continue
                completed_time = convert_time(
                    item["completed_at"], user_timezone=user_timezone
                )
                logging.debug(
                    "Task completed time is '{}' converted to '{}'. Compare to start time '{}'".format(
                        item["completed_at"], completed_time, start_time
                    )
                )

                if completed_time >= start_time:
                    archived_items.append(item)
                else:
                    passed_start_time = True
                    break

            return archived_items, passed_start_time

        checked_archived, passed_start = _add_items_and_check_expired(
            items=archived_return["items"]
        )

        archived["items"].extend(checked_archived)
        archived["completed_info"].extend(archived_return["completed_info"])
        archived["total"] += archived_return["total"]

        # logging.info("has_more '{}' passed_start")

        while archived_return["has_more"] and not passed_start:
            logging.info("Getting more archived items with page id '{}'".format(archived_return["next_cursor"]))
            
            kwargs["next_cursor"] = archived_return["next_cursor"]
            temp = self.get_archived_items(**kwargs)

            print(temp["next_cursor"])

            checked_archived, passed_start = _add_items_and_check_expired(
                items=archived_return["items"]
            )

            archived["items"].extend(checked_archived)
            archived["completed_info"].extend(archived_return["completed_info"])
            archived["total"] += archived_return["total"]

            has_more = archived_return["has_more"]

            logging.info(has_more)
        return archived

    def get_user_info(self) -> dict:
        """
        Makes an API call and returns user info from todoist
        """

        url = self.todoist_api_url + "sync"

        data = 'sync_token=*&resource_types=["user"]'

        response = requests.post(url, headers=self.api_header, data=data)

        if response.status_code == 200:
            logging.info("Returning User info")
            return response.json()
        else:
            logging.error(
                "A {} error was encountered when trying to connect to todoist".format(
                    response.status_code
                )
            )
            sys.exit()
