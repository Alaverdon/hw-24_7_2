from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_invalid_key(email=valid_email, password='12345'):
    """Провряем что запрос API ключа для неправильного пароля не возвращает статус 200"""

    status, result = pf.get_api_key(email, password)

    assert status != 200
    print(status)


def test_get_api_key_for_invalid_user(email='88005553535@mail.ru', password=valid_password):
    """Проверяем что запрос API ключа для неправильного логина не возвращает статус 200"""

    status, result = pf.get_api_key(email, password)

    assert status != 200
    print(status)


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем что запрос API ключа возвращает статус 200 и в результате содержится слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех пэтов возвращает не пустой список. """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Шархан', animal_type='Sibirian',
                                     age='1', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить пета с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_data_name(name='', animal_type='Sibirian',
                                            age='1', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить пэта с некорректными данными - (данные в обязательном поле 'имя питомца') """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200
    print(status)


def test_add_new_pet_with_invalid_data_age(name='Холо', animal_type='волчица',
                                           age='', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить пэта с некорректными данными - (данные в обязательном поле 'возраст') """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200
    print(status)


def test_add_new_pet_with_invalid_data_animal_type(name='Щегол', animal_type='',
                                                   age='1', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить пэта с некорректными данными - (данные в обязательном поле 'порода') """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200
    print(status)


def test_successful_delete_self_pet():
    """Проверяем возможность удаления пэта"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Ленин', animal_type='Черепах', age=5):
    """Проверяем возможность обновления информации о пэте"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_unsuccessful_update_self_pet_info_without_name(name='', animal_type='Собака', age=4):
    """Проверяем невозможность обновления информации о пэте с некорректными данными -
    (пустое поле 'имя питомца') """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status != 200
        print(status)
    else:

        raise Exception("There is no my pets")


def test_unsuccessful_update_self_pet_info_without_age(name='Алиса', animal_type='Лиса', age=''):
    """Проверяем невозможность обновления информации о пэте с некорректными данными -
      (пустое поле 'возраст питомца') """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status != 200
        print(status)
    else:
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo_with_valid_data(name='Бармаглот', animal_type='Котэ',
                                                   age='2'):
    """Проверяем что можно добавить пэта без фото с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_new_pet_without_photo_with_invalid_data_name(name='', animal_type='Котэ',
                                                          age='2'):
    """Проверяем что нельзя добавить пэта без фото с некорректными данными -
     (пустое поле 'имя питомца') """

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status != 200
    print(status)


def test_add_new_pet_without_photo_with_invalid_data_age(name='Бздун', animal_type='Котэ',
                                                         age=''):
    """Проверяем что нельзя добавить пета без фото с некорректными данными -
        (пустое поле 'возраст') """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    print(status)


def test_add_new_pet_without_photo_with_invalid_data_animal_type(name='Cheshir', animal_type='',
                                                                 age='3'):
    """Проверяем что нельзя добавить пэта без фото с некорректными данными -
        (невозможность передать пустое поле 'порода') """

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status != 200
    print(status)


def test_add_pet_photo_with_valid_data(pet_photo='images/123.jpg'):
    """Проверяем что можно добавить фото пэта с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    assert status == 200
    assert result['pet_photo'] != 0


def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос моих пэтов, при наличии пэтов на сайте, возвращает не пустой список. """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем нового питомца, для уверенности, что список пэтов на сайте не пустой.
    pf.add_new_pet(auth_key, "Вурдалак", "кот", "2", "images/cat1.jpg")

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0
