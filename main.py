import requests
import json

# 1.Получаем фотографии с профиля пользователя VK с помощью метода photos.get
user_id = "" #id пользователя VK
access_token = "" #действующий токен доступа VK
def get_vk_photos(user_id, access_token):
    response = requests.get('https://api.vk.com/method/photos.get', params={
        'owner_id': user_id,
        'album_id': 'profile',
        'rev': 1,
        'access_token': access_token,
        'v': '5.131'
    })
    photos_data = response.json()
    return photos_data['response']['items']

# 2.1Выбираем фотографии максимального размера
def get_max_size_photo(photos):
    max_size_photo = max(photos, key=lambda x: x['height']*x['width'])
    return max_size_photo
# 2.2 Сохранять фотографии на Я.Диске

def save_to_yandex_disk(photo_url, access_token):
    headers = {
        'Authorization': f'OAuth {access_token}'
    }
    response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', params={
        'url': photo_url,
        'path': '/photos/photo.jpg'
    }, headers=headers)
    if response.status_code == 202:
        print('Photo has been successfully saved to Yandex.Disk')
    else:
        print('Failed to save photo to Yandex.Disk')

    # 3. Добавляем сохранение фотографии с учетом количества лайков
    likes_count = 100  # Замените на реальное количество лайков для фотографии
    new_path = f'/photos/photo_with_{likes_count}_likes.jpg'
    response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', params={
        'url': photo_url,
        'path': new_path
    }, headers=headers)
    if response.status_code == 202:
        print(f'Photo with {likes_count} likes has been successfully saved to Yandex.Disk')
    else:
        print('Failed to save photo with likes to Yandex.Disk')

user_id = "" #id пользователя VK
access_token_vk = "" #действующий токен доступа VK
access_token_yandex = "" #действующий токен доступа Я.Диск

photos = get_vk_photos(user_id, access_token_vk)
max_size_photo = get_max_size_photo(photos)
photo_url = max_size_photo['photo_604']

save_to_yandex_disk(photo_url, access_token_yandex)

# 4.Создаем json-файл с информацией о фотографиях
def create_json_file(photos):
    with open('photos_info.json', 'w') as json_file:
        json.dump(photos, json_file)

# Основной код
if __name__ == "__main__":
    user_id = "" #id пользователя VK
    access_token_vk = "" #действующий токен доступа VK
    access_token_yandex_disk = "" #действующий токен доступа Я.Диск

    photos = get_vk_photos(user_id, access_token_vk)
    max_size_photo = get_max_size_photo(photos)
    save_to_yandex_disk(max_size_photo, access_token_yandex_disk)
    create_json_file(photos)