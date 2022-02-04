# movie/urls.pyで呼び出される
from logging import exception
from django.shortcuts import redirect, render
import requests
import json
import environ
from movie.models import UserMovie

from tmdbv3api import TMDb
from tmdbv3api import Movie

# https://www.themoviedb.org/settings/api(TMDBユーザー情報)
tmdb = TMDb()
env = environ.Env()
tmdb.api_key = env("tmdb_api_key")

tmdb.language = 'ja'
tmdb.debug = True


# saveボタン押された後にidからデータを取得してDBに保存する
def saved_movie(request):

    context = {}

    # idをsave_btnから引っ張ってくる
    try:
        # POSTされたIDを取得
        request.method == "POST"
        saved_id = request.POST["save_btn"]
        sum_text = request.POST["sum_text"]
        vote_rate = request.POST["vote_rate"]

        if sum_text:
            summary = sum_text
        else:
            summary = "感想・要約は記入されていません"

        # IDで映画データを取得
        saved_id = int(saved_id)
        movie = Movie()
        saved_movie = movie.details(saved_id)

        if saved_movie:
            saved_id = saved_movie.id
            saved_title = saved_movie.title
            saved_poster_path = saved_movie.poster_path
            saved_release_date = saved_movie.release_date

            now_logging_user_id = request.user.id
            # ログインしているユーザー名取得
            now_logging_user = request.user.username
            # DBに追加
            UserMovie.objects.create(
                movie_id=saved_id, title=saved_title, poster_path=saved_poster_path, release_date=saved_release_date, summary=summary, vote_rate=vote_rate, auther=now_logging_user, user_id=now_logging_user_id)
        else:
            print("映画を取得できませんでした")
    except:
        print("新規作成されてない")

    try:
        # nowplaying_movie
        now_api = "https://api.themoviedb.org/3/movie/now_playing?api_key=e3bf1bb49fc4d8b56a7ccc546e43e313&language=ja&page={}&region=JP"
        now_movie_api = requests.get(now_api.format(1)).text
        now_movie_api2 = requests.get(now_api.format(2)).text
        now_movie = json.loads(now_movie_api)
        now_movie2 = json.loads(now_movie_api2)

        now_movie = now_movie["results"] + now_movie2["results"]

        # week_movie
        week_api = "https://api.themoviedb.org/3/trending/movie/week?api_key=e3bf1bb49fc4d8b56a7ccc546e43e313&language=ja&page={}&region=JP"
        week_movie_api = requests.get(week_api.format(1)).text
        week_movie_api2 = requests.get(week_api.format(2)).text
        week_movie = json.loads(week_movie_api)
        week_movie2 = json.loads(week_movie_api2)

        week_movie = week_movie["results"] + week_movie2["results"]

        # latest_movies
        top_api = "https://api.themoviedb.org/3/movie/top_rated?api_key=e3bf1bb49fc4d8b56a7ccc546e43e313&language=ja&page={}&region=JP"
        top_movie_api = requests.get(top_api.format(1)).text
        top_movie_api2 = requests.get(top_api.format(2)).text
        top_movie = json.loads(top_movie_api)
        top_movie2 = json.loads(top_movie_api2)

        top_movie = top_movie["results"] + top_movie2["results"]

        if now_movie:
            context["week_movies"] = week_movie
            context["now_movies"] = now_movie
            context["top_movies"] = top_movie
        else:
            print("DBから所得できてない")
    except:
        print("おすすめ映画読み込みされてない")

    # 編集・削除のボタンが押された後の処理
    # summaryとrateを受け取る
    try:
        print("DBが変更されました")
        # POSTされたDB_IDを取得
        request.method == "POST"
        if request.POST["db_edit_btn"]:
            db_id = request.POST["db_edit_btn"]
            sum_text = request.POST["sum_text"]
            vote_rate = request.POST["vote_rate"]
            btn_from = request.POST["btn_from"]

            if sum_text:
                summary = sum_text
            else:
                summary = "感想・要約は記入されていません"
            UserMovie.objects.filter(id=db_id).update(
                summary=summary, vote_rate=vote_rate)

            if btn_from == "mypage_tab1":
                return redirect("/mypage/my_movie")
        else:
            ("編集ボタンが認証できませんでした")

    except:
        print("DBが変更されてない")

    try:
        print("delete_movieボタンが押されました")
        # POSTされたDB_IDを取得
        request.method == "POST"
        if request.POST["db_delete_btn"]:
            print("削除処理がされました")
            db_id = request.POST["db_delete_btn"]
            UserMovie.objects.filter(id=db_id).delete()
        else:
            print("削除ボタン情報が認証できませんでした")
    except:
        print("削除処理が通っていません")

    # DBに保存されたデータを取り出す
    # DBから最新ObjectをN個取り出す
    try:
        objs = UserMovie.objects.order_by("id")[::-1][:5]
        # userのprofile画像を取り出す
        # for i in objs:
        #     user_id = i.user_id
        #     User.objects.filter("id")[::-1][:5]

        if objs:
            context["db_movies"] = objs
        else:
            print("DBから所得できてない")
    except:
        print("DB読まれてもない")

    return render(request, "movie/movies.html", context)


