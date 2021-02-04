from rest_framework import viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Announcement, User
from . import serializers
from .pagination_service import AnnouncementPagination
from .permissions import AnnouncementPermission


class AuthView(TokenObtainPairView):
    """Use to authenticate users."""

    serializer_class = serializers.TokenObtainPairCustomSerializer
    permission_classes = (AllowAny, )


class UserInfoView(generics.RetrieveAPIView):
    """Use to retrieve user`s account information (id, email and nickname)."""

    queryset = User
    serializer_class = serializers.UserInfoSerializer
    permission_classes = (IsAuthenticated,)


class UserCreateView(generics.CreateAPIView):
    """Use to create a new user."""

    queryset = User
    serializer_class = serializers.UserCreateSerializer
    permission_classes = (AllowAny,)


class AnnouncementViewSet(viewsets.ModelViewSet):
    """Use to create a new announcement, \
    retrieve/delete an announcement with given id or to get the whole announcements list."""

    queryset = Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerializer
    permission_classes = (AnnouncementPermission,)
    pagination_class = AnnouncementPagination

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class BaseAnnouncementUserListView(generics.ListAPIView):
    """Base announcement user view to extend in subclasses."""

    serializer_class = serializers.AnnouncementSerializer
    permission_classes = (AllowAny,)
    pagination_class = AnnouncementPagination
    lookup_field = 'user_id'


class UserAnnouncementsListView(BaseAnnouncementUserListView):
    """Use to get announcements that belong to user with given user id."""

    def get_queryset(self):
        return Announcement.objects.get_announcements_of_user(self.kwargs.get(self.lookup_field))


class FeedForUserListView(BaseAnnouncementUserListView):
    """Use to get feed for user with given user id \
    (Announcements that belong to this user are excluded)."""

    def get_queryset(self):
        return Announcement.objects.get_feed_for_user(self.kwargs.get(self.lookup_field))


class BaseAnnouncementsMapListView(generics.ListAPIView):
    """Base announcements map view to extend in subclasses."""

    serializer_class = serializers.AnnouncementsMapSerializer
    permission_classes = (AllowAny,)


class AnnouncementsMapListView(BaseAnnouncementsMapListView):
    """Use to get the whole announcements map."""

    queryset = Announcement.objects.all()


class AnnouncementsMapForUserView(BaseAnnouncementsMapListView):
    """Use to get announcements map without announcements \
    that belong to user with given user id."""

    lookup_field = "user_id"

    def get_queryset(self):
        return Announcement.objects.get_feed_for_user(self.kwargs.get(self.lookup_field))