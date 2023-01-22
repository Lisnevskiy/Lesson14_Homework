import sqlite3


def find_movie_by_title(search_title):
    """
    Принимает название фильма и возвращает самый свежий фильм из БД
    :param search_title: str(название фильма)
    :return: dict(название, страна, год выпуска, жанр, описание)
    """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()

        query = f"""
        SELECT title, country, release_year, listed_in, description 
        FROM netflix
        WHERE lower(title) LIKE '%{search_title}%'
        AND type = 'Movie'
        ORDER BY release_year DESC 
        LIMIT 1
        """

        cursor.execute(query)
        result = cursor.fetchall()
        result_dict = {
            "title": result[0][0],
            "country": result[0][1],
            "release_year": result[0][2],
            "genre": result[0][3],
            "description": result[0][4]
        }

    return result_dict


def find_by_range(first_value, second_value):
    """
    Принимает два года и возвращает список фильмов с годом выпуска
    :param first_value: целое число
    :param second_value: целое число
    :return: список словарей(название, год выпуска)
    """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()

        query = f"""
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN {first_value} AND {second_value}
        AND type = 'Movie'
        ORDER BY release_year DESC 
        LIMIT 100
        """

        cursor.execute(query)
        result = cursor.fetchall()
        range_result = []
        for row in result:
            row_dict = {"title": row[0], "release_year": row[1]}
            range_result.append(row_dict)
    return range_result


def search_by_rating(movie_ratings):
    """
    Принимает список рейтингов и возвращает данные в формате json
    :param movie_ratings: list(список рейтингов)
    :return: json(название, рейтинг, описание)
    """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()

        query = f"""
        SELECT title, rating, description
        FROM netflix
        WHERE type = 'Movie'
        AND rating = 'G' OR rating = 'PG' OR rating = 'PG-13' OR rating = 'R' OR rating = 'NC-17'
        """

        cursor.execute(query)
        result = cursor.fetchall()
        movie_list = []
        for row in result:
            if row[1] in movie_ratings:
                row_dict = {"title": row[0], "rating": row[1], "description": row[2]}
                movie_list.append(row_dict)
    return movie_list


def search_movies_by_genre(search_genre):
    """
    Принимает название жанра и возвращает 10 самых свежих фильмов в формате json.
    :param search_genre: str(название жанра)
    :return: json(название, описание)
    """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()

        query = f"""
        SELECT title, description 
        FROM netflix
        WHERE lower(listed_in) LIKE '%{search_genre}%'
        AND type = 'Movie'
        ORDER BY release_year DESC 
        LIMIT 10
        """

        cursor.execute(query)
        result = cursor.fetchall()
        result_list = []
        for row in result:
            row_dict = {"title": row[0], "description": row[1]}
            result_list.append(row_dict)
    return result_list


def find_by_cast(first_actor, second_actor):
    """
    Принимает имена двух актеров и возвращает список актеров, играющих с ними в паре больше 2 раз
    :param first_actor: str(имя первого актера)
    :param second_actor: str(имя второго актера)
    :return: list(список актеров)
    """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()

        query = f"""
        SELECT netflix.cast
        FROM netflix
        WHERE netflix.cast != ''
        AND netflix.cast LIKE '%{first_actor}%'
        AND netflix.cast LIKE '%{second_actor}%'
        """

        cursor.execute(query)
        result = cursor.fetchall()

        actors = ''
        all_actors = []
        actors_dict = {}
        actors_in_couple = []

        # Создаем строку актеров, перечисленных через запятую
        for row in result:
            for string in row:
                actors += f'{string}, '

        # Добавляем в all_actors актеров сыгравших в паре с first_actor и second_actor не более 1 раза
        #           в actors_dict актеров сыгравших в паре с first_actor и second_actor 2 или более раза
        for actor in actors.rstrip(', ').split(', '):
            if actor in all_actors:
                if actor in actors_dict:
                    actors_dict[actor] += 1
                else:
                    actors_dict[actor] = 2
            else:
                all_actors.append(actor)

        # Удаляем из словаря actors_dict первого и второго актера, если они там есть
        if first_actor in actors_dict:
            del actors_dict[first_actor]
        if second_actor in actors_dict:
            del actors_dict[second_actor]

        # Добавляем в actors_in_couple актеров сыгравших в паре с first_actor и second_actor более 2 раз
        [actors_in_couple.append(act) for act in actors_dict if actors_dict[act] > 2]

    if actors_in_couple:
        return f'Эти актеры {actors_in_couple} сыграли в паре с {first_actor} и {second_actor} более 2 раз'
    else:
        return f'Нет актеров сыгравших в паре с {first_actor} и {second_actor} более 2 раз'


def find_by_type(required_type, year, genre):
    """
    Принимает тип картины, год выпуска, жанр и возвращает список фильмов в формате json.
    :param required_type: str(тип)
    :param year: int(год выпуска)
    :param genre: str(название жанра)
    :return: json(название, описание)
    """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()

        query = f"""
        SELECT title, description
        FROM netflix
        WHERE lower(type) LIKE '%{required_type}%'
        AND release_year = {year}
        AND lower(listed_in) LIKE '%{genre}%'
        """

        cursor.execute(query)
        result = cursor.fetchall()
        range_result = []
        for row in result:
            row_dict = {"title": row[0], "description": row[1]}
            range_result.append(row_dict)
    return range_result
