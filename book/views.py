import imp
from django.shortcuts import redirect, render
import requests
import json
from book.models import UserBook, BookAPI
import re
import environ

# from datetime import datetime
import datetime

env = environ.Env()
applicationId = env("applicationId")
# 保存後の処理


def saved_book(request):
    context = {}

    # idをsave_btnから引っ張ってくる
    try:
        # POSTされたIDを取得
        request.method == "POST"
        # textareaの情報
        sum_text = request.POST["sum_text"]
        saved_isbn = request.POST["save_btn"]
        vote_rate = request.POST["vote_rate"]

        if sum_text:
            summary = sum_text
        else:
            summary = "感想・要約は記入されていません"

        api = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&isbn={}&applicationId="+str(applicationId).format(
            saved_isbn)

        # 実際にAPIにリクエストを送信して結果を取得する
        search_books_api = requests.get(api).text
        # 結果はJSON形式なのでデコードする
        search_books = json.loads(search_books_api)
        # 結果を表示
        if search_books:
            # isbnで特定の一つのみ取得しているため[0]で一つだけ取得
            saved_result = search_books['Items'][0]["Item"]

            saved_title = saved_result["title"]
            saved_url = saved_result["itemUrl"]
            saved_largeImageUrl = saved_result["smallImageUrl"]

            salesDate = saved_result["salesDate"]

            salesDate = salesDate.replace("頃", "").replace("日", "")
            salesDate = re.split("年|月", salesDate)
            salesDate = [text if text !=
                         "" else "??" for text in salesDate]

            salesDate = "-".join(salesDate)

            now_logging_user_id = request.user.id
            # ログインしているユーザー名取得
            now_logging_user = request.user.username
            # DBに追加
            UserBook.objects.create(
                title=saved_title, itemUrl=saved_url, ImageUrl=saved_largeImageUrl, salesDate=salesDate, vote_rate=vote_rate, summary=summary, auther=now_logging_user, user_id=now_logging_user_id)
            print("DBに保存されました")
        else:
            print("書籍を取得できませんでした")
    except:
        print("You failed POST")

    # 編集・削除のボタンが押された後の処理
    # summaryとrateを受け取る
    try:
        # POSTされたDB_IDを取得
        request.method == "POST"
        if request.POST["db_edit_btn"]:
            print("変更処理がされました")
            db_id = request.POST["db_edit_btn"]
            sum_text = request.POST["sum_text"]
            vote_rate = request.POST["vote_rate"]
            btn_from = request.POST["btn_from"]

            if sum_text:
                summary = sum_text
            else:
                summary = "感想・要約は記入されていません"
            UserBook.objects.filter(id=db_id).update(
                summary=summary, vote_rate=vote_rate)

            if btn_from == "mypage_tab2":
                return redirect("/mypage/my_book")
        else:
            ("編集ボタンが認証できませんでした")

    except:
        print("変更処理が通っていません")

    try:
        # POSTされたDB_IDを取得
        request.method == "POST"
        if request.POST["db_delete_btn"]:
            print("削除処理がされました")
            db_id = request.POST["db_delete_btn"]
            UserBook.objects.filter(id=db_id).delete()
        else:
            print("削除ボタン情報が認証できませんでした")
    except:
        print("削除処理が通っていません")

    # DBに保存されたデータを取り出す
    # DBから最新ObjectをN個取り出す
    try:
        objs = UserBook.objects.order_by("id")[::-1][:5]
        if objs:
            context["db_books"] = objs
        else:
            print("DB情報が取得出来ませんでした")
    except:
        print("DB読まれてもない")

    # その日の20個を表示
    # [::-1][:30]
    objs1 = BookAPI.objects.filter(
        book_id=1).order_by("id")[:60]
    objs2 = BookAPI.objects.filter(
        book_id=2).order_by("id")[:60]
    objs3 = BookAPI.objects.filter(
        book_id=3).order_by("id")[:60]

    context["got_book1"] = objs1
    context["got_book2"] = objs2
    context["got_book3"] = objs3

    return render(request, "book/books.html", context)


