from django.test import TestCase
from guests.models import Guest, Group, Category

class GuestViewsTest(TestCase):
    fixtures = ['rsvp_test.json']
    
    def loadGroup(self, id):
        self.group = Group.objects.get(pk=id)
        
    def assertEmailWasInvalid(self, response):
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'guests/index.html')
        self.assertEquals(response.context[0]['error'], True)        
    
    def assertStage2Succeeded(self):
        """ 
        Posts to stage 2 as expected, and does generic assertions on it.
        
        Returns the response object.
        """
        response = self.client.post('/rsvp/stage2', { 'email': self.group.email })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'guests/stage2.html')
        self.assertEquals(response.context[0]['group'], self.group)
        self.assertContains(response, ('Hi %s!' % self.group.name), 1)
        
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
        self.loadGroup(1)
        
        response = self.assertStage2Succeeded()        
        self.assertContains(response, 'Meal', 2)
    
    def testStage2WithValidEmailAndGuestNotInvitedToMeal(self):
        self.loadGroup(2)
        
        response = self.assertStage2Succeeded()
        self.assertNotContains(response, 'Meal')
        
    def testSaveWithInvalidEmail(self):
        response = self.client.post('/rsvp/save', { 'email': 'nobody@example.org'})
        self.assertEmailWasInvalid(response)
        
    def testSaveWithValidEmail(self):
        self.loadGroup(1)
        response = self.client.post('/rsvp/save', { 'email': self.group.email, 
                                                    '1_ceremony': '1', '1_meal': '0', '1_reception': '1',
                                                    '2_ceremony': '0', '2_meal': '0', '2_reception': '1' })
        
        # Reload the guest to get current state
        self.loadGroup(1)
        
        self.assertRedirects(response, '/rsvp/confirmed')
        guests = self.group.guest_set.all()
        
        self.assertEquals(self.group.rsvp_received, True)
        
        self.assertEquals(guests[0].attending_ceremony, True)
        self.assertEquals(guests[0].attending_meal, False)
        self.assertEquals(guests[0].attending_reception, True)
        
        self.assertEquals(guests[1].attending_ceremony, False)
        self.assertEquals(guests[1].attending_meal, False)
        self.assertEquals(guests[1].attending_reception, True)