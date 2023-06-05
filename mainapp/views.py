from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

data = pd.read_csv('D:\\Python\\4\\dictionary\\mainapp\\medicine.csv')

kz_x = np.array(data['kz'])
kz_y = np.array(data['сипаттама'])
ru_x = np.array(data['ru'])
ru_y = np.array(data['описание'])
en_x = np.array(data['en'])
en_y = np.array(data['description'])


def search(request):
    text = str(request.POST['search'])
    cv = CountVectorizer()
    KZ_X = cv.fit_transform(kz_x)
    X_train, X_test, y_train, y_test = train_test_split(KZ_X, kz_y,
                                                        test_size=0.20,
                                                        random_state=61
                                                        )
    model = MultinomialNB()
    model.fit(X_train, y_train)
    description = cv.transform([text]).toarray()
    print(str(model.predict(description)))
    i = np.where(kz_x == text)
    if len(i[0]):
        context = {
            'word': kz_x[i[0]][0],
            'i': i[0][0],
            'v': True,
        }

    else:
        context = {
            'v': False,
        }
    return render(request, 'mainapp/search.html', context)


def index(request):
    favorite = request.session.get('favorite')
    if not favorite:
        request.session['favorite'] = {}
    if request.method == 'POST':
        favorite = request.session.get('favorite')
        p = str(request.POST.get('p'))
        i = np.where(kz_x == p)
        if not favorite.get(str(i[0][0])):
            favorite[str(i[0][0])] = p
        request.session['favorite'] = favorite
    context = {'words': kz_x}
    return render(request, 'mainapp/index.html', context)


def word_single(request, pk):
    context = {
        'word_kz': kz_x[pk],
        'description_kz': kz_y[pk],
        'word_ru': ru_x[pk],
        'description_ru': ru_y[pk],
        'word_en': en_x[pk],
        'description_en': en_y[pk],
    }
    return render(request, 'mainapp/word-single.html', context)


def favorites(request):
    favorite = request.session.get('favorite')
    if not favorite:
        request.session['favorite'] = {}
    if request.method == 'POST':

        favorite = request.session.get('favorite')
        p = str(request.POST.get('p'))
        i = np.where(kz_x == p)
        if favorite.get(str(i[0][0])):
            favorite.pop(str(i[0][0]))
        request.session['favorite'] = favorite
    words = favorite
    context = {'words': words}
    return render(request, 'mainapp/favorites.html', context)
