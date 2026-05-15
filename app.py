import statistics
import random
import storage.movie_storage_sql as storage
import requests
import helper_file
from dotenv import load_dotenv
import os
from colors import RESET, BOLD, UNDERLINE, RED, GREEN, YELLOW, MAGENTA, CYAN


load_dotenv()

API_KEY = os.getenv("API_KEY")

def user_menu():
    """Display the main menu and execute the selected user action."""

    print()
    print(f"{BOLD}{UNDERLINE}{CYAN}********** My Movie Database ********** {RESET}")
    while True:
        print()
        print(f"{BOLD}{UNDERLINE}{YELLOW}     Menu     {RESET}")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")
        print("9. Generate website")
        print()

        while True:
            try:
                user_choice = int(input(f"{GREEN}Enter choice (0-9): {RESET}"))
                break
            except ValueError:
                print(f"{RED}Please enter a number from 0 to 9.{RESET}")


        print()

        actions = {
            0: exit_program,
            1: list_movies,
            2: add_movie,
            3: delete_movie,
            4: update_movie,
            5: movie_stats,
            6: random_movie,
            7: search_movie,
            8: movies_rating,
            9: generate_website
        }

        action = actions.get(user_choice)
        if action:
            action()
        else:
            print(f"{RED}Invalid input{RESET}")


def exit_program():
    """Print a goodbye message and exit the program."""

    print("Bye!")
    exit()


def list_movies():
    """Retrieve all movies from the SQL database and print their title, year, and rating."""

    movies = storage.list_movies()
    print(f"{MAGENTA} {len(movies)} movies in total {RESET}")
    print(f"{YELLOW} {20 * '-' }{RESET}")
    for title, movie_data in movies.items():
        print(f"{MAGENTA}{title} ({movie_data['year']}): {movie_data['rating']}{RESET}")


def add_movie():
    """Ask for a movie title, fetch movie data from OMDb API, and add it to the SQL database."""

    movies = storage.list_movies()

    movie = helper_file.get_valid_text(f"{GREEN}Enter movie to add: {RESET}")

    if movie in movies:
        print(f"{RED} Movie already exists. {RESET}")
        return

    url = "http://www.omdbapi.com/"
    params = {
        "apikey": API_KEY,
        "t": movie
    }

    try:
        response = requests.get(url, params=params)
        movie_data = response.json()

        if movie_data.get("Response") == "False":
            print(f"{RED}Movie not found.{RESET}")
            return

        title = movie_data["Title"]
        year = int(movie_data["Year"])
        rating = float(movie_data["imdbRating"])
        poster = movie_data["Poster"]

        storage.add_movie(title, year, rating, poster)

    except requests.exceptions.RequestException:
        print(f"{RED}Could not connect to OMDb API.{RESET}")
    except ValueError:
        print(f"{RED}Could not read movie year or rating correctly.{RESET}")
    except KeyError:
        print(f"{RED}Missing movie data from API response.{RESET}")


def delete_movie():
    """Ask the user for a movie title and delete it from the SQL database."""

    movies = storage.list_movies()

    while True:
        movie = helper_file.get_valid_text(f"{GREEN}Enter movie to delete: {RESET}")

        if movie not in movies:
            print(f"{RED}The movie is not in the list. {RESET}")
        else:
            storage.delete_movie(movie)

            break




def update_movie():
    """Ask the user for a movie title and update its rating in the SQL database."""

    movies = storage.list_movies()

    while True:
        movie = helper_file.get_valid_text(f"{GREEN}Enter movie to update: {RESET}")

        if movie not in movies:
            print(f"{RED}The movie is not in the list. {RESET}")
        else:
            rating = helper_file.get_valid_float(f"{GREEN}Enter rating for movie: {RESET}")
            storage.update_movie(movie, rating)

            break


