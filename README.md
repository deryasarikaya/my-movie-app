# My Movie App

A Python movie database application with SQLite storage, OMDb API integration, and dynamic HTML website generation.

## Features

* Add movies using the OMDb API
* Store movie data in SQLite
* Generate a movie website automatically
* Display movie posters
* Search movies
* Random movie suggestions
* Movie statistics
* Sort movies by rating

## Technologies Used

* Python
* SQLite
* SQLAlchemy
* OMDb API
* HTML & CSS
* Git & GitHub

## Project Structure

```plaintext
data/       -> SQLite database
storage/    -> Database logic
_static/    -> HTML and CSS files
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your OMDb API key:

```plaintext
API_KEY=your_api_key
```

## Usage

Run the application:

```bash
python app.py
```

Use the terminal menu to:

* Add movies
* Delete movies
* View statistics
* Generate a website

## Generate Website

The application can generate a movie website automatically.

Generated file:

```plaintext
_static/index.html
```
