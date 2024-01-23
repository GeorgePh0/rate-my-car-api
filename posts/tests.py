from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='andrew', password='Pass')

    def test_can_list_posts(self):
        andrew = User.objects.get(username='andrew')
        Post.objects.create(owner=andrew, title='andrew title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='andrew', password='Pass')
        response = self.client.post('/posts/', {'title': 'andrew title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'andrew title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        andrew = User.objects.create_user(username='andrew', password='Pass')
        alex = User.objects.create_user(username='alex', password='Pass')
        Post.objects.create(
            owner=andrew, title='andrew title', content='andrews content'
        )
        Post.objects.create(
            owner=alex, title='alex title', content='alexs content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'andrew title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='andrew', password='Pass')
        response = self.client.put('/posts/1/', {'title': 'andrews new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'andrews new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='andrew', password='Pass')
        response = self.client.put('/posts/2/', {'title': 'andrews new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)