# リロード(1日1回)
def reload_data(request):

    print("リロードされたよ")
    context = {}
    # # DB一日前の削除・更新
    # try:
    request.method == "POST"
    search_query = request.POST["reload_btn"]
    if search_query == "":
        d_today = datetime.date.today()  # 現在日付の取得
        print(d_today)
        before_1_days = d_today - datetime.timedelta(days=1)
        print(before_1_days)
        if BookAPI.objects.filter(created_at__lte=before_1_days).exists():
            print(BookAPI.objects.filter(
                created_at__lte=before_1_days).count(), "1日前までの動画数")
            print(BookAPI.objects.all().count(), "今日までの総動画数")
            BookAPI.objects.filter(
                created_at__lte=before_1_days).delete()
            print(BookAPI.objects.all().count(), "消去後の総動画数")
            print("削除されました")
        else:
            print("1日前のデータがありません")
    else:
        print("機能していない")
    # except:
    #     print("reloadできていません")

    # API取得処理
    ranking_api = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1091122717356551414&genreId={}&page=1"
    ranking_api2 = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1091122717356551414&genreId={}&page=2"

    essay_id = 101266
    business_id = 200446
    paperbook_id = 101937

    # api1
    essay = ranking_api.format(essay_id)
    bussines = ranking_api.format(business_id)
    paperbook = ranking_api.format(paperbook_id)

    search_essay_api = requests.get(essay).text
    search_bussines_api = requests.get(bussines).text
    search_paperbook_api = requests.get(paperbook).text

    # 結果はJSON形式なのでデコードする
    essay_ranking = json.loads(search_essay_api)
    bussines_ranking = json.loads(search_bussines_api)
    paperbook_ranking = json.loads(search_paperbook_api)

    # api=2
    essay2 = ranking_api2.format(essay_id)
    bussines2 = ranking_api2.format(business_id)
    paperbook2 = ranking_api2.format(paperbook_id)

    search_essay_api2 = requests.get(essay2).text
    search_bussines_api2 = requests.get(bussines2).text
    search_paperbook_api2 = requests.get(paperbook2).text

    # 結果はJSON形式なのでデコードする
    essay_ranking2 = json.loads(search_essay_api2)
    bussines_ranking2 = json.loads(search_bussines_api2)
    paperbook_ranking2 = json.loads(search_paperbook_api2)

    # essay_ranking
    if essay_ranking:
        saved_result = essay_ranking['Items']

        for i in saved_result:
            item = i["Item"]
            image = item["mediumImageUrls"][0]
            thumbnail_image = image["imageUrl"]
            item_url = item["itemUrl"]

            BookAPI.objects.create(
                ImageUrl=thumbnail_image, item_Url=item_url, book_id=1)

    else:
        print("essay_rankingが取得できませんでした")

    # if essay_ranking2:
    #     saved_result = essay_ranking2['Items']

    #     for i in saved_result:
    #         item = i["Item"]
    #         image = item["mediumImageUrls"][0]
    #         thumbnail_image = image["imageUrl"]
    #         item_url = item["itemUrl"]

    #         BookAPI.objects.create(
    #             ImageUrl=thumbnail_image, item_Url=item_url, book_id=1)

    # else:
    #     print("essay_ranking2が取得できませんでした")

    # bussines_ranking
    if bussines_ranking:
        saved_result = bussines_ranking['Items']

        for i in saved_result:
            item = i["Item"]
            image = item["mediumImageUrls"][0]
            thumbnail_image = image["imageUrl"]
            item_url = item["itemUrl"]

            BookAPI.objects.create(
                ImageUrl=thumbnail_image, item_Url=item_url, book_id=2)

    else:
        print("bussines_rankingが取得できませんでした")

    # if bussines_ranking2:
    #     saved_result = bussines_ranking2['Items']

    #     for i in saved_result:
    #         item = i["Item"]
    #         image = item["mediumImageUrls"][0]
    #         thumbnail_image = image["imageUrl"]
    #         item_url = item["itemUrl"]

    #         BookAPI.objects.create(
    #             ImageUrl=thumbnail_image, item_Url=item_url, book_id=2)

    # else:
    #     print("bussines_ranking2が取得できませんでした")

    # paperbook_ranking
    if paperbook_ranking:
        saved_result = paperbook_ranking['Items']

        # paperbook_image = []
        for i in saved_result:
            item = i["Item"]
            image = item["mediumImageUrls"][0]
            thumbnail_image = image["imageUrl"]
            item_url = item["itemUrl"]

            BookAPI.objects.create(
                ImageUrl=thumbnail_image, item_Url=item_url, book_id=3)

            # paperbook_image.append(image)
            # context["paperbook_image"] = paperbook_image
    else:
        print("paperbook_rankingが取得できませんでした")

    # if paperbook_ranking2:
    #     saved_result = paperbook_ranking2['Items']

    #     # paperbook_image = []
    #     for i in saved_result:
    #         item = i["Item"]
    #         image = item["mediumImageUrls"][0]
    #         thumbnail_image = image["imageUrl"]
    #         item_url = item["itemUrl"]

    #         BookAPI.objects.create(
    #             ImageUrl=thumbnail_image, item_Url=item_url, book_id=3)

    # else:
    #     print("paperbook_ranking2が取得できませんでした")

    return redirect("/book")

# Query送信後の処理


