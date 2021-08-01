from django.contrib import admin

from .models import Poll, PollCategory, Candidate, RestrictionKey,Vote, PollCategoryGroup

admin.site.register(Poll)
admin.site.register(PollCategory)
admin.site.register(Candidate)
admin.site.register(RestrictionKey)
admin.site.register(Vote)
admin.site.register(PollCategoryGroup)




