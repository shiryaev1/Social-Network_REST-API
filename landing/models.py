from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from my_profile.models import Post


class UserProfileManager(models.Manager):
	def get_queryset(self):
		return super(UserProfileManager, self).get_queryset().all()


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
	description = models.TextField(max_length=300, default='',blank=True)
	city = models.CharField(max_length=100, default='',blank=True)
	website = models.URLField(default='',blank=True)
	phone = models.IntegerField(default=0,blank=True)
	image = models.ImageField(upload_to='profile_image', blank=True)
	sex = models.CharField(max_length=1, default='M')
	posts = models.ForeignKey(Post,blank=True, null= True, default=None, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username


def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Friend(models.Model):
	users = models.ManyToManyField(User)
	current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

	@classmethod
	def make_friend(cls, current_user, new_friend):
		friend, created = cls.objects.get_or_create(
			current_user=current_user
		)
		friend.users.add(new_friend)

	@classmethod
	def lose_friend(cls, current_user, new_friend):
		friend, created = cls.objects.get_or_create(
			current_user=current_user
		)
		friend.users.remove(new_friend)

	def __str__(self):
		return self.current_user.username

	class Meta:
		verbose_name = 'Friend'
		verbose_name_plural = 'Friends'


class AllMsg(models.Model):
	text = models.TextField()
	sender_user = models.ForeignKey(User, related_name='sender_u', on_delete=models.CASCADE)
	recipient_user = models.ForeignKey(User, related_name='recipient_u', on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.text