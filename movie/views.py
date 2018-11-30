from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.db.models import Q
from .models import Movie, RateMovie, AuthUser, Rating
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django import forms
from .forms import RatingForm
from .sentiment_analysis import predict_sentiment
from .vectorize_comment import get_vector
import numpy as np
from .tconst_scrape import findMovie


class MovieListView(ListView):
    model = Movie
    template_name = 'movie/movie_list.html'

    def get_context_data(self, **kwargs):

        context = super(MovieListView,self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Movie.objects.all().order_by('-year')[:100]


def MovieDetail(request, pk):
    template = 'movie/movie_detail.html'
    moviedetail = get_object_or_404(Movie, pk=pk)
    comment_id_all = RateMovie.objects.filter(movie=pk).values('comment')
    comment_all = Rating.objects.filter(comment_id__in=comment_id_all)
    context = {
         'object':moviedetail,
        'comment_list': comment_all,
     }
    return render(request, template, context)


def search(request):
    template = 'movie/movie_list.html'
    query = request.GET.get('q')
    if query:
        results = Movie.objects.filter(Q(title__icontains=query))
    else:
        results = Movie.objects.order_by('-year')[:20]

    context = {
        'object_list':results,
    }
    return render(request, template, context)

def mode(my_list):
    from collections import Counter
    ct = Counter(my_list)
    max_value = max(ct.values())
    return sorted(key for key, value in ct.items() if value == max_value)

def recommend(request):
    template = 'movie/recommend.html'
    pos_movie_list = RateMovie.objects.filter(username=request.user.username, attitude=1)
    pos_movie_genre_list = []
    for i in range(len(pos_movie_list)):
        pos_movie_id = pos_movie_list[i].movie.movie_id
        pos_movie_genre = Movie.objects.get(movie_id=pos_movie_id).genre
        pos_movie_genre_list.append(pos_movie_genre)
    fav_genre = mode(pos_movie_genre_list)[0]

    result = Movie.objects.filter(genre=fav_genre).order_by('-rating')[:100]

    context = {
        'object_list': result,
    }
    return render(request, template, context)

def webscrap(request):
    template = 'movie/webscrap.html'
    tmp_list = RateMovie.objects.filter(username=request.user.username)
    tconst_list = []
    for i in range(len(tmp_list)):
        tconst_num = tmp_list[i].movie.tconst
        tconst_list.append(tconst_num)
    movie_dict = findMovie(tconst_list)
    context = {
        'dictionary': movie_dict
    }

    return render(request, template, context)




def new_comment(request, pk):
    if request.method == "POST":
        if (RateMovie.objects.filter(username=request.user.username, movie=pk)).exists():
            comment_id = RateMovie.objects.get(username=request.user.username, movie=pk).comment.comment_id
            Rating.objects.filter(pk=comment_id).delete()
        form = RatingForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            user_instance = AuthUser.objects.get(username=request.user.username).username
            movie_instance = Movie.objects.get(movie_id=pk)
            comment_instance = Rating.objects.get(comment_id = post.comment_id)
            #####get the actual comment
            actual_comment = comment_instance.comments #### new
            ratemovie_instance = RateMovie()
            #####Vectorize the comment
            comment_vec = get_vector(actual_comment) # new
            attitude_pred = predict_sentiment(comment_vec) # new

             ####Need to store the attitude to the table
            ratemovie_instance.username = user_instance
            ratemovie_instance.movie = movie_instance
            ratemovie_instance.comment = comment_instance# new
            ratemovie_instance.attitude = attitude_pred
            ratemovie_instance.save()
            return redirect('/')
    else:
        form = RatingForm()
    return render(request, 'movie/comment_edit.html', {'form': form, 'prime': pk})
#

def edit_comment(request, pk):
    comment_id =  RateMovie.objects.get(username=request.user.username, movie=pk).comment.comment_id
    post = get_object_or_404(Rating, pk=comment_id)
    if request.method == "POST":
        form = RatingForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return redirect('/')

    else:
        form = RatingForm(instance=post)
    return render(request, 'movie/comment_edit.html', {'form': form, 'prime': pk})


def delete_comment(request, pk):
    comment_id =  RateMovie.objects.get(username=request.user.username, movie=pk).comment.comment_id
    Rating.objects.filter(pk=comment_id).delete()
    return redirect('/')


