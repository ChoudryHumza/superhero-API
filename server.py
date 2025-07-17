from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import logging

app = Flask(__name__)
API_TOKEN = 'a50448b352b3804680843ce2279cc856'
BASE_URL = f'https://www.superheroapi.com/api.php/{API_TOKEN}'






# Global cache for 100 heroes (IDs 1-100) and any newly created heroes.
cached_heroes = {}

def preload_heroes():
    global cached_heroes
    for i in range(1, 101):
        try:
            r = requests.get(f"{BASE_URL}/{i}")
            data = r.json()
            if data.get("response") == "success":
                cached_heroes[str(i)] = data
            else:
                logging.warning(f"Hero id {i} not loaded successfully.")
        except Exception as e:
            logging.error(f"Error fetching hero id {i}: {e}")

# Preload heroes once when the server starts
preload_heroes()

def hero_matches_query(hero, query):
    query = query.lower()
    name = hero.get("name", "").lower()
    full_name = hero.get("biography", {}).get("full-name", "").lower()
    aliases = hero.get("biography", {}).get("aliases", [])
    aliases_joined = " ".join(aliases).lower() if isinstance(aliases, list) else ""
    return query in name or query in full_name or query in aliases_joined









@app.route("/")
def index():
    search_query = request.args.get("search", "").strip()
    # Define professor card
    professor = {
         "id": "professor",
         "image": {"url": "https://www.cs.columbia.edu/~chilton/web/images/headshots/chilton-banner-headshot.jpg"},
         "name": "Professor Lydia Chilton",
         "biography": {"full-name": "Professor Lydia Chilton"}
    }
    if search_query:
        results = [hero for hero in cached_heroes.values() if hero_matches_query(hero, search_query)]
        # Only insert professor if it matches the search query.
        if hero_matches_query(professor, search_query):
            results.insert(0, professor)
        return render_template("index.html", results=results, search=search_query)
    
    # No search query: show professor card first then cached heroes.
    results = [professor] + list(cached_heroes.values())
    return render_template("index.html", results=results)









@app.route("/view/<id>")
def view(id):
    if id == "professor":
        return render_template("details.html", hero="professor")
    else:
        hero = cached_heroes.get(id)
        if hero:
            return render_template("details.html", hero=hero)
        else:
            return "Hero not found", 404










@app.route("/add", methods=["GET", "POST"])
def add():
    errors = {}
    if request.method == "POST":
        full_name    = request.form.get("full_name", "").strip()
        alter_egos   = request.form.get("alter_egos", "").strip()
        aliases      = request.form.get("aliases", "").strip()
        intelligence = request.form.get("intelligence", "").strip()
        strength     = request.form.get("strength", "").strip()
        speed        = request.form.get("speed", "").strip()
        durability   = request.form.get("durability", "").strip()
        power        = request.form.get("power", "").strip()
        combat       = request.form.get("combat", "").strip()
        gender       = request.form.get("gender", "").strip()
        occupation   = request.form.get("occupation", "").strip()
        image_option = request.form.get("image_option", "no_image").strip()
        
        if not full_name:
            errors["full_name"] = "Full Name is required."
        if not alter_egos:
            errors["alter_egos"] = "Alter Egos is required."
        if not aliases:
            errors["aliases"] = "Aliases is required."
        if not gender:
            errors["gender"] = "Gender is required."
        if not occupation:
            errors["occupation"] = "Occupation is required."
        
        for field_value, field_key, label in [
            (intelligence, "intelligence", "Intelligence"),
            (strength, "strength", "Strength"),
            (speed, "speed", "Speed"),
            (durability, "durability", "Durability"),
            (power, "power", "Power"),
            (combat, "combat", "Combat")
        ]:
            if not field_value:
                errors[field_key] = f"{label} is required."
            else:
                try:
                    int(field_value)
                except ValueError:
                    errors[field_key] = f"{label} must be a number."
        
        if errors:
            return jsonify({"success": False, "errors": errors})
        else:
            image_options = {
                "no_image": "https://media.pri.org/s3fs-public/story/images/RTX1GZCO.jpg",
                "michael_scott": "https://media.licdn.com/dms/image/v2/D5612AQGqPGHORIsa-g/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1691871730624?e=2147483647&v=beta&t=HT4mUN4oFnzQAJ7wz1X7pDqRp38vifBP8d9SkyG7hW4",
                "pam_beesly": "https://i.ytimg.com/vi/bskdOrWMwD0/maxresdefault.jpg",
                "jim_halpert": "https://www.denofgeek.com/wp-content/uploads/2021/10/Jim-The-Office-John-Krasinski.jpg?fit=1200%2C675",
                "andy_bernard": "https://static1.srcdn.com/wordpress/wp-content/uploads/2021/01/The-Office-The-10-Saddest-Things-About-Andy.jpg",
                "dwight_schrute": "https://img.nbc.com/files/images/2013/11/12/dwight-500x500.jpg",
                "kevin_malone": "https://upload.wikimedia.org/wikipedia/en/6/60/Office-1200-baumgartner1.jpg",
                "angela_martin": "https://upload.wikimedia.org/wikipedia/en/6/60/Office-1200-baumgartner1.jpg",
                "phyllis_lapin": "https://static1.srcdn.com/wordpress/wp-content/uploads/2020/04/1400x700-2-15.jpg",
                "todd_packer": "https://static.wikia.nocookie.net/theoffice/images/6/61/Todd_Packer.jpg/revision/latest?cb=20150916222108"
            }
            image_url = image_options.get(image_option, image_options["no_image"])
            new_id = str(max([int(k) for k in cached_heroes.keys()] + [100]) + 1)
            new_hero = {
                "id": new_id,
                "name": full_name,
                "image": {"url": image_url},
                "biography": {
                    "full-name": full_name,
                    "alter-egos": alter_egos,
                    "aliases": [alias.strip() for alias in aliases.split(",") if alias.strip()]
                },
                "powerstats": {
                    "intelligence": intelligence,
                    "strength": strength,
                    "speed": speed,
                    "durability": durability,
                    "power": power,
                    "combat": combat
                },
                "appearance": {
                    "gender": gender
                },
                "work": {
                    "occupation": occupation
                },
                "connections": {}
            }
            cached_heroes[new_id] = new_hero
            return jsonify({"success": True, "new_id": new_id})
    return render_template("add.html", errors={}, form={})











