# Build and run

Steps to run this program are as follows:
```
1. git clone <link to this repository>
2. pip install -r requirements.txt
3. python main.py
```
The code is developed and tested on Python 3.7.3

# API Documentation

These APIs have been generated based on the details provided in the base classes i.e., `user_base.py`, `team_base.py` and `project_board_base.py`

## Users

1. **POST /user/**
   - Takes JSON input in POST request with parameters `name` and `display_name`
   - Example: `{"name": "john",
    "display_name": "john doe"}`
   - Adds a user to the database and returns its id of the form `{"id": 1656836811}`
2. **GET /user/**
   - A GET request on this endpoint returns a list of current users
   - Example:
```json
[
    {
        "creation_time": "Sun, 03 Jul 2022 13:56:17 GMT",
        "display_name": "iron man",
        "name": "tony stark"
    },
    {
        "creation_time": "Sun, 03 Jul 2022 13:56:37 GMT",
        "display_name": "john doe",
        "name": "john"
    }
]
```
3. **POST /user/describe**
   - A POST request with body containing the user id, like `{"id": 1656836777}`
   - Returns a description of the user, indicating which teams the user admins, which teams they are a part of, and their assigned tasks.
   - Example:
```json
{
    "creation_time": "Sun, 03 Jul 2022 13:56:17 GMT",
    "description": "Name=tony stark, admins=[], teams=[], tasks=[]",
    "name": "tony stark"
}
```
4. **POST /user/update**
   - Request body is of the form `{"id": "<user_id>", "user": {"name": "<user_name>", "display_name": "<display name>"}}`
   - Updates the user for the specified ID
5. **POST /teams**
   - POST request is made with body containing the user id, like `{"id": 1656836777}`
   - Returns the list of teams the user is a part of
```json
[
    {
        "creation_time": "Sun, 03 Jul 2022 14:54:02 GMT",
        "description": "Earth's greatest heroes",
        "name": "The Avengers"
    }
]
```

## Teams

1. **POST /team/**
   - JSON request body is sent, containing `{"name": "<team_name>", "description": "<some description>", "admin": "<id of a user>"}`
   - A new team is created and the team id is returned as
```json
{
    "id": 1656840242
}
```
2. **GET /team/**
   - A GET request sent on this endpoint returns a list of teams with their admin user, creation time, name, and description.
   - Example:
```json
[
    {
        "admin": 1656836777,
        "creation_time": "Sun, 03 Jul 2022 14:54:02 GMT",
        "description": "Earth's Heroes",
        "name": "Avengers"
    },
    {
        "admin": 1656836797,
        "creation_time": "Sun, 03 Jul 2022 14:56:18 GMT",
        "description": "Earth's Hackers",
        "name": "Anonymous"
    }
]
```
3. **POST /team/describe**
   - The team id is sent in the POST request body here like `{"id": 1656840242}`
   - A description of that specific team is received in response
   - Example:
```json
{
    "admin": 1656836777,
    "creation_time": "Sun, 03 Jul 2022 14:54:02 GMT",
    "description": "Earth's Heroes",
    "name": "Avengers"
}
```
4. **POST /team/update**
   - Request body is of the form `{"id": "<team_id>", "team": {"name": "<team_name>", "description": "<team_description>", "admin": "<id of a user>"}}`
   - Updates the specified team details
5. **POST /team/add_users**
   - Takes a POST request body in the form `{"id": "<team_id>", "users": ["user_id 1", "user_id2", ..]}`
   - Adds the mentioned users into the specified team
6. **POST /team/remove_users**
   - Takes a POST request body in the form `{"id": "<team_id>", "users": ["user_id 1", "user_id2", ..]}`
   - Removes the mentioned users from the specified team
7. **POST /team/users**
   - The team id is sent in the request body
   - A list of users is returned who are in the team
```json
[
    {
        "display_name": "iron man",
        "id": 1656836777,
        "name": "tony stark"
    },
    {
        "display_name": "captain america",
        "id": 1656836811,
        "name": "steve rogers"
    }
]
```

## Boards

1. **POST /board/**
   - Takes a request in the form `{"name": "<board_name>", "description": "<description>", "team_id": "<team id>"}`
   - Returns a JSON string in response with id of board created
2. **POST /board/close**
   - Takes a board id in the request like `{"id": 1656842467}`
   - Attempts to close a board if all tasks are completed, otherwise returns `"There are incomplete tasks on this board!"`
3. **POST /board/add_task**
   - Task details are POSTed for a particular board
   - We receive the task id in response
   - Request data is of the following form, where id indicates board_id
```json
{
    "id": 1656842467,
    "user_id": 1656836777,
    "title": "Collect the mind stone",
    "description": "Defeat Loki and take the mind stone back"
}
```
4. **POST /board/update_task**
   - Request body JSON contains task `id` and new `status`
   - The corresponding task is then updated
5. **POST /board/list**
   - Takes a team `id` in the JSON request body
   - Returns a list of boards assigned to a team
```json
[
    {
        "id": 1656842467,
        "name": "defeat thanos"
    }
]
```
6. **POST /board/export**
   - Receives a board `id` in the request body
   - Responds with the txt file generated, which displays the current board details
<details>
<summary>Click to view output</summary>

```

                         DEFEAT THANOS                          

ID = 1656842467
Created on 2022-07-03 15:31:07.135022

collect the infinity stones

Belongs to team: The Avengers
Admin: tony stark

                       BOARD STATUS: OPEN                       

---------- OPEN TASKS ----------

[ ] Collect the time stone
	- Steal the time stone from doctor strange
	- Assigned to: tony stark

------ IN_PROGRESS TASKS -------

[o] Collect the space stone
	- Defeat galactic villain and retrieve the space stone
	- Assigned to: steve rogers

------- COMPLETED TASKS --------

[X] Collect the mind stone
	- Defeat Loki and take the mind stone back
	- Assigned to: tony stark

1 out of 3 tasks are completed
```
</details>

# Thought Process & Design Decisions

- Although APIs for this particular project could have been developed with pure Python, given that this assignment was for a Python engineer with backend development I chose to build web APIs with the help of Flask library
- I have tried my best to match the base abstract classes which were given, and to have the input and output match the conditions that were specified
- I have tried to add RESTful APIs wherever it was appropriate to add them. However, the given task's API constraints resulted in input conditions not matching the required methodology. Given additional time I'm sure the functions could be modified to match this criteria as well
- I have worked with the assumption that this is a single-threaded application which will be run directly by one end user, who will interact with the API and give commands one after the other and not concurrently
- Given the above, I have made use of the UNIX timestamp for the  ID values in user, team, board and task
- The database used for this application is sqlite, since it is a lightweight and in-built database with local file storage 

## Future Improvements

- There is scope for better error handling in this program. I have utilized the `abort()` function provided by Flask to redirect/exit with 400 and 500 error codes in case of exceptions or incorrent requests. There can be a better request parsing and response to exceptions that can be developed
- 