## Table of Contents

This file is just to add notes and background about the technologies used in this repo

<!-- TOC -->

* [Table of Contents](#table-of-contents)
* [Project Roadmap](#project-roadmap)
* [To learn](#to-learn)
* [FastAPI](#fastapi)
* [SQLAlchemy](#sqlalchemy)
* [API/HTTP Request Methods](#apihttp-request-methods)
    * [HTTP POST request](#http-post-request)
    * [HTTP GET request](#http-get-request)
    * [HTTP PUT request](#http-put-request)
    * [HTTP HEAD request](#http-head-request)
    * [HTTP PATCH request](#http-patch-request)
    * [HTTP DELETE request](#http-delete-request)
* [YAML](#yaml)
    * [What it tries to solve](#what-it-tries-to-solve)
    * [Rules](#rules)
* [Docker](#docker)
    * [Concepts](#concepts)
    * [Dockerfile vs. docker-compose](#dockerfile-vs-docker-compose)
        * [Dockerfile](#dockerfile)
        * [docker-compose](#docker-compose)
    * [For my app](#for-my-app)
        * [1. Create a Dockerfile](#1-create-a-dockerfile)
        * [2. Create the docker-compose.yaml](#2-create-the-docker-composeyaml)
        * [3. Start up the container](#3-start-up-the-container)
* [Testing](#testing)
* [Logging](#logging)
    * [Important: Use a custom logger class](#important-use-a-custom-logger-class)
* [Data load](#data-load)
    * [Validations:](#validations)
* [General: What to set up for blank project](#general-what-to-set-up-for-blank-project)
* [Now for the specific project](#now-for-the-specific-project)
    * [2. Create new project in PyCharm](#2-create-new-project-in-pycharm)
    * [3. Basic set up in PyCharm](#3-basic-set-up-in-pycharm)
        * [3.n. Create models](#3n-create-models)
        * [3.n. Database](#3n-database)

<!-- TOC -->

## Project Roadmap

<details open>

- [x] Set up DB
- [x] First endpoint to add users
- [x] Dockerize my API
    - [x] Use `requirements.txt`
- [x] Connect to cloud SQL (Azure)
- [ ] Add automated testing
    - [ ] Unit tests
    - [x] Feature tests (Cucumber / Gherkin)
- [x] Enrich add users endpoint to
  optionally [include skills](https://fastapi.tiangolo.com/tutorial/sql-databases/#__tabbed_1_3)
- [x] Add logging
- [x] Feature: load data from
    - [ ] A CSV file
        - [ ] Class to read CSV's
        - [ ] Optional/TBD: Automated uploader
    - [ ] Others? (TBD)
- [ ] Feature: upload files (Cover letters/Resumes)
- [ ] Feature: Create stuff from templates (TBD, the Consumer might a better place for it)
- [ ] Add endpoint to PULL data from the DB
- [ ] Kubernetize my API
- [ ] Basic Kafka
    - [ ] Produce messages from the API
    - [ ] Consume messages
- [ ] Consumer
    - [ ] Validate incoming messages
    - [ ] Enrich data using the API (if applicable)
    - [ ] Create and store PDF's based on templates
- [ ] Break the API and the Kafka consumer into separate projects
- [ ] Implement secure Kafka
- [ ] Put this in the cloud
    - [ ] Is there a free version of Azure/GCP/etc ? (maybe RedHat?)
    - [ ] Put K8S modules in the cloud
    - [ ] Move the MySQL DB to the cloud
    - [ ] Store PDF documents in the cloud
    - [ ] Store templates (HTML?) in the cloud

</details>

## To learn

<details>

- [ ] Check exactly what FastAPI is
- [ ] How does FastAPI compares to other solutions
- [ ] What exactly is `uvicorn`? is it just for Dev? is it only for FastAPI?
- [ ] WSGI vs ASGI
- [ ] Learn about API keys
- [ ] Learn about pydantic and other alternatives
- [ ] Also learn about GraphQL
    - [ ] How does it compare to REST for ease of implementation?
    - [ ] How does it compare to REST in other areas (e.g. performance)
- [x] Add/use `requirements.txt` in my application
- [ ] What is the `__init__.py` (in the Python package folder) used for?
- [ ] Flask vs Uvicorn
- [ ] Learn what each section of `docker-compose.yaml` does
- [x] `yield` vs `return`
- [x] What is `sqllite` exactly? Is it good for local testing?

</details>

## FastAPI

<details>

- it is a framework to build RESTful API's
- It uses Pydantic intrinsically to validate, serialize and deserialize data
    - Pydantic is a data validation library for Python.
    - Pydantic is among the fastest data validation libraries for Python.
    - Pydantic provides type hints for schema validation and serialization through type annotations.
- Starlette
    - is a lightweight ASGI framework/toolkit, to support async functionality in Python.
    - great performance by independent benchmarks, which is inherited by FastAPI.
- Uvicorn
    - Uvicorn is a minimal low-level server/application web server for async frameworks
    - following the ASGI specification
- Automatically generate OpenAPI documentation
- Can run on Gunicorn (WSGI) and ASGI servers such as Uvicorn and Hypercorn, making it a good choice for production
  environments

</details>

## SQLAlchemy

<details>

- `declarative_base()` is a factory function that constructs a base class for declarative class definitions (which is
  assigned to the Base variable)
- The Declarative system is the typically used system provided by the SQLAlchemy ORM in order to define classes mapped
  to relational database tables.
    - However, as noted in Classical Mappings, Declarative is in fact a series of extensions that ride on top of the
      SQLAlchemy mapper() construct.
- To link a pydantic model to a SQLAlchemy model (table) we declare an inner `Config` class inside the pydantic model
    - In the `Config` class We set the value `orm_mode = True` to let pydantic know this is an ORM (duh!)
    - Pydantic's `orm_mode` will tell the Pydantic model to read the data even if it is not a dict, but an ORM model
    - This way, instead of only trying to get the id value from a dict, as in `id = data["id"]` it will also
      try `id = data.id`
- SQLAlchemy and many others are by default "lazy loading".
    - That means, they don't fetch the data for relationships (e.g. `User`-->`Skill`) unless you try to access the
      attribute that would contain that data.
    -

</details>

## API/HTTP Request Methods

<details>

These are the basic ones, see below for further reference:

- [https://www.freecodecamp.org/news/http-request-methods-explained/]
- [https://www.w3schools.com/tags/ref_httpmethods.asp]

### HTTP POST request

- We use POST to create a new resource.
- A POST request requires a body in which you define the data of the entity to be created.
- A successful POST request would be a 200 response code.
- No restrictions on data length

### HTTP GET request

- We use GET to read or retrieve a resource.
- A successful GET returns a response containing the information you requested.
- **Data sent is visible as part of the URL**
- should never be used when dealing with sensitive data

### HTTP PUT request

- We use PUT to modify (`insert`/`update`) a resource.
- PUT updates the entire resource with data that is passed in the body payload.
- If there is no resource that matches the request, it will create a new resource.
- It is idempotent: calling the same PUT request multiple times will always produce the same result. In contrast,
  calling a POST request repeatedly have side effects of creating the same resource multiple times.

### HTTP HEAD request

- HEAD is almost identical to GET, but without the response body.
- In other words, if GET /users returns a list of users, then HEAD /users will make the same request but will not return
  the list of users.
- useful for checking what a GET request will return before actually making a GET request
    - a HEAD request can read the Content-Length header to check the size of the file, without actually downloading the
      file.

### HTTP PATCH request

- We use PATCH to modify a part of a resource.
- With PATCH, you only need to pass in the data that you want to update.

### HTTP DELETE request

- It is used to, well.... delete data

</details>

## YAML

<details>

### What it tries to solve

- Set of standards to transfer data regardless of language (Python, Java, etc)
- Competes with JSON and XML, but simpler (in theory)

### Rules

```yaml
# This is a comment
# In general, lowercase is encouraged
# YAML is simply a key:value pair
course:
  # Notice the indentation for sub-elements!
  course_name: "Python rules"
  course_name2: Python rules # No quotes is still acceptable
  version: 1.1
  year: 2023
  price: &price 1000  # Notice the ampersand!! this indicates a re-usable variable
  is_public: true
  release_date: 2023-12-15 14:09:00 # Notice ISO-ish
  pre-enroll: null # null isused for ... well, nulls
  tags: # This is one way to declare an array (notice indentation + dashes)
    - python
    - web development
    - mysql
  teachers: [ "hugo", "paco", "luis" ]  # Another way for an array
  # Notice the following syntax, it declares an array of objects (compare to JSON [{},{}] )
  teacher_details:
    - name: "hugo"
      email: "hugo@gmail.com"
      role: "admin"
    - name: "paco"
      email: "paco@gmail.com"
      role: "servant"
    # Yet another way to write objects / dicts
    - { name: "luis",email: "luis@gmail.com",role: "runner" }
  short_desc: > # This is a multi-line string, when read, tabs and line breaks are removed
    mi mama
    me mima mucho
  long_desc: | # Another multiline but all indentation and linebreaks are KEPT
    mi mama
      me mima mucho
  process_payment: *price  # Notice the reference to the variable we declared above ^^
  parent_var: &parent # Again, declaring a variable
    one: two
  child_var:
    three: four
    <<: *parent  # This includes all sub-elements in parent, in the child variable 

```

</details>

## Docker

<details>

### Concepts

- dockerfile
    - blueprint for building images
        - more like a set of instructions IMO
- image
    - template for running containers
- container
    - The actual running code

### Dockerfile vs. docker-compose

- A `Dockerfile` describes how to build a Docker **image**, while Docker Compose is a command for running a Docker
  **container**.
- `docker-compose` is a tool for defining and running multi-container applications
- Use a Dockerfile to **define** your app’s environment, so it can be reproduced anywhere.
- Define the services of your app in docker-compose.yml, so you can run them together in an isolated environment.
- Use `docker compose up` and `docker compose command` to start and run your entire app.

#### Dockerfile

- Uses docker build commands, which use a “context,”
- Context: the set of files located in the specified PATH or URL
- The build process can refer to any of the files in the context
- the URL parameter can refer to
    - Git repositories,
    - pre-packaged tarball contexts
    - or plain text files
- A Docker image consists of read-only layers, each of which represents a Dockerfile instruction.
- The layers are stacked and each one is a delta of the changes from the previous layer
- In the following Example
    - FROM creates a layer from the ubuntu:18.04 Docker image.
    - COPY adds files from your Docker client’s current directory.
    - RUN builds your application with make.
    - CMD specifies what command to run within the container.

```dockerfile
FROM ubuntu:18.04
COPY . /app
RUN make /app
CMD python /app/app.py
```

- Trivia: you can have multiple `FROM` sections to pull assorted functionality from different places:

```dockerfile
FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y odbcinst
RUN apt install -y unixodbc-dev
RUN apt-get install -y unixodbc

FROM Python:3.11
COPY . /app
RUN make /app
CMD python /app/app.py
```

- `requirements.txt`
    - You can make this one generic, i.e. don't specify a version, let `pip` decide

#### docker-compose

- "Adds" a new **writable** layer on top of the image
- All changes made to the running container, such as writing/modifying/deleting files, are done in this writable
  container layer

### For my app

#### 1. Create a Dockerfile

Remember: this is about creating the **image**

```dockerfile
# We copy the kernel functionality here. I'm using Python but it can be Devian, Ubuntu, ETC
FROM python:3.11

# Name the working dir
WORKDIR /app

# Copy "local" files to the container (in the `/app` folder)
# Sample:
COPY ./api/ ./api/
COPY ./requirements.txt .

# Install requirements in the container
RUN pip install --upgrade pip
# PRE-REQUISITE: Don't forget to refresh your requirements by doing : `pip freeze > requirements.txt`
RUN pip install -r ./requirements.txt
```

#### 2. Create the docker-compose.yaml

Note how you could spin up multiple container (in different ports) for escalabitily here

```yaml
version: "3"
services:
  # each service that could be executed from docker-compose goes here
  # note that the name can be anything (I just named it api)
  api:
    build: . # # config to build my image goes here... maybe? TODO: Investigate further
    expose:
      - 8000
    ports: # Port for my API
      - "8000:8000"
    restart: "always"
```

#### 3. Start up the container

```commandline
docker-compose up api
```

</details>

## Testing

<details>

- `pytest` provides unit testing
- BDD
    - Two options: `pytest-bdd` or `behave`
    - In theory `behave` is more flexible (e.g. file and method conventions) and easier, so that's what I'm running with
- pytest fixtures are used for dependency injection and app state
    - They will NOT be used in this project (using FastAPI dependency overrides instead)
- Override DB connection and test endpoints locally
    - Regular flow (prod/dev):
        1. engine is created by connecting to the URL (`database.py`)
        2. A `SessionLocal` is created based on the engine (`database.py`)
        3. The `Base` (`declarative_base`) is created here to add our ORM models to
        4. `app = FastAPI()` creates our API (`endpoints.py`)
        5. A method `get_session()` yields the `SessionLocal`. **Important**, this is where the magic happens
        6. In our `app` (for each endpoint) we introduce a dependency to the
           `session` (`add_users(model: UserModel, session: Session = Depends(get_session))`)
        7. The `session` gets passed down to the DAO for database usage
    - For tests, we need to override using fixtures (test file, UT or `steps.py`:
        1. We import `app` and `get_session` from our `endpoints.py` file, and the `Base` from `database.py`
        2. We create a "shadow" engine and session, connecting to the dummy DB
        3. We create a test version of `get_session()` (See step `e.` previously)
        4. Just to be sure, let's drop and re-create our tables: `Base.metadata.drop_all(engine)`
        5. Now re-create our ORM models in testing: `Base.metadata.create_all(bind=engine)`
        6. Super cool: we override the session like so: `app.dependency_overrides[get_session] = override_get_session`
        7. We leverage `TestClient` from FastAPI to create a testable version of our API: `client = TestClient(app)`
        8. And now we are ready to implement our tests: `response = client.get("/endpointName/")`
- Pro-tip: You can do ste-by-step debugging by using PyCharm's integrated FastAPI Run/Debug configuration

No more mocking the logger, check this out this beauty of code to check the logs!:

```python
class TestDataUpload(TestCase):
    def test_partially_correct_data(self):
        with self.assertLogs() as check_log:
            parser = CsvParser()
            result = parser.upload("/app/tests/data/partiallyCorrectUpload.csv")
            self.assertFalse(result)
            log_text = str(check_log.output)
            self.assertIn("Error in Row 1: missing email", log_text)
            self.assertIn("Error in Row 3: skill level must be numeric", log_text)
```

</details> <!-- Testing -->

## Logging

<details>

- no need for any installs, just `import logging`
- Remember the default level is WARNING, if you want INFO's you'll have to configure it
    - simply do `logging.basicConfig(level.logging.DEBUG)`
- to log to a file: `logging.basicConfig(filename='MyFile.log', level.logging.DEBUG)`
- Formatting:
    - [Reference](https://docs.python.org/3/library/logging.html#logrecord-attributes)
    - `logging.basicConfig(filename='MyFile.log', level.logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')`
- Default logger is the `root` logger, which we may want to avoid for complex apps
    - The first config is the one that takes over, hence, confusion
- A logger will help us create a logger per class/module, etc: `logger=logging.getLogger(__name__)`
    - `name` is of course the name of the method invoking
- IMPORTANT: difference between `logger.error()` and `logger.exception()` is that `exception()` gives the stacktrace

```python
import sys
import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('myLoggingFile.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)

"""
Option B: One handler per log level. You can have as many as you want 
"""
error_handler = logging.FileHandler('onlyErrors.log')
error_handler.formatter = formatter
error_handler.setLevel(logging.ERROR)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
console_handler.level = logging.DEBUG

# We add all our handlers here
logger.addHandler(file_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)


class MyStuff:
    def my_method(self):
        try:
        # do some logic
        except Exception as ex:
            logger.error(ex.message())
```

### Important: Use a custom logger class

Originally I had set up a custom logging functionality as a stand-alone function, but for some reason it wasn't working
on FastAPI:

```python
### FILE: utilities.py
def get_logger():
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(DEFAULT_LOG_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger


### FILE: endpoints.py
from common.utilities import get_logger

app = FastAPI()
logger = get_logger()
```

So, now I moved that into a class and I create an instance of that class, not sure why this DOES work, maybe because I'm
adding state to my logger?

```python
### FILE: utilities.py
class DefaultLogger:
    """
    Having a class is a bit convoluted, but necessary since logging kept failing when I initialized
    the log from endpoints.py without a wrapper class. My theory is that this happened because I needed to add state
    """

    def __init__(self):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(DEFAULT_LOG_FORMAT)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

    def get_logger(self) -> Logger:
        return self.logger


### FILE: endpoints.py
from common.utilities import DefaultLogger

app = FastAPI()
logger = DefaultLogger().get_logger()
```

</details> <!-- Logging -->

## Data load

<details>

- CSV: There are 2 main data loaders for Python
    - Pandas
        - Data manipulation and analysis
        - It is cool to slice and dice data
        - "offers data structures and operations for manipulating numerical tables and time series"
        - Pros
            - Good for complex analysis and mathematical stuff
        - Cons
            - It is a heavy framework
            - Puts the whole data in memory
    - CSV (just like that: `import csv`)
        - It has CSV-specific functionality (duh!)
        - Better if you have simple needs
        - Pros
            - Much lighter than pandas
        - Cons
            - Not good if you need more complex functionality
- CSV module (ditching pandas for the time being)
    - no need for `pip install`

### Validations:

- Leverage pydantic, it has a cool array of validation functions, check the following code
- NOTE: there is a deprecated `from pydantic import validator`, be careful to use `field_validator`
- IMPORTANT: seems like some pydantic validators require their own package: `pip install pydantic[email]`

```python
import re
from pydantic import BaseModel, EmailStr, field_validator


class UserModel(BaseModel):
    email: EmailStr  # Built-in validation
    phone: str
    name: str
    title: str

    @classmethod
    @field_validator("phone")
    def validate_phone(cls, value: str):  # Custom validation
        pattern = "^(\\+\\d+)?(\\(\\d+\\))?\\s*[\\d-]+$"
        # Even though we use assert, this should throw a ValidationError
        assert re.match(pattern=pattern, string=value), "Phone doesn't match expected pattern"
        return value

    @classmethod
    @field_validator("name", "title")  # <== Check this, you can add validations for multiple fields
    def validate_alphanums(cls, value: str) -> str:
        pattern = "^[a-zA-Z\\s]+"
        # Even though we use assert, this should throw a ValidationError
        assert re.match(pattern=pattern, string=value), "Phone doesn't match expected pattern"
        return value
```

</details> <!-- Data load -->

## General: What to set up for blank project

<details>
<summary>Expand for details</summary>

<details>
<summary>Preparation Checklist</summary>

- [ ] Create a new repo from [template](https://github.com/jorge-cardenas-salas/template) ahead of time
    - [Instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
- [ ] Configure PyCharm
    - Set interpreter
    - Set FastAPI Debug config
    - Set unit test run config
    - Set feature test run config
    - Make sure the project works from the command line
- [x] See if all of the above can
  be [saved to github](https://www.jetbrains.com/help/pycharm/sharing-project-settings.html)
- [x] Determine the minimum viable product "frame"
    - Database connection
    - API
    - Unit tests
    - Logging
    - Models / logic
    - Data load
- [ ] Implement the minimum viable frame into this project
- [ ] Practice creating at least 4 blank projects "by hand"
- [ ] Do at least 4 exercises from scratch
    - [ ] Ideally, ask community for peer review
- [ ] Create slides for personal presentation and portfolio

</details> <!-- Preparation Checklist -->

<details>
<summary>Basic (blank) set up</summary>

**_Make sure the DB is up and running_**

**IMPORTANT**: Consider creating a script for it

1. From Windows, open `Services`
2. Look for `MySQLServer`
3. Hit `Start`

</details> <!-- Database -->

<details>
<summary>Create basic folder structure</summary>

**NOTE**: _italics_ mean folder, `code` means file

- _api_
    - `endpoints.py`
- _common_
    - _database_
        - _daos_
            - `dao.py`
        - _row_models_
            - `row_models.py`
        - `database.py`
    - _models_
    - `constants.py`
    - `utilities.py`
- _data_upload_
    - `csv_parser.py`
    - `other_file_type_parser.py`
- _tests_
    - _unit_
    - _feature_
        - _steps_
            - `steps.py`
- _data_upload_
    - `csv_parser.py`
    - `other_parser.py`
- `Dockerfile`
- `docker-compose.yaml`
- `README.md`
- `requirements.txt`

</details> <!-- Basic structure -->

<details>
<summary>Environment/Config</summary>

- Update `.env` file

</details>
<details>
<summary>Add requirements</summary>

```commandline
pip freeze > requirements.txt
```

Alternatively, you can leave your requirements as open as possible and let Docker figure out versioning:

```requirements
fastapi
sqlalchemy
pydantic
pytest
behave
requests
uvicorn
mssql
sqlserver
pyodbc
starlette.testclient
httpx
python-dotenv
```

</details> <!-- Requirements -->

<details>
<summary>Utilities</summary>

- Create a `DefaultLogger`

```python
class DefaultLogger:
    """
    Having a class is a bit convoluted, but necessary since logging kept failing when I initialized
    the log from endpoints.py without a wrapper class. My theory is that this happened because I needed to add state
    """

    def __init__(
            self,
            logger_name: Optional[str] = PROJECT_NAME,
            use_file: Optional[bool] = False,
            filename: Optional[str] = ""
    ):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(DEFAULT_LOG_FORMAT)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        if use_file:
            log_filename = f"{filename if filename else 'default'}.log"
            file_handler = logging.FileHandler(f"{log_filename}")
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(file_handler)

    def get_logger(self) -> Logger:
        return self.logger

```

</details> <!-- Utilities -->

<details>
<summary>Set up minimum Docker config</summary>

`Dockerfile`:

```dockerfile
# Specify the parent image to pull core functionality from (in this case Python)
FROM python:3.11

# Name the working dir (will be set by Docker if we don't do it)
WORKDIR /app

# Copy "local" files to the container (in the `/app` folder)
# Sample:
COPY ./api/ ./api/
COPY ./common/ ./common/
# Super important, don't forget to put the DB file in the image if you are running local
COPY ./coverletter.db ./
COPY ./requirements.txt .

# Install requirements in the container
RUN pip install --upgrade pip
# PRE-REQUISITE: Don't forget to refresh your requirements by doing : `pip freeze > requirements.txt`
RUN pip install -r ./requirements.txt
```

**IMPORTANT**: If you are using MS SQL things are more complex, make sure to add to `Dockerfile`:

```dockerfile
# Next section to be able to connect to Azure
## Make sure we get the latest version of our requirements
RUN apt-get update
## Start with installations
RUN apt-get install -y odbcinst
## This gets the MS SQL Drivers for Debian (apparently the default for the image is Debian)
### Get the public keys to be able to pull the sources from MS
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
### Get the drivers
RUN curl https://packages.microsoft.com/config/debian/9/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
RUN apt update
### Annoying, I need to accept the EULA. This was a HEADACHE to figure out
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN apt install -y unixodbc-dev
RUN apt-get install -y unixodbc
```

`docker-compose.yaml` :

```yaml
version: "3"
services:
  # each service that could be executed from docker-compose goes here
  # note that the name can be anything (I just named it api)
  api:
    build: . # config to build my image goes here... maybe? TODO: Investigate further
    expose:
      - 8000
    ports: # Port for my API
      - "8000:8000"
    restart: "always"
    # You could put the command in Dockerfile. Dealer's choice
    command: [ "uvicorn", "api.endpoints:app", "--host=0.0.0.0", "--reload" ]
    # This should prevent us from having to rebuild our image for every change
    volumes:
      - ./api/:/app/api
    # watch allows the app to auto-reload on code changes, very practical
    develop:
      watch:
        - action: sync+restart
          # The path to watch changes for
          path: api/
          # the target (within the container) for the path
          target: /app/api
          ignore:
            - __pycache__/
            - .env
            - .venv
            - env/
            - venv/
            - .idea/
        - action: rebuild
          path: Dockerfile
        - action: rebuild
          path: docker-compose.yaml
        - action: rebuild
          path: requirements.txt
```

</details> <!-- Docker -->

<details>
<summary>Create Business Models</summary>

- This section refers to the **business** models, database models (rows) will be created in a bit
- For simplicity both models are in the same file, they should be separate in the finalized version

```python
from typing import Optional, List, Optional
from pydantic import BaseModel


# This is called "child" because it mimics a 1..N relationship
class ChildModel(BaseModel):
    name: str
    parent_id: Optional[int] = None

    # SUPER important: This tells pydantic that this an ORM (database)
    class Config:
        orm_mode = True


class ParentModel(BaseModel):
    name: str
    children: Optional[List[ChildModel]] = []

    class Config:
        orm_mode = True
```

</details> <!-- Business Models -->

<details>
<summary>Create Database Models</summary>

- Start by adding details to `database.py`
  - connection string: 
    - Try and use sqlite for simplicity if possible
    - If MS SQL is needed remember to un-comment the necessary installs in `Dockerfile`
  - Create `engine` from conn string
  - Create `SessionLocal` from `engine` using `sessionmaker`. This is actually a session **_generator_**
  - Create the SQLAlchemy `declarative_base`. This will link models together
  - Use a `get_session` to actually create the data session
- Secondly, create the DB models
  - Putting all DB models in the same file, otherwise my app fails (should be fixable, don't know how)
  - Notice that the business and DB models are NOT tied up here. That happens in the DAO
- Lastly, create the DAO

```python
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
# IMPORTANT: Notice how we link these to the declarative_base (Base). This orchestrates our relational DB
from common.database.database import Base


class ParentTableRow(Base):
    __tablename__ = "tblNameGoesHere"
    # __table_args__ = {"schema": "coverletter"} # Used only for SQL Server

    """
    SQLAlchemy ORM (Object Relational Model) representation of the table
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    # relationship() can be backtraced, but keeping it simple for this example
    skills: Mapped[List["ChildTableRow"]] = relationship()


class ChildTableRow(Base):
    __tablename__ = "tblNameGoesHere"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    # Notice 2 things:
    # 1. I am assigning a column name here, otherwise it defaults to the same name as in Python
    # 2. I am explicitly stating the ForeignKey
    user_id: Mapped[int] = mapped_column("userId", ForeignKey("tblUser.id"))
```

</details> <!-- DB Models -->

<details>
<summary>Create DAO(s)</summary>

- You can have one or multiple DAO's, for the sake of simplicity we'll have one for this project
- Here's where you link the business and the DB models

```python
from sqlalchemy.orm import Session
from common.database.table_models.table_row_models import ParentTableRow, ChildTableRow
from common.models.user_model import ParentModel


class Dao:
    @staticmethod
    def create_something(session: Session, parent_model: ParentModel) -> ParentTableRow:
        # Create the row model from the business model (passed down from the endpoint)
        child_rows = []
        for child in parent_model.children:
            child_row = ChildTableRow(name=child.name)
            child_rows.append(child_row)

        parent_row = ParentTableRow(name=parent_model.name, children=child_rows)
        session.add(parent_row)
        session.commit()

        # I presume I would be updating the data (mostly the PK) from the DB
        session.refresh(parent_row)
        return parent_row
```

</details> <!-- DAO -->


<details>
<summary>Create an endpoints file</summary>

```python
from fastapi import FastAPI, Depends

from common.database.database import SessionLocal
from sqlalchemy.orm import Session
from common.models.user_model import UserModel
from common.database import Dao

app = FastAPI()


def get_session() -> SessionLocal:
    """
    We need to have an independent database session/connection (SessionLocal) per request, 
    use the same session through all the request and then close it after the request
    is finished.

    Returns:
        SessionLocal: A DB session to be used once
    """
    # fetch session
    session = SessionLocal()
    try:
        # `yield` returns a generator for the session, aka an iterable that can only iterate once
        # In this case it returns a new Session every time is called, but forgets the previous sessions immediately
        yield session
    finally:
        session.close()
```

**_Checkpoint: Make sure you are doing good_**

1. Start up the service

```commandline
docker-compose up api
```

2. See FastAPI:

```
http://localhost:8000/docs
```

</details> <!-- Endpoints -->


<details>
<summary>Testing framework</summary>

Add requirements if you don't have them already:

```requirements
pytest
behave
requests
starlette.testclient
httpx
```

**_Integration tests_**

1. Let PyCharm do the deed for you. Just create a `.feature` file, example:

```gherkin
Feature: AddUsers
  # Add users with assorted combinations

  Scenario: Add Data with endpoint
    When The following is posted to the "add-users" endpoint using PUT
    """
    {"input":"dummy input"}
    """
    Then response should be
    """
    {"TBD":"TBD"}
    """
```

2. Now update the `steps.py`

```python
import json
from behave import when, then
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.database.database import Base
from api.endpoints import app, get_session

# This allows us to test our endpoint without deploying the API
test_client = TestClient(app)

# The following steps recreate our DB in a mock
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
TestSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# These overrides are where the magic to avoid using our actual DB happens
def override_get_session() -> TestSessionLocal:
    session = TestSessionLocal()
    yield session
    session.rollback()
    session.close()


app.dependency_overrides[get_session] = override_get_session


@when('The following is posted to the "{endpoint_name}" endpoint using PUT')
def step_impl(context, endpoint_name):
    try:
        # context.text is where the framework puts the text under the When/Then/Given etc 
        response = test_client.put(url=f"/{endpoint_name}", json=json.loads(context.text))
        if response.status_code == 200:
            # We can add whatever to the context, which will allow us to test
            context.response = response
            context.success = True
        else:
            context.success = False
    except Exception as ex:
        print(f"Something horrible happened!!: {str(ex)}")
        context.success = False


@then("response should be")
def step_impl(context):
    assert context.success is True
    response_dict = json.loads(context.response.text)
    expected = json.loads(context.text)
    assert response_dict == expected
```

</details> <!-- Testing -->


<details>
<summary>Data load</summary>

- Add the module to my image: `COPY ./data_uploader/ ./data_uploader/`
- Leverage `pydantic` for your validations
    - `from pydantic import EmailStr, field_validator`
    - Use pre-built validations directly in the field declaration: `email: EmailStr`
    - implement the field_validator decoration on top of validation
      methods (`@field_validator("phone") ... def myvalidation()`)

</details> <!-- Data load -->

</details> <!-- General: What to set up for blank project -->

## Now for the specific project

<details>

### 2. Create new project in PyCharm

### 3. Basic set up in PyCharm

#### 3.n. Create models

- For each model identified
    - Create a class, inheriting from `BaseModel` (`from pydantic import BaseModel`)
    - Add properties straight under the class, e.g.:

```python
class UserModel(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
```

- Don't forget to add a `Config` class inside the model and set `orm_mode = True`, this tells pydantic that is a an
  Object-Relational (DB) model

#### 3.n. Database

</details> <!-- Now for the specific project -->

</details>