@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    # Only allow editing of user-created heroes (IDs > 100)
    if id == "professor" or (id.isdigit() and int(id) <= 100):
        return redirect(url_for("view", id=id))
    
    hero = cached_heroes.get(id)
    if not hero:
        return "Hero not found", 404

    errors = {}
    if request.method == "POST":
        full_name    = request.form.get("full_name", "").strip()
        alter_egos   = request.form.get("alter_egos", "").strip()
        aliases      = request.form.get("aliases", "").strip()
        intelligence = request.form.get("intelligence", "").strip()
        strength     = request.form.get("strength", "").strip()
        speed        = request.form.get("speed", "").strip()
        durability   = request.form.get("durability", "").strip()
        power        = request.form.get("power", "").strip()
        combat       = request.form.get("combat", "").strip()
        gender       = request.form.get("gender", "").strip()
        occupation   = request.form.get("occupation", "").strip()
        image_option = request.form.get("image_option", "").strip()
        
        if not full_name:
            errors["full_name"] = "Full Name is required."
        if not alter_egos:
            errors["alter_egos"] = "Alter Egos is required."
        if not aliases:
            errors["aliases"] = "Aliases is required."
        if not gender:
            errors["gender"] = "Gender is required."
        if not occupation:
            errors["occupation"] = "Occupation is required."
        
        for field_value, field_key, label in [
            (intelligence, "intelligence", "Intelligence"),
            (strength, "strength", "Strength"),
            (speed, "speed", "Speed"),
            (durability, "durability", "Durability"),
            (power, "power", "Power"),
            (combat, "combat", "Combat")
        ]:
            if not field_value:
                errors[field_key] = f"{label} is required."
            else:
                try:
                    int(field_value)
                except ValueError:
                    errors[field_key] = f"{label} must be a number."
        
        if errors:
            return render_template("edit.html", errors=errors, form=request.form, hero_id=id)
        else:
            image_options = {
                "no_image": "https://media.pri.org/s3fs-public/story/images/RTX1GZCO.jpg",
                "michael_scott": "https://media.licdn.com/dms/image/v2/D5612AQGqPGHORIsa-g/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1691871730624?e=2147483647&v=beta&t=HT4mUN4oFnzQAJ7wz1X7pDqRp38vifBP8d9SkyG7hW4",
                "pam_beesly": "https://i.ytimg.com/vi/bskdOrWMwD0/maxresdefault.jpg",
                "jim_halpert": "https://www.denofgeek.com/wp-content/uploads/2021/10/Jim-The-Office-John-Krasinski.jpg?fit=1200%2C675",
                "andy_bernard": "https://static1.srcdn.com/wordpress/wp-content/uploads/2021/01/The-Office-The-10-Saddest-Things-About-Andy.jpg",
                "dwight_schrute": "https://img.nbc.com/files/images/2013/11/12/dwight-500x500.jpg",
                "kevin_malone": "https://upload.wikimedia.org/wikipedia/en/6/60/Office-1200-baumgartner1.jpg",
                "angela_martin": "https://upload.wikimedia.org/wikipedia/en/6/60/Office-1200-baumgartner1.jpg",
                "phyllis_lapin": "https://static1.srcdn.com/wordpress/wp-content/uploads/2020/04/1400x700-2-15.jpg",
                "todd_packer": "https://static.wikia.nocookie.net/theoffice/images/6/61/Todd_Packer.jpg/revision/latest?cb=20150916222108"
            }
            image_url = image_options.get(image_option, hero.get("image", {}).get("url"))
            
            updated_hero = {
                "id": id,
                "name": full_name,
                "image": {"url": image_url},
                "biography": {
                    "full-name": full_name,
                    "alter-egos": alter_egos,
                    "aliases": [alias.strip() for alias in aliases.split(",") if alias.strip()]
                },
                "powerstats": {
                    "intelligence": intelligence,
                    "strength": strength,
                    "speed": speed,
                    "durability": durability,
                    "power": power,
                    "combat": combat
                },
                "appearance": {
                    "gender": gender
                },
                "work": {
                    "occupation": occupation
                },
                "connections": hero.get("connections", {})
            }
            cached_heroes[id] = updated_hero
            return redirect(url_for("view", id=id))
    
    # GET: prepopulate form with current hero data.
    current_image_url = hero.get("image", {}).get("url", "").strip().lower()
    print("Current image URL:", current_image_url)
    image_option = "no_image"
    options = {
        "no_image": "https://media.pri.org/s3fs-public/story/images/RTX1GZCO.jpg",
        "michael_scott": "https://media.licdn.com/dms/image/v2/D5612AQGqPGHORIsa-g/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1691871730624?e=2147483647&v=beta&t=HT4mUN4oFnzQAJ7wz1X7pDqRp38vifBP8d9SkyG7hW4",
        "pam_beesly": "https://i.ytimg.com/vi/bskdOrWMwD0/maxresdefault.jpg",
        "jim_halpert": "https://www.denofgeek.com/wp-content/uploads/2021/10/Jim-The-Office-John-Krasinski.jpg?fit=1200%2C675",
        "andy_bernard": "https://static1.srcdn.com/wordpress/wp-content/uploads/2021/01/The-Office-The-10-Saddest-Things-About-Andy.jpg",
        "dwight_schrute": "https://img.nbc.com/files/images/2013/11/12/dwight-500x500.jpg",
        "kevin_malone": "https://upload.wikimedia.org/wikipedia/en/6/60/Office-1200-baumgartner1.jpg",
        "angela_martin": "https://upload.wikimedia.org/wikipedia/en/6/60/Office-1200-baumgartner1.jpg",
        "phyllis_lapin": "https://static1.srcdn.com/wordpress/wp-content/uploads/2020/04/1400x700-2-15.jpg",
        "todd_packer": "https://static.wikia.nocookie.net/theoffice/images/6/61/Todd_Packer.jpg/revision/latest?cb=20150916222108"
    }
    for key, value in options.items():
        if current_image_url == value.strip().lower():
            image_option = key
            break

    print("Prepopulated image option:", image_option)
    form_data = {
        "full_name": hero.get("biography", {}).get("full-name", ""),
        "alter_egos": hero.get("biography", {}).get("alter-egos", ""),  # Changed key to "alter_egos"
        "aliases": ", ".join(hero.get("biography", {}).get("aliases", [])),
        "intelligence": hero.get("powerstats", {}).get("intelligence", ""),
        "strength": hero.get("powerstats", {}).get("strength", ""),
        "speed": hero.get("powerstats", {}).get("speed", ""),
        "durability": hero.get("powerstats", {}).get("durability", ""),
        "power": hero.get("powerstats", {}).get("power", ""),
        "combat": hero.get("powerstats", {}).get("combat", ""),
        "gender": hero.get("appearance", {}).get("gender", ""),
        "occupation": hero.get("work", {}).get("occupation", ""),
        "image_option": image_option
    }
    return render_template("edit.html", errors={}, form=form_data, hero_id=id)

