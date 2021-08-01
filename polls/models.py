import os
from django.conf import settings
from django.db import models
from django.urls import reverse
from datetime import date
from django.db.models import Count


# Handles where to save images for candidates
def poll_candidates_image_upload_dir(instance, filename):
    return os.path.join(settings.BASE_DIR, f'media/polls/{instance.poll.name}/{instance.name}', filename)

# Handles where to save images for polls
def poll_image_upload_dir(instance, filename):
    return os.path.join(settings.BASE_DIR, f'media/polls/{instance.name}', filename)

# Poll creation
class Poll(models.Model):
    # restrict access by ip or one key for all or special key by each voter
    RESTRICTION_TYPE = (
        ('oneKey','oneKey'),
        ('specialKeys','specialKeys'),
        ('none','none'),
    )
    creator = models.ForeignKey("user.User", on_delete=models.CASCADE ,null=True)
    name = models.CharField(max_length=100, unique=True)
    image =  models.ImageField(null=True,blank=True,upload_to=poll_image_upload_dir, max_length =500)
    active = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    closing_date = models.DateField(null=True)
    live_results = models.BooleanField(default=False)
    restrictionType = models.CharField(max_length=30, choices=RESTRICTION_TYPE, null=True, blank=True, default="none")

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "is_active":self.active,
            "hidden":self.hidden,
            "closing_date":self.closing_date,
            "restrictionType": self.restrictionType,
            "live_results": self.live_results
        }

    # Go to actual voting page
    def get_absolute_url(self):
        return reverse("polls:voting_page",kwargs={"poll_name":self.name})
    
    # Go to voting page preview, no voting
    def preview_url(self):
        return reverse("polls:voting_pagePreview",kwargs={"poll_name":self.name,"preview":True})
    
    # Go to settings and management
    def manage_poll_url(self):
        return reverse("polls:poll_management",kwargs={"poll_name":self.name,"view":"categories"})
    
    # Go to results page 
    def get_poll_results_url(self):
        return reverse("polls:resultsPage",kwargs={"poll_name":self.name})

    # Check poll deadline
    def deadline(self):
        if not self.active:
            return False
        # print("checking poll closing date")
        if date.today() >= self.closing_date:
            self.active = False
            self.save()

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        # if new object
        if self._state.adding:
            if self.closing_date <= date.today():
                raise Exception("Closing date be atleast a day ahead")
        if self.restrictionType == "none" or not self.restrictionType:
            # print(self.restrictionType)
            self.delete_keys()
        super().save(*args, **kwargs)
    
    def delete(self):
        # Try delete image
        if self.image:
            try:
                os.remove(self.image.path)
            except Exception as e:
                print(e)
        super().delete()

    def clear_keys_usage(self):
        keys = self.keys.all()
        for key in keys:
            key.allowed.clear()
            key.usedBy = None
            key.save()

    def delete_keys(self):
        keys = self.keys.all()
        for key in keys:
            key.delete()

    def delete_empty_groups(self):
        groups = self.groups.all()
        for group in groups:
            if len(group.categories.all()) < 1:
                # print("deleted group", group.name)
                group.delete()

    def delete_empty_categories(self):
        categories = self.categories.all()
        for category in categories:
            if len(category.candidates.all()) < 1:
                # print("deleted category", category.name)
                category.delete()

    def delete_all_votes(self):
        for vote in self.votes.all():
            vote.delete()

    def launch(self):
        if self.active:
            raise Exception("Can't activate an already active poll")
        if date.today() >= self.closing_date:
            raise Exception("Closing date Error")
        self.active = True
        self.delete_empty_groups()
        self.delete_empty_categories()
        self.delete_all_votes()
        self.clear_keys_usage()

        # Make sure every category is grouped if using groups
        categories = self.categories.all()
        grouped_categories = categories.exclude(group__isnull = True)
        ungrouped_categories = categories.exclude(group__isnull = False)
        if len(grouped_categories) > 0 and len(ungrouped_categories) > 0:
            raise Exception("All categories may either be grouped or ungrouped")

        # Make sure all candidates have a category
        candidates = self.candidates.all()
        uncategorized_candidate = candidates.exclude(categories_contesting__isnull = False)
        if len(uncategorized_candidate) > 0:
            raise Exception("Candidates must be assigned categories")
        self.save()
        
