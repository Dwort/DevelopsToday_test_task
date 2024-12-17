# **DevelopsToday**
## **TestTask**

### Description:
It's a test task realized on DRF (Django Rest Framework). I implemented all API requests that were necessary.
As SQL DB, I used a PostgreSQL (in docker, as Docker Image). All endpoints I describe below. And I left the examples of bodies for endpoints in the code. 

### How to run the project:

```
docker compose build

docker compose up 

docker-compose run app python manage.py makemigrations 

docker-compose run app python manage.py migrate
```

### API Endpoints (Test using Postman or Web):

#### API Endpoints (cats actions):
```
api/add_cat/ - Creating a new cat agent
api/all_cats/ - Get a list of all cats
api/cat/<int:cat_id>/ - CRUD operations for cat.
                          - Update salary.
                          - Get current cat by id.
                          - Delete cat.
```

#### API Endpoints (mission/target actions):

```
api/mission/create/ - Create a mission and targets.
api/mission/all/ - Get a list of all missions and targets.
api/mission/<int:mission_id>/ - CRUD operations for missions.
                                  - Get current mission by id.
                                  - Delete mission.
api/mission/assign/ - Assign a cat to mission without an executor.
api/mission/target/mark/<int:target_id>/?mark=True - Update target mark. (Completed or not - True or False)
api/mission/target/notes/<int:target_id>/ - Update target notes.
```