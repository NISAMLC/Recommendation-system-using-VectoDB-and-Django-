from django.shortcuts import render
from .models import Course
from .filters import CourseFilter

from django.core.paginator import Paginator
from .forms import RecommenderForm

import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import models
from sentence_transformers import SentenceTransformer
import pickle
from .services import *
import os

VECTOR_DB_PATH = "vector_database.db"
VECTOR_FILE_PATH = "vectorized_courses.pickle"
COLLECTION_NAME = "courses_collection"
MODEL = SentenceTransformer('all-MiniLM-L6-v2')

df = load_data(r'D:\Codeme\Deep_Learning\Projects_Only\Recommendation_System_using_vector_db\udemy_courses.csv')
docx, payload = prepare_data(df)


client = initialize_qdrant(VECTOR_DB_PATH, COLLECTION_NAME, 384)

if not os.path.exists(VECTOR_FILE_PATH):
    print("Vector file not found. Creating and saving vectors...")
    vectors = vectorize_texts(MODEL, docx)
    save_vector(vectors, VECTOR_FILE_PATH)
else:
    print("Loading vectors from pickle file...")
    vectors = load_vectors(VECTOR_FILE_PATH)

client.upload_collection(collection_name=COLLECTION_NAME, vectors=vectors, payload=payload, ids=None, batch_size=256)

# Create your views here.
def index_view(request):
    courses = Course.objects.all()
    search_filter = CourseFilter(request.GET,queryset=courses)
    search_term  =request.GET.get('course_title',"")
    courses = search_filter.qs
    paginator = Paginator(courses, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'index.html',context={'title':'Recommendation System','courses':courses,'search_filter':search_filter,"page_obj":page_obj,"search_term":search_term})


def read_course(request,pk):
    course = Course.objects.get(id=pk)
    context  ={'course':course}
    return render(request,"read_course.html",context)


def recommend_view(request):
    # if request.method=='POST':
    #     form = RecommenderForm(data=request.POST)
    #     if form.is_valid():
    #         search_term = form.cleaned_data['search_term']
    #
    #         #vectorize the search term
    #         vectorized_text = model.encode(search_term).tolist()
    #         search_results = client.search(collection_name='courses_collection', query_vector=vectorized_text, limit=5)
    #         courses = [ suggestion.payload for suggestion in search_results]
    #         scores  =[ {'score':suggestion.score} for suggestion in search_results]
    #         results  =[{**courses[i],**scores[i]} for i in range(len(courses))]
    #
    #
    #         #search the vectorDB and get recommendation
    #         context  ={'results':results,'form':form,'search_term':search_term}
    #         # context  ={'results':search_term.title(),'form':form,'search_term':search_term}
    #         return render(request,"recommended.html",context)
    if request.method == 'POST':
        form = RecommenderForm(data=request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            vectorized_text = MODEL.encode(search_term).tolist()
            search_results = search_qdrant(client, COLLECTION_NAME, vectorized_text, limit=5)
            results = [
                {**result.payload, 'score': result.score}
                for result in search_results
            ]

            context = {'results': results, 'form': form, 'search_term': search_term}
            return render(request, "recommended.html", context)

    else:
        form = RecommenderForm()

    context = {'form':form}
    return render(request,"recommended.html",context)