def search_books(request):

    try:
        request.method == "POST"
        search_query = request.POST["search_query"]

        # APIの雛型
        api = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&title={}&applicationId=1091122717356551414&hits=30".format(
            search_query)

        # 実際にAPIにリクエストを送信して結果を取得する
        search_books_api = requests.get(api).text
        # 結果はJSON形式なのでデコードする
        search_books = json.loads(search_books_api)
        # 結果を表示
        if search_books:
            saved_result = search_books['Items']
            book_data = []

            for i in saved_result:
                item = i["Item"]
                title = item["title"]
                itemUrl = item["itemUrl"]
                image = item["largeImageUrl"]
                author = item["author"]
                isbn = item["isbn"]
                salesDate = item["salesDate"]
                publisherName = item["publisherName"]
                reviewAverage = item["reviewAverage"]

                salesDate = salesDate.replace("頃", "").replace("日", "")
                salesDate = re.split("年|月", salesDate)
                salesDate = [text if text !=
                             "" else "??" for text in salesDate]

                salesDate = "-".join(salesDate)

                context = {}
                context["title"] = title
                context["itemUrl"] = itemUrl
                context["image"] = image
                context["author"] = author
                context["isbn"] = isbn
                context["salesDate"] = salesDate
                context["publisherName"] = publisherName
                context["reviewAverage"] = reviewAverage

                book_data.append(context)
                search_title = search_query + "に関する書籍"
            return render(request, "book/user_books.html", {"book_data": book_data, "search_title": search_title})
        else:
            book_data = []
            search_title = "正しい書籍名を入力してください"
            return render(request, "book/user_books.html", {"book_data": book_data, "search_title": search_title})
    except:
        book_data = []
        search_title = "書籍が見つかりませんでした"
        return render(request, "book/user_books.html", {"book_data": book_data, "search_title": search_title})


# 保存画面の処理
def user_book(request):
    context = {}
    try:
        # POSTされたIDを取得
        request.method == "POST"
        saved_isbn = request.POST["save_btn"]

        api = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&isbn={}&applicationId=1091122717356551414".format(
            saved_isbn)

        # 実際にAPIにリクエストを送信して結果を取得する
        search_books_api = requests.get(api).text
        # 結果はJSON形式なのでデコードする
        search_books = json.loads(search_books_api)
        # 結果を表示
        if search_books:
            # isbnで特定の一つのみ取得しているため[0]で一つだけ取得
            saved_result = search_books['Items'][0]["Item"]

            salesDate = saved_result["salesDate"]

            salesDate = salesDate.replace("頃", "").replace("日", "")
            salesDate = re.split("年|月", salesDate)
            salesDate = [text if text !=
                         "" else "??" for text in salesDate]
            salesDate = "-".join(salesDate)

            context["title"] = saved_result["title"]
            context["isbn"] = saved_result["isbn"]
            context["largeImageUrl"] = saved_result["largeImageUrl"]
            context["author"] = saved_result["author"]
            context["salesDate"] = salesDate
            context["itemPrice"] = saved_result["itemPrice"]
            context["publisherName"] = saved_result["publisherName"]
            context["reviewAverage"] = saved_result["reviewAverage"]

            # ジャンル取得処理
            genre_id = saved_result["booksGenreId"]
            if genre_id:
                api = "https://app.rakuten.co.jp/services/api/BooksGenre/Search/20121128?format=json&booksGenreId={}&applicationId=1091122717356551414".format(
                    genre_id)
                books_genre = requests.get(api).text
                # 結果はJSON形式なのでデコードする
                genre = json.loads(books_genre)
                genre_result = genre['parents'][0]["parent"]
                context["genre"] = genre_result["booksGenreName"]
            else:
                print("ジャンルが取得できませんでした")

        else:
            print("JSONが取得できませんでした")

    except:
        print("isbnが取得できませんでした")

    return render(request, "book/book_save.html", context)


# edit画面にIDでデータを渡す
def edit_book(request):

    context = {}
    try:
        print("編集ボタンが押されました")
        # POSTされたDB_IDを取得
        request.method == "POST"
        if request.POST["db_edit_btn"]:
            db_id = request.POST["db_edit_btn"]
            objs = UserBook.objects.filter(id=db_id)
            context["db_book"] = objs
            context["btn_from"] = "edit_book"
        else:
            print("DBから所得できてない")
    except:
        print("btnが機能していない")

    # db_edit_btnがPOSTだれた時の処理

    return render(request, "book/edit_book.html", context)

# edit画面にIDでデータを渡す


def mypage_edit_book(request):

    context = {}
    try:
        print("編集ボタンが押されました")
        # POSTされたDB_IDを取得
        request.method == "POST"
        if request.POST["mypage_edit_btn"]:
            db_id = request.POST["mypage_edit_btn"]
            objs = UserBook.objects.filter(id=db_id)
            context["db_book"] = objs
            context["btn_from"] = "mypage_tab2"
        else:
            print("DBから所得できてない")
    except:
        print("btnが機能していない")

    # db_edit_btnがPOSTだれた時の処理

    return render(request, "book/edit_book.html", context)


def mypage_delete_book(request):

    context = {}
    print("delete_movieボタンが押されました")
    try:
        # POSTされたDB_IDを取得
        request.method == "POST"
        if request.POST["mypage_delete_btn"]:
            print("削除処理がされました")
            db_id = request.POST["mypage_delete_btn"]
            UserBook.objects.filter(id=db_id).delete()
        else:
            print("削除ボタン情報が認証できませんでした")
    except:
        print("削除処理が通っていません")

    return redirect("/mypage/my_book")
