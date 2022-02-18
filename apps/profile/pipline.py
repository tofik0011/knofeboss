from filebrowser.base import FileObject

from mainapp.helper import print_c, download
from unine_engine.globals import MEDIA_ROOT, MEDIA_URL
from django.core.files import File

#TODO Дописати щоб була асоціація з акаунтом.
def create_profile(user, is_new=False, *args, **kwargs):
    if is_new:
        print("test")
        # create a profile instance for the given user
        # create_user_profile(user)
    else:
        print("test1")

def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    url = None
    image_name = ""
    if backend.name == 'facebook':
        image_name = f'facebook_{response["id"]}.jpg'
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
        # if you need a square picture from fb, this line help you
        url = "http://graph.facebook.com/%s/picture?width=150&height=150" % response['id']
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')
    if backend.name == 'google-oauth2':
        pass
        # url = response['image'].get('url')
        # ext = url.split('.')[-1]
    if url:
        path_image = f'{MEDIA_ROOT}/profile/{image_name}'
        url_image = f'profile/{image_name}'
        download(url, path_image)
        user.picture = FileObject(url_image)
        user.save()
