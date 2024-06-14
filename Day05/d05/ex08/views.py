from django.shortcuts import render, redirect
import psycopg2
from django.http import HttpResponse
from django.conf import settings

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
            CREATE TABLE ex08_planets(
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                climate VARCHAR,
                diameter INT,
                orbital_period INT,
                population BIGINT,
                rotation_period INT,
                surface_water REAL,
                terrain VARCHAR(128)
            );

            CREATE TABLE ex08_people(
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                birth_year VARCHAR(32),
                gender VARCHAR(32),
                eye_color VARCHAR(32),
                hair_color VARCHAR(32),
                height INT,
                mass REAL,
                homeworld VARCHAR(64) REFERENCES ex08_planets(name)
            );
            ''')

        # Commit et fermeture de la connexion
        conn.commit()

        return HttpResponse("OK")

    except Exception as e:
        return HttpResponse(f"Error: {e}")


def parse_planet(line: str):
    line = line.split('	')
    planet = {
        'name': line[0].strip() if line[0].strip() != 'NULL' else None,
        'climate': line[1].strip() if line[1].strip() != 'NULL' else None,
        'diameter': line[2].strip() if line[2].strip() != 'NULL' else None,
        'orbital_period': line[3].strip() if line[3].strip() != 'NULL' else None,
        'population': line[4].strip() if line[4].strip() != 'NULL' else None,
        'rotation_period': line[5].strip() if line[5].strip() != 'NULL' else None,
        'surface_water': line[6].strip() if line[6].strip() != 'NULL' else None,
        'terrain': line[7].strip() if line[7].strip() != 'NULL' else None,
    }
    return planet

def parse_people(line: str):
    line = line.split('	')
    people = {
        'name': line[0].strip() if line[0].strip() != 'NULL' else None,
        'birth_year': line[1].strip() if line[1].strip() != 'NULL' else None,
        'gender': line[2].strip() if line[2].strip() != 'NULL' else None,
        'eye_color': line[3].strip() if line[3].strip() != 'NULL' else None,
        'hair_color': line[4].strip() if line[4].strip() != 'NULL' else None,
        'height': line[5].strip() if line[5].strip() != 'NULL' else None,
        'mass': line[6].strip() if line[6].strip() != 'NULL' else None,
        'homeworld': line[7].strip() if line[7].strip() != 'NULL' else None,
    }
    return people


def populate(request):
    planets = []
    peoples = []
    try:
        conn = connect_bdd()
        with open('data/planets.csv') as f:
            lines = f.readlines()
            for line in lines:
                planets.append(parse_planet(line))
        with open('data/people.csv') as f:
            lines = f.readlines()
            for line in lines:
                peoples.append(parse_people(line))

        INSERT_PLANET = """
        INSERT INTO ex08_planets(name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        INSERT_PEOPLE = """
        INSERT INTO ex08_people(name, birth_year, gender, eye_color, hair_color, height, mass, homeworld)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        response = []
        
        with conn.cursor() as cur:
            for planet in planets:
                try:
                    cur.execute(INSERT_PLANET, [
                        planet['name'],
                        planet['climate'],
                        planet['diameter'],
                        planet['orbital_period'],
                        planet['population'],
                        planet['rotation_period'],
                        planet['surface_water'],
                        planet['terrain'],
                    ])
                    response.append("OK")
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    response.append(e)
            for people in peoples:
                try:
                    cur.execute(INSERT_PEOPLE, [
                        people['name'],
                        people['birth_year'],
                        people['gender'],
                        people['eye_color'],
                        people['hair_color'],
                        people['height'],
                        people['mass'],
                        people['homeworld'],
                    ])
                    response.append("OK")
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    response.append(e)
        return HttpResponse("<br/>".join(str(i) for i in response))
    except Exception as e:
        return HttpResponse(e)


def display(request):
    table_planets = "ex08_planets"
    table_people = "ex08_people"
    try:
        conn = connect_bdd()
    
        SELECT_TABLE = f"""
            SELECT
                {table_people}.name,
                {table_people}.homeworld,
                {table_planets}.climate
            FROM
                {table_planets}
                RIGHT JOIN {table_people}
                ON
                    {table_people}.homeworld = {table_planets}.name
                    where
                        {table_planets}.climate
                        LIKE '%windy%'
                ORDER BY {table_planets}.name;
            """
        with conn.cursor() as cur:
            cur.execute(SELECT_TABLE)
            datas = cur.fetchall()
        if len(datas) == 0:
            return HttpResponse("No data available")
        return render(request, 'ex08/display.html', {"datas": datas})

    except Exception as e:
        print(e)
        return HttpResponse("No data available")
