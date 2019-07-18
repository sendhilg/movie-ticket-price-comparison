# Movie Ticket Price Comparison

## Description
The application is completed as a task following the [brief](BRIEF.md).


## Requirements
The application was developed using python version 3.7.3 on a windows 10 machine 
using Visual Studio Code for coding and GitBash for running commands.

To check the version on your machine run the below command:

    $ python --version


## Cloning the project and setting up the local development environment:
Clone the project from github:

    $ git clone https://github.com/sendhilg/movie-ticket-price-comparison.git


Change into the project directory 'movie-ticket-price-comparison':

    $ cd movie-ticket-price-comparison


Setup a virtual environment for the application using virtualenv tool:

    virtualenv is a tool to create isolated Python environments. virtualenv creates a folder which contains all the necessary executables for the packages that a Python application would need.

    On windows (GitBash Terminal):

        $ pip install virtualenv
        $ python -m venv movie_venv
        $ source ./movie_venv/Scripts/activate

    On Linux systems (Bash Terminal):

        $ pip3 install --user virtualenv
        $ python3 -m venv movie_venv
        $ source ./movie_venv/bin/activate

    To verify that the virtual environment is activated, run the below command and 
    check that the source for pip (python package manager) is the virtual environment i.e. 'movie_venv' created in the above steps:

        $ pip -V

After the virtual environment is created and activated, use the package manager 'pip' to install 
requirements for the application.

    $ pip install -r requirements.txt


## Launching the application locally:

Important:
    For the application to be able to retrieve data from the downstream API's, the API Access Key must be 
    provided by the application in the http request headers 'x-access-token'.

    Create an environment variable called MOVIES_API_ACCESS_TOKEN and set it to the required access key value using the export(Linux) or set(Windows) command.

Django web framework is used to develop this application. Run the below manage.py command to run the local server
for the application:

    $ python manage.py runserver --noreload

Copy the localhost address displayed on the console and launch the application using the below URL:

    http://127.0.0.1:8000/tickets/price-comparison


### Example
```
$ python manage.py runserver --noreload

Performing system checks...

System check identified no issues (0 silenced).
July 18, 2019 - 23:38:58
Django version 2.2.2, using settings 'movie.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

```

## Unit Tests

### Running unit tests
Run the below commands at the project directory to run tests with code coverage. The test should fail if the 
code coverage is under 75%.

    $  pytest --cov=tickets --cov-report=term --cov-report=html --cov-fail-under=75 --no-cov-on-fail   --junitxml=unittest-report/xml/results.xml
