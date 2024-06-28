from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from watchlist.models import StreamPlatform, WatchList, Review

class StreamPlatformTestCase(APITestCase):
    def setUp(self) -> None:
         self.platform = StreamPlatform.objects.create(
            name="Alt tv",
            about="Entertainment OTT",
            website="https://alttv.com"
        )
    
    def test_create_platform(self):
        data = {
            "name": "Alt tv",
            "about": "Entertaintment OTT",
            "website": "https://alttv.com"
        }
        response = self.client.post(reverse('platform-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_platform(self):
        response = self.client.get(reverse('platform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_platform(self):
        response = self.client.get(reverse('platform-detail', args=[self.platform.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_platform(self):
        data = {
            "name": "Alt tv Updated",
            "about": "Updated Entertainment OTT",
            "website": "https://updatedalttv.com"
        }
        response = self.client.put(reverse('platform-detail', args=[self.platform.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.platform.refresh_from_db()
        self.assertEqual(self.platform.name, data['name'])
        self.assertEqual(self.platform.about, data['about'])
        self.assertEqual(self.platform.website, data['website'])
    
    def test_delete_platform(self):
        response = self.client.delete(reverse('platform-detail', args=[self.platform.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class WatchListTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testcase', password='testcase@123')
        data = {
            "username": "testcase",
            "password": "testcase@123"
        }
        response = self.client.post(reverse('token_obtain_pair'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.platform = StreamPlatform.objects.create(
            name="Alt tv",
            about="Entertainment OTT",
            website="https://alttv.com"
        )

        self.watchlist = WatchList.objects.create(
            platform = self.platform,
            title = "movies test case",
            storyline = "test case story",
            active = True
        )
    
    def test_list_watchlist(self):
        response = self.client.get(reverse('watch-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    '''
    def test_create_watchlist(self):
        data = {
            "platform": self.platform.id,
            "title": "Krish three",
            "storyline": "Udane wala insaan with black cloth",
            "active": True
        }
        response = self.client.post(reverse('watch-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    '''
    
class ReviewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testcase', password='testcase@123')
        data = {
            "username": "testcase",
            "password": "testcase@123"
        }
        response = self.client.post(reverse('token_obtain_pair'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.platform = StreamPlatform.objects.create(
            name="Alt tv",
            about="Entertainment OTT",
            website="https://alttv.com"
        )

        self.watchlist = WatchList.objects.create(
            platform = self.platform,
            title = "movies test case",
            storyline = "test case story",
            active = True
        )

        self.watchlist2 = WatchList.objects.create(
            platform = self.platform,
            title = "movies test case",
            storyline = "test case story",
            active = True
        )

        self.review = Review.objects.create(
            user = self.user,
            rating = 4,
            description = "Not bad",
            watchlist = self.watchlist2,
            active = True
        )
    
    def test_create_review(self):
        data = {
            "user": self.user.id,
            "rating": 4,
            "description": "Not bad",
            "watchlist": self.watchlist.id,
            "active": True
        }

        response = self.client.post(reverse('review-create', args=[self.watchlist.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)

    def test_update_review(self):
        data = {
            "user": self.user.id,
            "rating": 5,
            "description": "Not bad - updated",
            "watchlist": self.watchlist.id,
            "active": False
        }
        
        response = self.client.put(reverse('review-detail', args=[self.review.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.description, "Not bad - updated")
        self.assertFalse(self.review.active)

    def test_list_review(self):
        response = self.client.get(reverse('review-list', args=[self.watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_review(self):
        response = self.client.get(reverse('review-detail', args=[self.review.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)