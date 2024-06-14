from django.shortcuts import render, redirect
import psycopg2
from django.http import HttpResponse
from django.conf import settings
from .forms import DropdownMovieForm

def connect_bdd():
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        return conn
    except Exception as e:
        raise e

def init(request):
    try:
        conn = connect_bdd()
        with conn.cursor() as cur:
            # Création de la table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS ex06_movies (
                    title VARCHAR(64) UNIQUE NOT NULL,
                    episode_nb INT PRIMARY KEY,
                    opening_crawl TEXT,
                    director VARCHAR(32) NOT NULL,
                    producer VARCHAR(128) NOT NULL,
                    release_date DATE NOT NULL,
                    created TIMESTAMP NOT NULL DEFAULT NOW(),
                    updated TIMESTAMP NOT NULL DEFAULT NOW()
                );
                CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                RETURNS TRIGGER AS $$
                BEGIN
                NEW.updated = now();
                NEW.created = OLD.created;
                RETURN NEW;
                END;
                $$ language 'plpgsql';
                CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
                ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
                update_changetimestamp_column();
            ''')

        # Commit et fermeture de la connexion
        conn.commit()

        return HttpResponse("OK")

    except Exception as e:
        return HttpResponse(f"Error: {e}")

def populate(request):
    movies = [
        {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick mcCallum",
            "release_date": "1999-05-19",
        },
        {
            "episode_nb": 2,
            "title": "Attack of the Clones",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16"
        },
        {
            "episode_nb": 3,
            "title": "Revenge of the Sith",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19"
        },
        {
            "episode_nb": 4,
            "title": "A New Hope",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25"
        },
        {
            "episode_nb": 5,
            "title": "The Empire Strikes Back",
            "director": "Irvin Kershner",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1980-05-17"
        },
        {
            "episode_nb": 6,
            "title": "Return of the Jedi",
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25"
        },
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11"
        }
    ]
    try:
        conn = connect_bdd()

        INSERT_DATA = """
        INSERT INTO ex06_movies(episode_nb, title, director, producer, release_date)
        VALUES (%s, %s, %s, %s, %s)
        """

        response = []

        for movie in movies:
            try:
                with conn.cursor() as cur:
                    cur.execute(INSERT_DATA, [
                        movie["episode_nb"],
                        movie["title"],
                        movie["director"],
                        movie["producer"],
                        movie["release_date"]
                    ])
                conn.commit()
                response.append("OK")
            except Exception as e:
                conn.rollback() # annule les dernières modifications
                response.append(e)
        return HttpResponse("<br>".join(str(i) for i in response))
    except Exception as e:
        return HttpResponse(e)


def display(request):
    try:
        conn = connect_bdd()
    
        SELECT_TABLE = """
        SELECT * FROM ex06_movies
        """
        with conn.cursor() as cur:
            cur.execute(SELECT_TABLE)
            movies = cur.fetchall()
        if len(movies) == 0:
            return HttpResponse("No data available")
        return render(request, 'ex06/display.html', {"movies": movies})

    except Exception as e:
        print(e)
        return HttpResponse("No data available")

def update(request):
    try:
        conn = connect_bdd()

        if request.method == "GET":
            SELECT_TABLE = """
            SELECT * FROM ex06_movies
            """

            with conn.cursor() as cur:
                cur.execute(SELECT_TABLE)
                movies = cur.fetchall()
            if len(movies) == 0:
                return HttpResponse("No data available")
            context = {'form': DropdownMovieForm(choices=((movie[0], movie[0]) for movie in movies))}
            return render(request, 'ex06/update.html', context)
        
        elif request.method == "POST":
            SELECT_TABLE = """
            SELECT * FROM ex06_movies
            """

            with conn.cursor() as cur:
                cur.execute(SELECT_TABLE)
                movies = cur.fetchall()
            if len(movies) == 0:
                return HttpResponse("No data available")
            choices = ((movie[0], movie[0]) for movie in movies)

            data = DropdownMovieForm(choices, request.POST)
            if data.is_valid() == True:
                UPDATE_SQL = f"""
                UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s
                """
                with conn.cursor() as cur:
                    cur.execute(UPDATE_SQL, [data.cleaned_data['opening_crawl'], data.cleaned_data['movie']])
                conn.commit()
            return redirect(request.path)    
    
    except Exception as e:
        print(e)
        return HttpResponse("No data vailable")