def movie_stats():
    """Retrieve all movies from the SQL database and print rating statistics."""

    movies = storage.list_movies()

    if not movies:
        print(f"{RED}No movies found.{RESET}")
        return

    rating_list = []

    for movie_data in movies.values():
        rating_list.append(movie_data["rating"])


    average_rating = round(sum(rating_list)/len(rating_list), 2)
    median_rating = round(statistics.median(rating_list),2)
    print(f"{BOLD}{YELLOW}Movie Stats{RESET}")
    print(f"- The {UNDERLINE}average{RESET} rating of the movies is: {BOLD}{average_rating}{RESET}")
    print(f"- The {UNDERLINE}median{RESET} rating of the movies is: {BOLD}{median_rating}{RESET}")

    best_rated_movies = []
    worst_rated_movies = []
    best_movie_rating = max(rating_list)
    worst_movie_rating = min(rating_list)

    for movie, movie_data in movies.items():
        if movie_data["rating"] == best_movie_rating:
            best_rated_movies.append({"title": movie, "rating": movie_data["rating"]})
        if movie_data["rating"] == worst_movie_rating:
            worst_rated_movies.append({"title": movie, "rating": movie_data["rating"]})

    if len(best_rated_movies) == 1:
        print(f"- The {UNDERLINE}best{RESET} rated movie is {BOLD} {best_rated_movies[0].get('title')}, {best_rated_movies[0].get('rating')} {RESET}")
    else:
        print(f"- The {UNDERLINE}best{RESET} rated movies are: " )
        for movie in best_rated_movies:
            print (f" {BOLD} {movie.get('title')}, {movie.get('rating')} {RESET}")

    if len(worst_rated_movies) == 1:
        print(f"- The {UNDERLINE}worst{RESET} rated movie is {BOLD} {worst_rated_movies[0].get('title')}, {worst_rated_movies[0].get('rating')} {RESET}")
    else:
        print(f"- The {UNDERLINE}worst{RESET} rated movies are: " )
        for movie in worst_rated_movies:
            print (f" {BOLD} {movie.get('title')}, {movie.get('rating')} {RESET}")





def random_movie():
    """Retrieve all movies from the SQL database and print one random movie with its rating."""

    movies = storage.list_movies()

    if not movies:
        print(f"{RED}No movies found.{RESET}")
        return

    random_choice = random.choice(list(movies))
    print(f"Here is a random movie choice for you: {BOLD}{random_choice}{RESET}. It is rated with: {BOLD}{movies[random_choice]['rating']}{RESET}.")

def search_movie():
    """Ask for part of a title and print all matching movies from the SQL database."""

    movies = storage.list_movies()

    movie_part = helper_file.get_valid_text(
        f"{GREEN}Enter part of movie name: {RESET}").strip().lower()

    for movie, movie_data in movies.items():
        if movie_part in movie.lower():
            print(f"{MAGENTA}{movie} ({movie_data['year']}): {movie_data['rating']}{RESET}")


def movies_rating():
    """Retrieve all movies from the SQL database and print them sorted by rating."""

    movies = storage.list_movies()
    print(f"{BOLD}{YELLOW}Movies sorted by rating{RESET}")

    sorted_movies = sorted(movies.items(), key=lambda v: v[1]["rating"], reverse=True)

    for movie, movie_data in sorted_movies:
        print(f"{MAGENTA}{movie} ({movie_data['year']}): {movie_data['rating']}{RESET}")


def generate_website():
    """Generate an HTML website from the movies stored in the SQL database."""

    movies = storage.list_movies()

    movie_grid = ""

    for title, movie_data in movies.items():
        movie_grid += f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{movie_data['poster']}" alt="{title} poster"/>
                <div class="movie-title">{title}</div>
                <div class="movie-year">{movie_data['year']}</div>
            </div>
        </li>
        """

    with open("_static/index_template.html", "r", encoding="utf-8") as template_file:
        template = template_file.read()

    html_content = template.replace("__TEMPLATE_TITLE__", "My Movie App")
    html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    with open("_static/index.html", "w", encoding="utf-8") as output_file:
        output_file.write(html_content)

    print("Website was generated successfully.")


def main():
    """Start the movie database program."""

    user_menu()


if __name__ == "__main__":
    main()


