from django.urls import path
from players import views

urlpatterns = [
    path("", views.PlayerHome.as_view(), name="home"),
    path("post/<slug:post_slug>/", views.ShowPost.as_view(), name="post"),
    path(
        "position/<slug:position_slug>/",
        views.PlayerPosition.as_view(),
        name="position",
    ),
    path("club/<slug:club_slug>/", views.PlayerClub.as_view(), name="club"),
    path("about/", views.About.as_view(), name="about"),
    path("addpage/", views.AddPage.as_view(), name="add_page"),
    path("contact/", views.Contact.as_view(), name="contact"),
    path("tag/<slug:tag_slug>/", views.TagPostList.as_view(), name="tag"),
    path("edit/<slug:slug>/", views.UpdatePage.as_view(), name="edit_page"),
    path("delete/<slug:slug>/", views.DeletePage.as_view(), name="delete_page"),
]
