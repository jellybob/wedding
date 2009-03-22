from django.test import TestCase
from guests.models import Guest

class RsvpTest(TestCase):
    fixtures = ['rsvp_test.json']
    
    def loadGuest(self, id):
        self.guest = Guest.objects.get(pk=id)
    def assertEmailWasInvalid(self, response):
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'guests/index.html')
        self.assertEquals(response.context[0]['error'], True)        
    
    def assertStage2Succeeded(self):
        """ 
        Posts to stage 2 as expected, and does generic assertions on it.
        
        Returns the response object.
        """
        response = self.client.post('/rsvp/stage2', { 'email': self.guest.email })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'guests/stage2.html')
        self.assertEquals(response.context[0]['guest'], self.guest)
        self.assertContains(response, ('Hi %s!' % self.guest.first_name), 1)
        return response
        
    def testIndex(self):
        response = self.client.get('/rsvp/')
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'guests/index.html')
        self.assertEquals(response.context[0]['error'], False)
        
    def testStage2WithInvalidEmail(self):
        response = self.client.post('/rsvp/stage2', { 'email': 'nobody@example.org'})
        self.assertEmailWasInvalid(response)
    
    def testStage2WithValidEmailAndGuestInvitedToMeal(self):
        self.loadGuest(1)
        
        response = self.assertStage2Succeeded()        
        self.assertContains(response, 'Meal', 1)
    
    def testStage2WithValidEmailAndGuestNotInvitedToMeal(self):
        self.loadGuest(2)
        
        response = self.assertStage2Succeeded()
        self.assertNotContains(response, 'Meal')
        
    def testSaveWithInvalidEmail(self):
        response = self.client.post('/rsvp/save', { 'email': 'nobody@example.org'})
        self.assertEmailWasInvalid(response)
        
    def testSaveWithValidEmail(self):
        self.loadGuest(1)
        response = self.client.post('/rsvp/save', { 'email': self.guest.email, 'ceremony': '1', 'meal': '0', 'reception': '1' })
        
        # Reload the guest to get current state
        self.loadGuest(1)
        
        self.assertRedirects(response, '/rsvp/confirmed')
        self.assertEquals(self.guest.attending_ceremony, True)
        self.assertEquals(self.guest.attending_meal, False)
        self.assertEquals(self.guest.attending_reception, True)