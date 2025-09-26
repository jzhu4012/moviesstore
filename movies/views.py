from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, HiddenMovies, Petition, PetitionVote
from django.contrib.auth.decorators import login_required
from .forms import PetitionForm

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    if request.user.is_authenticated:
        hidden_ids = HiddenMovies.objects.filter(user=request.user).values_list('movie_id', flat=True)
        movies = movies.exclude(id__in=hidden_ids)

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    is_hidden = False
    if request.user.is_authenticated:
        is_hidden = HiddenMovies.objects.filter(user=request.user, movie=movie).exists()

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['is_hidden'] = is_hidden
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def hide_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    HiddenMovies.objects.get_or_create(user=request.user, movie=movie)
    return redirect('movies.index')

@login_required
def unhide_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    HiddenMovies.objects.filter(user=request.user, movie=movie).delete()
    return redirect('movies.hidden_movies')

@login_required
def hidden_movies(request):
    hidden_entries = HiddenMovies.objects.filter(user=request.user).select_related('movie')
    movies_hidden = [entry.movie for entry in hidden_entries]
    template_data = {
        'title': 'Hidden Movies',
        'movies': movies_hidden,
        'is_hidden' : True
    }
    return render(request, 'movies/hidden_movies.html', {'template_data': template_data})

def petitions(request):
    petitions = Petition.objects.order_by("-created_at")
    template_data = {
        "title": "Petitions",
        "petitions": petitions,
    }
    return render(request, "movies/petitions.html", {"template_data": template_data})

@login_required
def create_petition(request):
    if request.method == "POST":
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            existing = Petition.objects.filter(title__iexact=petition.title).first()
            if existing:
                return redirect("movies.petition", pk=existing.pk)
            petition.save()
            return redirect("movies.petition", pk=petition.pk)
    else:
        form = PetitionForm()
    return render(request, "movies/create_petition.html", {"form": form})

def petition(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    user_voted = False

    if request.user.is_authenticated:
        user_voted = PetitionVote.objects.filter(petition=petition, user=request.user).exists()

    if request.method == "POST" and request.user.is_authenticated and not user_voted:
        PetitionVote.objects.create(petition=petition, user=request.user)
        return redirect("movies.petition", pk=pk)

    template_data = {
        "title": petition.title,
        "petition": petition,
        "user_voted": user_voted
    }
    return render(request, "movies/petition.html", {"template_data": template_data})