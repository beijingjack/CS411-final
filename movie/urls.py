from django.urls import path
from django.conf.urls import url
from . import views
from .views import search, new_comment, MovieDetail, edit_comment, delete_comment#, new_release

app_name = 'movie'

urlpatterns = [
    url(r'^$',views.MovieListView.as_view(),name='movie_list'),
    url(r'^results/$',search, name='search'),
    path('<int:pk>/detail/', MovieDetail, name='movie_detail'),
    path('<int:pk>/comment/', new_comment, name='movie_comment'),
    path('<int:pk>/editcomment/', edit_comment, name='edit_comment'),
    path('<int:pk>/deletecomment/', delete_comment, name='delete_comment'),
    #path('newrelease/', new_release, name='new_release'),

]