if __name__ == "__main__":
    app.run(debug=True, port=5001)



'''
server.py – Detailed Explanation
from flask import Flask, render_template, request, redirect, url_for, jsonify
Explanation:
Flask: This is the core Flask class that we use to create our web application instance.
If you remove this import, you won't be able to create your Flask app, and your code won't run.
render_template: This function renders HTML templates (usually stored in a “templates” folder) and returns an HTML response.
Without it, you cannot dynamically generate HTML from template files.
request: This object holds the incoming request data (such as form data, URL parameters, etc.).
Removing this would break any code that reads user input.
redirect: This function is used to redirect the client to a different URL.
If removed, you wouldn’t be able to send users to another page after an action (like after a form submission).
url_for: This function generates URLs for routes based on the function names, which makes your code more maintainable.
Without it, you’d need to hardcode URLs, increasing the chance of errors if routes change.
jsonify: This function converts a Python dictionary into a JSON response.
It’s crucial for API endpoints returning JSON data, such as our Ajax responses in add and edit routes.
import requests
Explanation:
The requests library is used to make HTTP requests from our server to external APIs.
In our code, we use it to fetch hero data from an external Superhero API. Without it, we couldn’t retrieve API data.
import logging
Explanation:
This module is used for logging warnings or errors during execution.
Logging is useful for debugging and monitoring the server's operation. Removing logging might make it harder to diagnose issues.
app = Flask(__name__)
Explanation:
This line creates an instance of the Flask application. The special variable __name__ tells Flask where to look for templates and static files.
If you remove this, you won’t have an application object to configure routes or run the server.
API_TOKEN = 'a50448b352b3804680843ce2279cc856'
BASE_URL = f'https://www.superheroapi.com/api.php/{API_TOKEN}'
Explanation:
API_TOKEN: This is a string that represents your API authentication token.
If you remove or change it, your API calls might fail or use incorrect credentials.
BASE_URL: A formatted string (f-string) that constructs the base URL for the external superhero API using your API_TOKEN.
If this is missing, your requests to the API would have no endpoint, breaking the data fetching.
cached_heroes = {}
Explanation:
A global dictionary to store hero data fetched from the API (and any newly created heroes).
Caching improves performance by avoiding repeated API calls. Removing this caching mechanism means every request might trigger a new API call, slowing down your app.
Function: preload_heroes()

def preload_heroes():
    global cached_heroes
    for i in range(1, 101):
        try:
            r = requests.get(f"{BASE_URL}/{i}")
            data = r.json()
            if data.get("response") == "success":
                cached_heroes[str(i)] = data
            else:
                logging.warning(f"Hero id {i} not loaded successfully.")
        except Exception as e:
            logging.error(f"Error fetching hero id {i}: {e}")
Explanation:
def preload_heroes():
Defines a function that loads hero data for hero IDs 1 through 100 from the external API.
global cached_heroes:
Tells Python that we are referring to the global cached_heroes variable, not a new local one.
for i in range(1, 101):
Loops through hero IDs 1 to 100.
try:
Starts a try block to catch potential errors during the HTTP request.
r = requests.get(f"{BASE_URL}/{i}")
Sends an HTTP GET request to fetch data for hero with id i.
data = r.json():
Parses the JSON response into a Python dictionary.
if data.get("response") == "success":
Checks if the API response indicates a successful fetch.
cached_heroes[str(i)] = data:
Stores the hero data in the cached_heroes dictionary, using the hero id (converted to a string) as the key.
else:
If the response is not successful:
logging.warning(...):
Logs a warning message indicating that the hero data wasn’t loaded.
except Exception as e:
Catches any exceptions that occur during the request or JSON parsing.
logging.error(...):
Logs an error message with details about the exception.
If you remove error handling, your server might crash on a failed request, and you’d lose insight into why a particular hero couldn’t be loaded.
preload_heroes()
Explanation:
Calls the preload_heroes() function immediately after defining it so that the hero data is loaded when the server starts.
If you remove this call, your cache would remain empty, and your homepage or search features wouldn’t have any hero data to display.
Function: hero_matches_query()

def hero_matches_query(hero, query):
    query = query.lower()
    name = hero.get("name", "").lower()
    full_name = hero.get("biography", {}).get("full-name", "").lower()
    aliases = hero.get("biography", {}).get("aliases", [])
    aliases_joined = " ".join(aliases).lower() if isinstance(aliases, list) else ""
    return query in name or query in full_name or query in aliases_joined
Explanation:
def hero_matches_query(hero, query):
This function checks if a given hero (a dictionary) matches the search query.
query = query.lower():
Converts the query string to lowercase to ensure case-insensitive matching.
name = hero.get("name", "").lower():
Retrieves the hero’s name from the dictionary, defaults to an empty string if missing, and converts it to lowercase.
full_name = hero.get("biography", {}).get("full-name", "").lower():
Retrieves the hero's full name from the nested biography dictionary. If "biography" or "full-name" isn’t present, it defaults to an empty string.
aliases = hero.get("biography", {}).get("aliases", []):
Retrieves the hero’s aliases. Defaults to an empty list if not present.
aliases_joined = " ".join(aliases).lower() if isinstance(aliases, list) else "":
Joins the aliases into a single string (separated by a space) and converts to lowercase if aliases is a list.
return query in name or query in full_name or query in aliases_joined:
Returns True if the query is found in any of the hero's name, full name, or aliases; otherwise, returns False.
If you remove this function, the search functionality wouldn’t be able to filter heroes based on the query.
Route: Index ("/")

@app.route("/")
def index():
    search_query = request.args.get("search", "").strip()
    # Define professor card
    professor = {
         "id": "professor",
         "image": {"url": "https://www.cs.columbia.edu/~chilton/web/images/headshots/chilton-banner-headshot.jpg"},
         "name": "Professor Lydia Chilton",
         "biography": {"full-name": "Professor Lydia Chilton"}
    }
    if search_query:
        results = [hero for hero in cached_heroes.values() if hero_matches_query(hero, search_query)]
        # Only insert professor if it matches the search query.
        if hero_matches_query(professor, search_query):
            results.insert(0, professor)
        return render_template("index.html", results=results, search=search_query)
    
    # No search query: show professor card first then cached heroes.
    results = [professor] + list(cached_heroes.values())
    return render_template("index.html", results=results)
Explanation:
@app.route("/"):
This decorator binds the following function to the root URL ("/").
Removing it would mean this function is never called for requests to the homepage.
def index()::
The view function for the homepage.
search_query = request.args.get("search", "").strip()::
Retrieves the "search" query parameter from the URL. If not present, defaults to an empty string. strip() removes any whitespace from the ends.
If you remove the strip, accidental spaces might cause mismatches.
professor = { ... }:
A dictionary representing a special hero (Professor Lydia Chilton). This card is always shown on the full homepage, and conditionally included in search results if relevant.
if search_query::
Checks if the user has entered a search query.
results = [hero for hero in cached_heroes.values() if hero_matches_query(hero, search_query)]:
Uses a list comprehension to filter cached heroes based on whether they match the search query.
if hero_matches_query(professor, search_query): results.insert(0, professor):
If the professor card matches the query, it is inserted at the beginning of the results list.
return render_template("index.html", results=results, search=search_query):
Renders the "index.html" template with the filtered results and the search query.
Else: (when no search query is provided)
results = [professor] + list(cached_heroes.values()):
Prepends the professor card to the full list of cached heroes.
return render_template("index.html", results=results):
Renders the homepage with the complete list.
If you remove these conditionals, the search functionality wouldn’t work properly, and the professor card might always appear regardless of the search query.
Route: View ("/view/<id>")

@app.route("/view/<id>")
def view(id):
    if id == "professor":
        return render_template("details.html", hero="professor")
    else:
        hero = cached_heroes.get(id)
        if hero:
            return render_template("details.html", hero=hero)
        else:
            return "Hero not found", 404
Explanation:
@app.route("/view/<id>"):
This decorator maps URLs of the form /view/<id> (where <id> is a variable part) to the following function.
def view(id)::
The view function that takes the id from the URL.
if id == "professor"::
Checks if the id is the special case "professor".
return render_template("details.html", hero="professor")::
Renders the details page with the professor card.
else::
Retrieves the hero from cached_heroes using the id.
if hero::
If the hero is found, render details.html with that hero’s data.
else::
If the hero is not found, return a 404 error.
Changing these conditions would affect how hero details are displayed and error handling for missing heroes.
Route: Add ("/add")

@app.route("/add", methods=["GET", "POST"])
def add():
    errors = {}
    if request.method == "POST":
        full_name    = request.form.get("full_name", "").strip()
        alter_egos   = request.form.get("alter_egos", "").strip()
        aliases      = request.form.get("aliases", "").strip()
        intelligence = request.form.get("intelligence", "").strip()
        strength     = request.form.get("strength", "").strip()
        speed        = request.form.get("speed", "").strip()
        durability   = request.form.get("durability", "").strip()
        power        = request.form.get("power", "").strip()
        combat       = request.form.get("combat", "").strip()
        gender       = request.form.get("gender", "").strip()
        occupation   = request.form.get("occupation", "").strip()
        image_option = request.form.get("image_option", "no_image").strip()
        
        # Validate required fields and numeric values...
        if not full_name:
            errors["full_name"] = "Full Name is required."
        if not alter_egos:
            errors["alter_egos"] = "Alter Egos is required."
        if not aliases:
            errors["aliases"] = "Aliases is required."
        if not gender:
            errors["gender"] = "Gender is required."
        if not occupation:
            errors["occupation"] = "Occupation is required."
        
        for field_value, field_key, label in [
            (intelligence, "intelligence", "Intelligence"),
            (strength, "strength", "Strength"),
            (speed, "speed", "Speed"),
            (durability, "durability", "Durability"),
            (power, "power", "Power"),
            (combat, "combat", "Combat")
        ]:
            if not field_value:
                errors[field_key] = f"{label} is required."
            else:
                try:
                    int(field_value)
                except ValueError:
                    errors[field_key] = f"{label} must be a number."
        
        if errors:
            return jsonify({"success": False, "errors": errors})
        else:
            image_options = {
                "no_image": "https://media.pri.org/s3fs-public/story/images/RTX1GZCO.jpg",
                "michael_scott": "https://media.licdn.com/dms/image/v2/D5612AQGqPGHORIsa-g/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1691871730624?e=2147483647&v=beta&t=HT4mUN4oFnzQAJ7wz1X7pDqRp38vifBP8d9SkyG7hW4",
                "pam_beesly": "https://i.ytimg.com/vi/bskdOrWMwD0/maxresdefault.jpg",
                "jim_halpert": "https://www.denofgeek.com/wp-content/uploads/2021/10/Jim-The-Office-John-Krasinski.jpg?fit=1200%2C675",
                "andy_bernard": "https://static1.srcdn.com/wordpress/wp-content/uploads/2021/01/The-Office-The-10-Saddest-Things-About-Andy.jpg",
                "dwight_schrute": "https://img.nbc.com/files/images/2013/11/12/dwight-500x500.jpg",
                "kevin_malone": "https://upload.wikimedia.org/wikipedia/en/6/60/Office-1200-baumgartner1.jpg",
                "angela_martin": "https://upload.wikimedia.org/wikipedia/en/6/60/Office-1200-baumgartner1.jpg",
                "phyllis_lapin": "https://static1.srcdn.com/wordpress/wp-content/uploads/2020/04/1400x700-2-15.jpg",
                "todd_packer": "https://static.wikia.nocookie.net/theoffice/images/6/61/Todd_Packer.jpg/revision/latest?cb=20150916222108"
            }
            image_url = image_options.get(image_option, image_options["no_image"])
            new_id = str(max([int(k) for k in cached_heroes.keys()] + [100]) + 1)
            new_hero = {
                "id": new_id,
                "name": full_name,
                "image": {"url": image_url},
                "biography": {
                    "full-name": full_name,
                    "alter-egos": alter_egos,
                    "aliases": [alias.strip() for alias in aliases.split(",") if alias.strip()]
                },
                "powerstats": {
                    "intelligence": intelligence,
                    "strength": strength,
                    "speed": speed,
                    "durability": durability,
                    "power": power,
                    "combat": combat
                },
                "appearance": {
                    "gender": gender
                },
                "work": {
                    "occupation": occupation
                },
                "connections": {}
            }
            cached_heroes[new_id] = new_hero
            return jsonify({"success": True, "new_id": new_id})
    return render_template("add.html", errors={}, form={})
Explanation:
@app.route("/add", methods=["GET", "POST"]):
Binds the add() function to the "/add" URL and allows both GET (to display the form) and POST (to handle form submissions).
Inside the function, we initialize an empty dictionary errors to collect validation errors.
if request.method == "POST":
Checks if the request is a POST (form submission).
We then retrieve form data using request.form.get(...) for each field, trimming whitespace with .strip().
Validation is performed for required fields (like full_name, alter_egos, aliases, gender, occupation) and for numeric fields (intelligence, strength, etc.). If a field is missing or not numeric, an error message is added to the errors dictionary.
if errors: returns a JSON response with success set to False and the errors dictionary. This JSON is used by the Ajax script (add.js).
Else:
A dictionary image_options maps image option keys to URLs.
The correct image URL is chosen based on the selected option.
A new hero id is generated by taking the maximum key from cached_heroes (converted to int) and adding 1.
A new hero dictionary is created with the submitted data and stored in cached_heroes.
Finally, a JSON response is returned with success set to True and the new hero id.
If the request is GET:
The function renders the add.html template, passing any errors or form data (initially empty).
If you remove the JSON responses or validation, users may submit incomplete or invalid data.
Route: Edit ("/edit/<id>")

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    # Only allow editing of user-created heroes (IDs > 100)
    if id == "professor" or (id.isdigit() and int(id) <= 100):
        return redirect(url_for("view", id=id))
    
    hero = cached_heroes.get(id)
    if not hero:
        return "Hero not found", 404

    errors = {}
    if request.method == "POST":
        full_name    = request.form.get("full_name", "").strip()
        alter_egos   = request.form.get("alter_egos", "").strip()
        aliases      = request.form.get("aliases", "").strip()
        intelligence = request.form.get("intelligence", "").strip()
        strength     = request.form.get("strength", "").strip()
        speed        = request.form.get("speed", "").strip()
        durability   = request.form.get("durability", "").strip()
        power        = request.form.get("power", "").strip()
        combat       = request.form.get("combat", "").strip()
        gender       = request.form.get("gender", "").strip()
        occupation   = request.form.get("occupation", "").strip()
        image_option = request.form.get("image_option", "").strip()
        
        if not full_name:
            errors["full_name"] = "Full Name is required."
        if not alter_egos:
            errors["alter_egos"] = "Alter Egos is required."
        if not aliases:
            errors["aliases"] = "Aliases is required."
        if not gender:
            errors["gender"] = "Gender is required."
        if not occupation:
            errors["occupation"] = "Occupation is required."
        
        for field_value, field_key, label in [
            (intelligence, "intelligence", "Intelligence"),
            (strength, "strength", "Strength"),
            (speed, "speed", "Speed"),
            (durability, "durability", "Durability"),
            (power, "power", "Power"),
            (combat, "combat", "Combat")
        ]:
            if not field_value:
                errors[field_key] = f"{label} is required."
            else:
                try:
                    int(field_value)
                except ValueError:
                    errors[field_key] = f"{label} must be a number."
        
        if errors:
            return render_template("edit.html", errors=errors, form=request.form, hero_id=id)
        else:
            image_options = {
                "no_image": "https://media.pri.org/s3fs-public/story/images/RTX1GZCO.jpg",
                "michael_scott": "https://media.licdn.com/dms/image/v2/D5612AQGqPGHORIsa-g/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1691871730624?e=2147483647&v=beta&t=HT4mUN4oFnzQAJ7wz1X7pDqRp38vifBP8d9SkyG7hW4",
                "pam_beesly": "https://i.ytimg.com/vi/bskdOrWMwD0/maxresdefault.jpg",
                "jim_halpert": "https://www.denofgeek.com/wp-content/uploads/2021/10/Jim-The-Office-John-Krasinski.jpg?fit=1200%2C675",
                "andy_bernard": "https://static1.srcdn.com/wordpress/wp-content/uploads/2021/01/The-Office-The-10-Saddest-Things-About-Andy.jpg",
                "dwight_schrute": "https://img.nbc.com/files/images/2013/11/12/dwight-500x500.jpg",
                "kevin_malone": "https://upload.wikimedia.org/wikipedia/en/6/60/Office-1200-baumgartner1.jpg",
                "angela_martin": "https://upload.wikimedia.org/wikipedia/en/6/60/Office-1200-baumgartner1.jpg",
                "phyllis_lapin": "https://static1.srcdn.com/wordpress/wp-content/uploads/2020/04/1400x700-2-15.jpg",
                "todd_packer": "https://static.wikia.nocookie.net/theoffice/images/6/61/Todd_Packer.jpg/revision/latest?cb=20150916222108"
            }
            image_url = image_options.get(image_option, hero.get("image", {}).get("url"))
            
            updated_hero = {
                "id": id,
                "name": full_name,
                "image": {"url": image_url},
                "biography": {
                    "full-name": full_name,
                    "alter-egos": alter_egos,
                    "aliases": [alias.strip() for alias in aliases.split(",") if alias.strip()]
                },
                "powerstats": {
                    "intelligence": intelligence,
                    "strength": strength,
                    "speed": speed,
                    "durability": durability,
                    "power": power,
                    "combat": combat
                },
                "appearance": {
                    "gender": gender
                },
                "work": {
                    "occupation": occupation
                },
                "connections": hero.get("connections", {})
            }
            cached_heroes[id] = updated_hero
            return redirect(url_for("view", id=id))
    
    # GET: prepopulate form with current hero data.
    current_image_url = hero.get("image", {}).get("url", "").strip().lower()
    print("Current image URL:", current_image_url)
    image_option = "no_image"
    options = {
        "no_image": "https://media.pri.org/s3fs-public/story/images/RTX1GZCO.jpg",
        "michael_scott": "https://media.licdn.com/dms/image/v2/D5612AQGqPGHORIsa-g/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1691871730624?e=2147483647&v=beta&t=HT4mUN4oFnzQAJ7wz1X7pDqRp38vifBP8d9SkyG7hW4",
        "pam_beesly": "https://i.ytimg.com/vi/bskdOrWMwD0/maxresdefault.jpg",
        "jim_halpert": "https://www.denofgeek.com/wp-content/uploads/2021/10/Jim-The-Office-John-Krasinski.jpg?fit=1200%2C675",
        "andy_bernard": "https://static1.srcdn.com/wordpress/wp-content/uploads/2021/01/The-Office-The-10-Saddest-Things-About-Andy.jpg",
        "dwight_schrute": "https://img.nbc.com/files/images/2013/11/12/dwight-500x500.jpg",
        "kevin_malone": "https://upload.wikimedia.org/wikipedia/en/6/60/Office-1200-baumgartner1.jpg",
        "angela_martin": "https://upload.wikimedia.org/wikipedia/en/6/60/Office-1200-baumgartner1.jpg",
        "phyllis_lapin": "https://static1.srcdn.com/wordpress/wp-content/uploads/2020/04/1400x700-2-15.jpg",
        "todd_packer": "https://static.wikia.nocookie.net/theoffice/images/6/61/Todd_Packer.jpg/revision/latest?cb=20150916222108"
    }
    for key, value in options.items():
        if current_image_url == value.strip().lower():
            image_option = key
            break

    print("Prepopulated image option:", image_option)
    form_data = {
        "full_name": hero.get("biography", {}).get("full-name", ""),
        "alter-egos": hero.get("biography", {}).get("alter-egos", ""),
        "aliases": ", ".join(hero.get("biography", {}).get("aliases", [])),
        "intelligence": hero.get("powerstats", {}).get("intelligence", ""),
        "strength": hero.get("powerstats", {}).get("strength", ""),
        "speed": hero.get("powerstats", {}).get("speed", ""),
        "durability": hero.get("powerstats", {}).get("durability", ""),
        "power": hero.get("powerstats", {}).get("power", ""),
        "combat": hero.get("powerstats", {}).get("combat", ""),
        "gender": hero.get("appearance", {}).get("gender", ""),
        "occupation": hero.get("work", {}).get("occupation", ""),
        "image_option": image_option
    }
    return render_template("edit.html", errors={}, form=form_data, hero_id=id)
Explanation:
@app.route("/edit/<id>", methods=["GET", "POST"]):
Maps the URL for editing a hero. It supports both GET (to show the edit form) and POST (to handle form submission).
if id == "professor" or (id.isdigit() and int(id) <= 100):
Restricts editing to user-created heroes only (IDs > 100). If the hero is an API hero or the professor, the user is redirected to the view page.
hero = cached_heroes.get(id):
Retrieves the hero data from the cache. If not found, returns a 404 error.
if request.method == "POST":
Processes form submission:
Retrieves form data for each field, trims whitespace.
Validates required fields and numeric inputs.
If there are errors, re-renders the edit page with error messages.
If validation passes, maps the selected image option to its URL, creates an updated hero dictionary, saves it to the cache, and then redirects to the hero view page.
GET branch:
Prepopulates the form with the current hero data:
Retrieves the current image URL, converts it to lowercase, and compares it against the predefined options to determine which option should be selected.
Prints debug information to the console (these print statements help during development; you might remove them in production).
Creates a form_data dictionary with prepopulated values.
Renders the edit.html template with the current hero data.
If you remove the validation or the image option mapping, you might lose proper error handling or the correct prepopulation of the image selection.
if __name__ == "__main__":
    app.run(debug=True, port=5001)
Explanation:
This conditional ensures that the Flask development server only runs when the file is executed directly, not when it is imported as a module.
debug=True enables debug mode, which provides detailed error messages and auto-reloads the server on code changes.
port=5001 specifies that the server should run on port 5001.
If you remove this block, the server won’t start when running this file directly.
Summary of Alternatives and Consequences
Imports and Flask Setup:
Alternative libraries (e.g., FastAPI) could be used instead of Flask, but that would require rewriting much of the code.
Removing error handling or logging would make debugging much more difficult.
Caching with cached_heroes:
An alternative might be using a database instead of an in-memory cache. This would persist data between server restarts but would require additional setup.
Route Definitions:
Each route is designed to separate concerns: index for listing/searching, view for details, add for creating, and edit for updating. Combining routes would reduce modularity and make the code harder to maintain.
Form Data Validation:
The chosen approach uses server-side validation and returns JSON errors for Ajax requests. Alternatively, client-side JavaScript validation could be added, but it should always be backed by server-side validation.
Preloading Heroes:
Preloading improves performance by avoiding API calls on every request. Without it, your application might become slow or rate-limited by the external API.

'''