class PollCategoryGroup(models.Model):
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE,related_name="groups")
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['poll','name'],
                name='unique category group per poll'
            )
        ]
        ordering = ["id"]

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
        }

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        if self.name == "none":
            raise Exception("Group cannot be named none")
        # If new object
        if self._state.adding:
            # Limit to a max of 3 groups per poll
            categories = PollCategoryGroup.objects.filter(poll = self.poll)
            if len(categories) >= 3:
                raise Exception("Maximum length of 3 groups reached")
        super().save(*args, **kwargs)

class PollCategory(models.Model):
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE,related_name="categories")
    name = models.CharField(max_length=100)
    group =  models.ForeignKey(PollCategoryGroup,null=True,on_delete=models.SET_NULL,blank=True,related_name="categories")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['poll','name'],
                name='unique category per poll'
            )
        ]
    
    def __str__(self):
        return self.name

    def serialize(self):
        group_name  =""
        if self.group:
            group_name = self.group.name
        return {
            "id": self.id,
            "name": self.name,
            "group_name": group_name,
            "number_candidates": self.number_candidates()
        }
    
    # Number of candidates in this category
    def number_candidates(self):
        return len(self.candidates.all())

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        # Make sure group is from this poll
        if self.group:
            if self.group.poll != self.poll:
                raise Exception("Invalid group selected")
        super().save(*args, **kwargs)
        
    # Remove all contenders in this category
    def clear_all_candidates(self):
        candidates = self.candidates.all()
        for candidate in candidates:
            candidate.categories_contesting.remove(self)
    
    # Go to results showing all candidates and votes unarranged 
    def results(self):
        return {
            "candidates": [candidate.category_votes(self.name) for candidate in self.candidates.all()]
        }

    # Go to results showing all candidates arranged by highest votes, ignoring zero votes
    def resultsByVotes(self):
        all_votes = self.votes.all()
        candidates_by_highest_votes = all_votes.values_list('candidate__id').annotate(candidate_count=Count('candidate')).order_by('-candidate_count')
        candidates = []
        for candidate in candidates_by_highest_votes:
            id = candidate[0]
            candidate = self.candidates.get(id = id)
            candidates.append(candidate.category_votes (self.name))
        return {
            "candidates": candidates
        }

# Candidates for the poll and the positions standing for if multiple
class Candidate(models.Model):
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE,related_name="candidates")
    name = models.CharField(max_length=100)
    image =  models.ImageField(null=True,blank=True,upload_to=poll_candidates_image_upload_dir, max_length =500)
    categories_contesting = models.ManyToManyField(PollCategory , blank=True, related_name="candidates")
    party = models.CharField(max_length=15,null=True)

    def __str__(self):
        return self.name + ": "+ str(self.party)

    # Return votes for candidate in the category specified
    def category_votes(self,category_name):
        image = None
        if self.image:
            image = self.image.url
        votes = self.votes.all().filter(poll = self.poll, category__name = category_name).count()
        return {
            "id" : self.id,
            "name":self.name,
            "party":self.party,
            "image":image,
            "votes": votes
        }

    def serialize(self):
        image = None
        if self.image:
            image = self.image.url
        return {
            "id":self.id,
            "name": self.name,
            "party":self.party,
            "image":image,
            "categories_contesting":[category.name for category in self.categories_contesting.all()],
        }

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def delete(self):
        # Try delete image
        if self.image:
            try:
                os.remove(self.image.path)
            except Exception as e:
                print(e)
        super().delete()

# Record votes
class Vote(models.Model):
    voter = models.ForeignKey("user.User", on_delete=models.CASCADE ,null=True, related_name="voted_polls")
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE,related_name="votes")
    category = models.ForeignKey(PollCategory,on_delete=models.CASCADE,null=True,related_name="votes")
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE,null=True, related_name="votes")
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['voter','poll','category'],
                name='can vote only once in poll category'
            )
        ]
        ordering = ['voter']

# Record all keys needed to access voting
class RestrictionKey(models.Model):
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE,related_name="keys")
    key = models.CharField(max_length=100,null=True)
    usedBy = models.ForeignKey('user.User',on_delete=models.CASCADE, null=True, blank=True, related_name="specialKey" )
    allowed = models.ManyToManyField('user.User',  blank=True, related_name="oneKey")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['poll','key'],
                name='unique key per poll'
            )
        ]

    def serialize(self):
        used = False
        if self.usedBy:
            used = True
        return {
            "id": self.id,
            "key": self.key,
            "used": used
        }
