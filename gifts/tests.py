# coding=utf-8
from django.test import TestCase
from wedding.gifts.models import Gift

class GiftModelsTest(TestCase):
    def testPriceConversionToPoundsAndPenceWithEmptyPrice(self):
        g = Gift(price=None)
        self.assertEquals(None, g.price_in_pounds())
        
    def testPriceConversionToPoundsAndPence(self):
        g = Gift(price=2499)
        self.assertEquals("£24.99", g.price_in_pounds())
        
    def testPriceConversionToPoundsAndPenceWithSubOnePound(self):
        g = Gift(price=99)
        self.assertEquals("£0.99", g.price_in_pounds())
        
    def testImagePathGeneration(self):
        g = Gift(slug='something-nice', name="Something Nice")
        self.assertEquals("gifts/something-nice/example.png", Gift.generate_gift_path(g, "example.png"))

class GiftViewsTest(TestCase):
    fixtures = ["gifts_test.json"]
    
    def testIndex(self):
        response = self.client.get('/gifts/')
        gift = Gift.objects.get(pk=1)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gifts/index.html')
        self.assertNotEquals(response.context[0]['gifts'], [gift])
        self.assertContains(response, gift.name, 1)
        self.assertContains(response, gift.image, 1)
        self.assertContains(response, gift.description, 1)
        self.assertContains(response, gift.address, 1)