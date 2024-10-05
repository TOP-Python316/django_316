from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Card, Category, Tag


class CardModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='AnkiTestUser1',
            is_superuser=True
        )
        self.Category = Category.objects.create(
            name='test_category'
        )
        self.Tag = Tag.objects.create(
            name='test_tag'
        )
        self.card = Card.objects.create(
            question='test_question',
            answer='test_answer',
            category=self.Category,
            author=self.user,
            status=Card.Status.UNCHECKED
        )
        self.card.tags.add(self.Tag)

    def test_card_creation(self):
        self.assertEqual(self.card.question, 'test_question')
        self.assertEqual(self.card.answer, 'test_answer')
        self.assertEqual(self.card.category, self.Category)
        self.assertEqual(self.card.author, self.user)
        self.assertEqual(self.card.status, Card.Status.UNCHECKED)
        self.assertEqual(self.Tag, self.card.tags.all()[0])

    def test_card_str(self):
        self.assertEqual(str(self.card), f'Карточка {self.card.question} - {self.card.answer[:50]}')


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='test_category')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'test_category')

    def test_category_str(self):
        self.assertEqual(str(self.category), f'Категория {self.category.name}')


class TagModelTest(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name='test_tag')

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'test_tag')

    def test_tag_str(self):
        self.assertEqual(str(self.tag), f'Тег {self.tag.name}')


class CardViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='AnkiTestUser1'
        )
        self.category = Category.objects.create(name='test_category')
        self.tag = Tag.objects.create(name='test_tag')
        self.card = Card.objects.create(
            question='test_question',
            answer='test_answer',
            category=self.category,
            author=self.user,
            status=Card.Status.UNCHECKED
        )
        self.card.tags.add(self.tag)

    def test_catalog_view(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/catalog.html')

    def test_card_detail_view(self):
        response = self.client.get(reverse('detail_card_by_id', kwargs={'pk': self.card.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/card_detail.html')

    def test_add_card_view(self):
        self.client.login(username='testuser', password='AnkiTestUser1')
        self.assertTrue(self.client.login(username='testuser', password='AnkiTestUser1'))
        response = self.client.get(reverse('add_card'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/add_card.html')

    def test_edit_card_view(self):
        self.client.login(username='testuser', password='AnkiTestUser1')
        self.assertTrue(self.client.login(username='testuser', password='AnkiTestUser1'))
        response = self.client.get(reverse('edit_card', kwargs={'pk': self.card.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/add_card.html')

    def test_delete_card_view(self):
        self.client.login(username='testuser', password='AnkiTestUser1')
        self.assertTrue(self.client.login(username='testuser', password='AnkiTestUser1'))
        response = self.client.get(reverse('delete_card', kwargs={'pk': self.card.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/delete_card.html')
