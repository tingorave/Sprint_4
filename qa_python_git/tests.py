import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


# --- add_new_book ---


@pytest.mark.parametrize(
    'name, should_add',
    [
        ('Хоббит', True),          # обычное имя
        ('x' * 40, True),          # граничное значение: 40 символов
        ('', False),               # пустое имя
        ('x' * 41, False),         # 41 символ
    ]
)
def test_add_new_book_name_length_and_empty(collector, name, should_add):
    collector.add_new_book(name)

    if should_add:
        assert name in collector.get_books_genre()
    else:
        assert name not in collector.get_books_genre()


def test_add_new_book_duplicate_not_added_twice(collector):
    collector.add_new_book('Дюна')
    collector.add_new_book('Дюна')

    assert list(collector.get_books_genre().keys()).count('Дюна') == 1


# --- set_book_genre + get_book_genre ---


def test_set_book_genre_only_from_available_list(collector):
    collector.add_new_book('Дюна')
    collector.set_book_genre('Дюна', 'Фантастика')       # валидный жанр
    collector.set_book_genre('Дюна', 'Неизвестный жанр')  # невалидный жанр

    # жанр не должен смениться на невалидный
    assert collector.get_book_genre('Дюна') == 'Фантастика'


def test_new_book_has_no_genre_by_default(collector):
    collector.add_new_book('Гарри Поттер')
    assert collector.get_book_genre('Гарри Поттер') == ''


# --- get_books_with_specific_genre ---


def test_get_books_with_specific_genre_returns_only_that_genre(collector):
    collector.add_new_book('Дюна')
    collector.set_book_genre('Дюна', 'Фантастика')

    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Ужасы')

    books = collector.get_books_with_specific_genre('Фантастика')

    assert 'Дюна' in books
    assert 'Оно' not in books


# --- get_books_genre ---


def test_get_books_genre_returns_full_dict(collector):
    collector.add_new_book('Дюна')
    collector.set_book_genre('Дюна', 'Фантастика')

    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Ужасы')

    result = collector.get_books_genre()
    assert result == {'Дюна': 'Фантастика', 'Оно': 'Ужасы'}


# --- get_books_for_children (книги с возрастным рейтингом отсутствуют) ---


def test_books_with_age_rating_not_in_children_list(collector):
    # жанры с рейтингом: 'Ужасы', 'Детективы'
    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Ужасы')

    collector.add_new_book('Шерлок Холмс')
    collector.set_book_genre('Шерлок Холмс', 'Детективы')

    collector.add_new_book('История игрушек')
    collector.set_book_genre('История игрушек', 'Мультфильмы')

    children_books = collector.get_books_for_children()

    assert 'История игрушек' in children_books
    assert 'Оно' not in children_books
    assert 'Шерлок Холмс' not in children_books


# --- add_book_in_favorites + delete_book_from_favorites + get_list_of_favorites_books ---


def test_add_and_delete_book_in_favorites_flow(collector):
    collector.add_new_book('Дюна')
    collector.add_new_book('История игрушек')

    collector.add_book_in_favorites('Дюна')
    collector.add_book_in_favorites('История игрушек')
    collector.add_book_in_favorites('Дюна')  # повторно, не должен продублироваться

    favorites = collector.get_list_of_favorites_books()
    assert len(favorites) == 2
    assert 'Дюна' in favorites and 'История игрушек' in favorites

    collector.delete_book_from_favorites('Дюна')
    favorites_after_delete = collector.get_list_of_favorites_books()

    assert 'Дюна' not in favorites_after_delete
    assert 'История игрушек' in favorites_after_delete