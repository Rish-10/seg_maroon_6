# Team Maroon 6 Small Group project

## Team members
The members of the team are:
- Soumya (Som) Ajmera
- Aradhya Kunwar
- Jiafan Li
- Ada Ozcan
- Rishi Patel

## Project structure
The project is called `recipify`.  It currently consists of a single app `recipes`.

## Deployed version of the application
The deployed version of the application can be found at [*https://rishi10.pythonanywhere.com/*](https://rishi10.pythonanywhere.com/).

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  The project source code has been developed using Python 3.12, so you are recommended to use the same version.  From the root of the project:

```
$ python3 -m venv venv
$ source venv/bin/activate
```

If your system does not have `python3.12` installed and you are unable to install Python 3.12 as a version you can explicitly refer to from the CLI, then replace `python3.12` by `python3` or `python`, provide this employs a relatively recent version of Python.

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run the server with:
```
$ python3 manage.py runserver
http://127.0.0.1:8000/dashboard/
```

Run all tests with:
```
$ python3 manage.py test
```

## Sources
The packages used by this application are specified in `requirements.txt`

Generative AI Use:
`recipe_form.py`
class RecipeForm: 15 lines; less than 50% of the unit.

`seed_recipes.py`
list SAMPLE_RECIPES: 350 lines; whole unit.
function create_placeholder_image: 5 lines; whole unit.
class Command: 50 lines; more than 50% of the unit.

`user.py`
class User: 20 lines; less than 50% of the unit.
class FollowRequest: 5 lines; about 50% of the unit.

`navbar.html`: 60 lines; more than 50% of the unit.

`recipe_rows.html`: 30 lines; less than 50% of the unit.

`recipe_detail.html`: 150 lines; more than 50% of the unit.

`recipe_form.html`: 60 lines; more than 50% of the unit.

`recipe_list.html`: 60 lines; more than 50% of the unit.

`recipe_search.html`: 120 lines; more than 50% of the unit.

`follow_list.html`: 30 lines; more than 50% of the unit.

`profile_page.html`: 60 lines; less than 50% of the unit.

`profile_search.html`: 60 lines; more than 50% of the unit.

`shopping_list.html`: 10 lines; less than 50% of the unit.

`base_recipe_content.html`: 70 lines; whole unit.

`explore.html`: 20 lines; less than 50% of the unit.

`home.html`: 2 lines; less than 10% of the unit.

`inbox.html`: 80 lines; more than 50% of the unit.

`test_log_in_form.py`: 40 lines; more than 50% of the unit.

`test_password_form.py`: 20 lines; less than 50% of the unit.

`test_rating_form.py`: 15 lines; less than 50% of the unit.

`test_recipe_form`: 40 lines; about 50% of the unit.

`test_signup_form.py`: 20 lines; less than 50% of the unit.

`test_user_form.py`: 10 lines; less than 50% of the unit.

`test_category.py`: 60 lines; more than 50% of the unit.

`test_comment.py`: 50 lines; more than 50% of the unit.

`test_recipe.py`: 60 lines; more than 50% of the unit.

`test_recipe_rating.py`: 20 lines; less than 50% of the unit.

`test_user.py`: 50 lines; less than 50% of the unit.

`dashboard_view.py`
function dashboard: 30 lines; about 50% of the unit.