def search_movies(request):

    context = {}

    # queryを入力画面から引っ張ってくる
    try:
        request.method == "POST"
        movie = Movie()
        search_query = request.POST["search_query"]
        if search_query:
            result = movie.search(search_query)
            # print(result)
        else:
            result = movie.search("ドラえもん")
        # Queryが読み込まれなかった時の処理
        if result == []:
            context["movies"] = []
            context["title"] = "正しい映画名を入力してください"
        else:
            genre_list = []
            # ジャンル取得
            for i in result:
                searched_id = i.id
                searched_movie = movie.details(searched_id)
                genres_list = searched_movie.genres

                genre = genres_list[0]
                genre_list.append(genre)

            context["genres"] = genre_list
            context["movies"] = result
            context["title"] = search_query + "に関する映画"

    except:
        context["movies"] = []
        context["genres"] = []
        context["title"] = "映画が見つかりませんでした"

    # blogs,htmlを使い回している
    return render(request, "movie/user_movies.html", context)


# 保存画面の処理
def user_movie(request):
    context = {}
    try:
        # POSTされたIDを取得
        request.method == "POST"
        request.POST["save_btn"]
        saved_id = request.POST["save_btn"]
        movie = Movie()
        saved_movie = movie.details(saved_id)

        # 結果を表示
        if saved_movie:
            saved_title = saved_movie.title
            saved_poster_path = saved_movie.poster_path
            saved_release_date = saved_movie.release_date
            saved_overview = saved_movie.overview
            saved_runtime = saved_movie.runtime
            saved_vote_average = saved_movie.vote_average

            context["id"] = saved_id
            context["title"] = saved_title
            context["poster_path"] = saved_poster_path
            context["release_date"] = saved_release_date
            context["vote_average"] = saved_vote_average

            a = saved_runtime / 60
            hour = int(a)
            x = a - int(a)
            x_minute = 60 * x

            import math
            minute = math.ceil(x_minute)
            # 切り上げ処理
            context["runtime"] = "{}時間{}分".format(hour, minute)

            if saved_overview == "":
                context["overview"] = "あらすじがありません"
            else:
                context["overview"] = saved_overview
    except:
        print("idが取得できませんでした")

    return render(request, "movie/movie_save.html", context)


def like(request, id):
    user_movie = UserMovie.objects.get(id=id)
    user_movie.like += 1  # ここでいいねの数を増やす
    user_movie.save()  # 保存をする
    return redirect("movie/", id)


# edit画面にIDでデータを渡す
def edit_movie(request):

    context = {}
    print("編集ボタンが押されました")
    # POSTされたDB_IDを取得
    request.method == "POST"
    # edit_movieから
    if request.POST["db_edit_btn"]:
        print("db_edit_btnが押された")
        db_id = request.POST["db_edit_btn"]
        objs = UserMovie.objects.filter(id=db_id)
        context["db_movie"] = objs
        context["btn_from"] = "edit_movie"

    # db_edit_btnがPOSTだれた時の処理

    return render(request, "movie/edit_movie.html", context)


def mypage_edit_movie(request):

    context = {}
    print("編集ボタンが押されました")
    # POSTされたDB_IDを取得
    request.method == "POST"
    # mypage_tab1から
    if request.POST["mypage_edit_btn"]:
        print("mypage_edit_btnが押された")
        db_id = request.POST["mypage_edit_btn"]
        objs = UserMovie.objects.filter(id=db_id)
        context["db_movie"] = objs
        context["btn_from"] = "mypage_tab1"

    return render(request, "movie/edit_movie.html", context)


def mypage_delete_movie(request):

    context = {}
    print("delete_movieボタンが押されました")
    try:
        # POSTされたDB_IDを取得
        request.method == "POST"
        if request.POST["mypage_delete_btn"]:
            print("削除処理がされました")
            db_id = request.POST["mypage_delete_btn"]
            UserMovie.objects.filter(id=db_id).delete()
        else:
            print("削除ボタン情報が認証できませんでした")
    except:
        print("削除処理が通っていません")

    return redirect("/mypage/my_movie")
