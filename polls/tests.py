from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta

from user.models import User
from .models import Poll, PollCategory, PollCategoryGroup, Candidate, Vote, RestrictionKey

class BreakOutError(Exception):
    pass

SMALL_GIF =  (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x01\x00\x2c\x00\x00\x02\x00\x02\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)

# Test Models
class PollTest(TestCase):
    def setUp(self):
        self.client = Client()
        #Create users 
        self.user = User.objects.create_user(
            username ="user1",
            password ="userpassword",
            first_name = "Kofi",
            last_name = "Aban",
            other_names = "Wood" ,
            email ="KofiAb@wood.com",
            country_code ="233", 
            phone_number ="123456789",
            profile_picture="test_image.jpg",
        )

        self.poll = Poll.objects.create(
            creator = self.user,
            name = "Test Poll One",
            image =  "test_image.jpg",
            active = False,
            hidden = False,
            closing_date = date.today() + timedelta(days=1),
            live_results = False,
            restrictionType = "specialKeys"
        )

        self.group = PollCategoryGroup.objects.create(
            poll = self.poll,
            name = "Test Group"
        )

        self.category = PollCategory.objects.create(
            poll = self.poll,
            name = "Test Category",
            group = self.group
        )
        self.category2 = PollCategory.objects.create(
            poll = self.poll,
            name = "Test Category Second",
            group = self.group
        )

        self.candidate1 = Candidate.objects.create(
            poll = self.poll,
            name = "Candidate One",
            image = "test_image.jpg",
            party = "Party A"
        )
        self.candidate1.categories_contesting.add(self.category)
        self.candidate1.categories_contesting.add(self.category2)

        self.candidate2 = Candidate.objects.create(
            poll = self.poll,
            name = "Candidate Two",
            image = "test_image.jpg",
            party = "Party B"
        )
        self.candidate2.categories_contesting.add(self.category)
        self.candidate2.categories_contesting.add(self.category2)
        
        self.key = RestrictionKey.objects.create(
            poll = self.poll,
            key = "1234"
        )

    def test_database(self):
        '''Testing Poll Database'''
        self.assertTrue(Poll.objects.all())
        self.assertTrue(PollCategoryGroup.objects.all())
        self.assertTrue(PollCategory.objects.all())
        self.assertEqual(Candidate.objects.all().count(),2)
        self.assertTrue(RestrictionKey.objects.all())

    def test_poll_name(self):
        try:
            Poll.objects.create(
                creator = self.user,
                name = "Test Poll One",
                image =  "test_image.jpg",
                active = True,
                hidden = False,
                closing_date = date.today() + timedelta(days=1),
                live_results = False,
                restrictionType = "oneKey"
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Poll with same name in database should have failed to save")
        except Exception as e:
            pass

    def test_group_name(self):
        try:
            PollCategoryGroup.objects.create(
                poll = self.poll,
                name = "Test Group",
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Group with same name in database should have failed to save")
        except Exception as e:
            pass

    def test_category_name(self):
        try:
            PollCategory.objects.create(
                poll = self.poll,
                name = "Test Category",
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Category with same name in database should have failed to save")
        except Exception as e:
            pass
    
    def test_launch_closing_date_today(self):
        self.poll.closing_date = date.today()
        try:
            self.poll.launch()
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Today as closing date should have failed launch")
        except Exception as e:
            pass

    def test_launch_empty_category(self):
        PollCategory.objects.create(
            poll = self.poll,
            name = "Test Category Two",
        )
        self.poll.launch()
        if PollCategory.objects.filter(name = "test category two"):
            raise Exception("Empty category should have been deleted")
        
    def test_launch_left_one_category_ungrouped(self):
        new_category = PollCategory.objects.create(
            poll = self.poll,
            name = "Test Category Two",
        )
        self.candidate2.categories_contesting.add(new_category)
        try:
            self.poll.launch()
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Ungrouped category while other is grouped should fail launch")
        except Exception as e:
            pass

    def test_launch_one_candidate_not_contending_any(self):
        Candidate.objects.create(
            poll = self.poll,
            name = "Candidate One",
            image = "test_image.jpg",
            party = "Party A"
        )
        try:
            self.poll.launch()
            raise BreakOutError()
        except BreakOutError:
            raise Exception("All candidates must contend a category")
        except Exception as e:
            pass

    def test_voting(self):
        Vote.objects.create(
            voter = self.user,
            poll = self.poll,
            category = self.category,
            candidate = self.candidate1
        )

        Vote.objects.create(
            voter = self.user,
            poll = self.poll,
            category = self.category2,
            candidate = self.candidate1
        )
       
        self.assertEqual(self.poll.votes.all().count(),2)
        self.assertEqual(self.category.votes.all().count(),1)
        self.assertEqual(self.category2.votes.all().count(),1)
        self.assertEqual(self.candidate1.votes.all().count(),2)

        try:
            Vote.objects.create(
                voter = self.user,
                poll = self.poll,
                category = self.category,
                candidate = self.candidate2
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Should not be able to vote in same category twice")
        except Exception as e:
            pass

    ##### Test Views #####
    def test_index_view(self):
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        response.context["polls"]

    def test_my_polls_view(self):
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.get("/myIndex/")
        self.assertEqual(response.status_code, 200)
        response.context["polls"]
        response.context['form']

        # Check Post requests
        try:
            # Invalid closing date
            response = self.client.post("/myIndex/", {
                    "name" : "Create New Poll",
                    "image" : SimpleUploadedFile("small.gif", SMALL_GIF , content_type='image/gif') ,
                    "closing_date" : date.today(),
                    "restrictionType" : "oneKey" 
            })
            self.assertEqual(response.status_code, 200)
            response.context['error_messages']
        except Exception as e:
            raise Exception(f"Create new poll, request failed;    {e}")

    def test_my_polls_2_view(self):
        # Correct adding new poll
        try:
            response = self.client.post("/myIndex/", {
                    "name" : "Create New Poll",
                    "image" : SimpleUploadedFile("small.gif", SMALL_GIF , content_type='image/gif') ,
                    "closing_date" : date.today() + timedelta(days=1),
                    "restrictionType" : "oneKey" 
            })
            self.assertEqual(response.status_code, 302)
        except Exception as e:
            raise Exception(f"Create new poll, request failed;    {e}")

    def test_get_groups_view(self):
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.get(f"/polls/getGroups/Test Poll One/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data[0]["name"],'test group')
    
    def test_categories_view(self):
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.get(f"/polls/getCategories/Test Poll One/test group/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data),2)
    
    def test_notGrouped_categories_view(self):
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.get(f"/polls/getCategories/Test Poll One/none/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data),2)

    def test_candidates_view(self):
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.get(f"/polls/getCandidates/Test Poll One/Test Category/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data),2)

        







    






        

