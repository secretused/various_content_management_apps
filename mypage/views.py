from django.shortcuts import render, redirect
from movie.models import UserMovie
from book.models import UserBook
from idea.models import UserIdea, ThreadComment
from english.models import UserEnglish
from mysite.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from mypage.forms import UploadForm


def mypage(request):
    context = {}
    user_id = request.user.id
    db_movie_objs = UserMovie.objects.filter(
        user_id=user_id).order_by("id").reverse()[:1]
    db_book_objs = UserBook.objects.filter(
        user_id=user_id).order_by("id").reverse()[:1]
    db_idea_objs = UserIdea.objects.filter(
        user_id=user_id).order_by("id").reverse()[:1]
    db_english_objs = UserEnglish.objects.filter(
        user_id=user_id).order_by("id").reverse()[:4]

    # 総数取得
    movie_count = UserMovie.objects.all().filter(
        user_id=user_id).count()
    book_count = UserBook.objects.all().filter(
        user_id=user_id).count()
    idea_count = UserIdea.objects.all().filter(
        user_id=user_id).count()
    english_count = UserEnglish.objects.all().filter(
        user_id=user_id).count()

    db_user_objs = User.objects.all().filter(id=user_id)

    context["latest_movie"] = db_movie_objs
    context["latest_book"] = db_book_objs
    context["latest_idea"] = db_idea_objs
    context["latest_english"] = db_english_objs
    context["user_profile"] = db_user_objs

    context["movie_count"] = movie_count
    context["book_count"] = book_count
    context["idea_count"] = idea_count
    context["english_count"] = english_count

    return render(request, "mypage/mypage.html", context)


# プロフィール編集処理
def profile_edit(request):

    # プロフィール情報表示する
    try:
        context = {}
        if request.method == "POST":
            # 画像アップロード
            form = UploadForm(request.POST, request.FILES,)
            context["form"] = form

            profile_id = request.POST["profile_edit"]
            db_user_objs = User.objects.all().filter(id=profile_id)
            context["profile_data"] = db_user_objs

    except:
        print("プロフィールデータが取得出来ませでした")

    return render(request, "mypage/profile_edit.html", context)


def profile_email_save(request):

    # ユーザー情報(email)DB変更処理
    if request.method == "POST":
        profile_id = request.POST["email_edit"]
        account_image = request.POST.get("account_image")
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        user_name = request.POST["user_name"]
        user_email = request.POST["user_email"]
        print(account_image, "aaaaaaa")

        User.objects.filter(id=profile_id).update(
            firstName=first_name, lastName=last_name, username=user_name, email=user_email, account_image=account_image)

    else:
        print("ユーザー情報が取得出来ませでした")

    return redirect("/mypage")


def profile_password_save(request):

    # パスワード変更処理
    if request.method == "POST":
        profile_id = request.POST["password_edit"]

        # inputされたパスワード
        now_password = request.POST["now_password"]

        # DBのハッシュ化されているパスワード取得
        now_db = User.objects.get(id=profile_id)
        now_db_password = now_db.password

        if now_password:
            new_password = request.POST["new_password"]
            new_password_again = request.POST["new_password_again"]

            if new_password == new_password:
                User.objects.filter(id=profile_id).update(
                    password=new_password_again)

            else:
                print("新しいパスワードが同じではありません")
        else:
            print("パスワードが違います")

    else:
        print("パスワード情報が取得出来ませでした")

    return redirect("/mypage")


def mypage_tab1(request):

    user_id = request.user.id
    db_objs = UserMovie.objects.filter(
        user_id=user_id).order_by("id").reverse()

    paginator = Paginator(db_objs, 18)
    page = request.GET.get('page', 1)
    obj_count = UserMovie.objects.all().count()
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)

    context = {'pages': pages, 'count': obj_count}

    return render(request, "mypage/mypage_segment/mypage_tab1.html", context)


def mypage_tab2(request):

    user_id = request.user.id
    db_objs = UserBook.objects.filter(
        user_id=user_id).order_by("id").reverse()

    paginator = Paginator(db_objs, 18)

    page = request.GET.get('page', 1)
    obj_count = UserBook.objects.all().count()

    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)

    context = {'pages': pages, 'count': obj_count}

    return render(request, "mypage/mypage_segment/mypage_tab2.html", context)


def mypage_tab3(request):

    context = {}
    image_array = []

    user_id = request.user.id
    objs = UserIdea.objects.filter(user_id=user_id).order_by("id")[::-1]
    obj_count = UserIdea.objects.all().count()
    if objs:
        context["db_ideas"] = objs
        for obj in objs:
            # account_image取り出し
            user_id = obj.user_id
            objs = User.objects.filter(id=user_id)
            for obj in objs:
                account_image = obj.account_image
                image_array.append(account_image)

        context["account_image"] = image_array
        context["obj_count"] = obj_count
    else:
        print("DBから所得できてない")

    return render(request, "mypage/mypage_segment/mypage_tab3.html", context)


def mypage_tab3_user(request, idea_id):
    context = {}

    "通常表示用"
    context = {}
    image_array = []
    objs = UserIdea.objects.order_by("id")[::-1][:10]
    obj_count = UserIdea.objects.all().count()
    if objs:
        context["db_ideas"] = objs
        for obj in objs:
            # account_image取り出し
            user_id = obj.user_id
            objs = User.objects.filter(id=user_id)
            for obj in objs:
                account_image = obj.account_image
                image_array.append(account_image)

        context["account_images"] = image_array
        context["obj_count"] = obj_count
    else:
        print("DBから所得できてない")

    # コメント投稿後処理
    request.method == "POST"
    if request.POST.get("add_comment_btn"):
        idea_id = request.POST.get("add_comment_btn")
        if idea_id:
            comment_user_id = request.POST["user_id"]
            user_info = User.objects.get(id=comment_user_id)
            account_image = user_info.account_image
            comment_username = request.POST["user_name"]
            got_comment = request.POST["comment_form"]
            ThreadComment.objects.create(
                user_id=comment_user_id, username=comment_username, account_image=account_image, idea_id=idea_id, comment=got_comment)
    else:
        print("コメント投稿後処理ができませんでした")

    # コメント削除ボタン処理
    try:
        edit_id = request.POST["comment_delete_btn"]
        if edit_id:
            ThreadComment.objects.filter(id=edit_id).delete()
        else:
            print("edit_idが受け取れませんでした。")
    except:
        print("削除処理失敗しました")

    # 選択されたIdeaの詳細
    user_idea = UserIdea.objects.get(id=idea_id)
    if user_idea:
        context["idea_id"] = user_idea.id
        context["user_id"] = user_idea.user_id
        context["idea_title"] = user_idea.idea_title
        context["username"] = user_idea.username
        context["idea_detail"] = user_idea.idea_detail
        context["idea_from"] = user_idea.idea_from
        context["idea_tag"] = user_idea.idea_tag
        context["created_at"] = user_idea.created_at
        context["idea_price"] = user_idea.idea_price
        context["idea_target"] = user_idea.idea_target
        context["idea_for"] = user_idea.idea_for
        # tag取り出し
        idea_tag = user_idea.idea_tag
        idea_tag = idea_tag.replace(",", " ").replace(
            "、", " ").replace("　", " ").replace(".", "")
        tag_list = idea_tag.split(" ")
        context["idea_tag"] = tag_list

        # account画像取り出し
        got_id = user_idea.user_id
        objs = User.objects.get(id=got_id)
        context["account_image"] = objs.account_image

        # commentの取得
        # 全て表示
        comment_count = ThreadComment.objects.filter(idea_id=idea_id).count()
        more_btn = request.POST.get("more_btn")
        if more_btn:
            print(more_btn)
            user_comment = ThreadComment.objects.filter(idea_id=idea_id)
            context["comment_count"] = 1
        # 初期表示
        else:
            user_comment = ThreadComment.objects.filter(idea_id=idea_id)[:2]
            context["comment_count"] = comment_count
        context["user_comment"] = user_comment
        context["user_comment_id"] = idea_id

    else:
        print("DBから所得できてない")
    return render(request, 'mypage/mypage_segment/mypage_tab3_user.html', context)


def mypage_tab5(request):

    context = {}

    # 単語の表示
    user_id = request.user.id
    db_objs = UserEnglish.objects.filter(
        user_id=user_id).order_by("id").reverse()

    paginator = Paginator(db_objs, 18)

    page = request.GET.get('page', 1)
    obj_count = UserEnglish.objects.all().count()

    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)

    # checkボタンDB保存
    check_content = request.POST.getlist("check_content")
    saved_id = request.POST.get("check_save_btn")

    if check_content:
        if "1times" in check_content:
            UserEnglish.objects.filter(
                id=saved_id).update(checkbox_1="checked")
        elif "1times" not in check_content:
            UserEnglish.objects.filter(
                id=saved_id).update(checkbox_1="unchecked")

        if "2times" in check_content:
            UserEnglish.objects.filter(
                id=saved_id).update(checkbox_2="checked")
        elif "2times" not in check_content:
            UserEnglish.objects.filter(
                id=saved_id).update(checkbox_2="unchecked")

        if "3times" in check_content:
            UserEnglish.objects.filter(
                id=saved_id).update(checkbox_3="checked")
        elif "3times" not in check_content:
            UserEnglish.objects.filter(
                id=saved_id).update(checkbox_3="unchecked")
    else:
        print("checkボタン押されていません")

     # 編集ボタン処理

    if request.POST.get("english_edit_btn"):
        saved_id = request.POST.get("english_edit_btn")
        db_objs = UserEnglish.objects.filter(id=saved_id)
        context["edit_id"] = saved_id

        for db_obj in db_objs:
            context["query_text"] = db_obj.search_text
            context["changed_text"] = db_obj.changed_text
            context["query_lang"] = db_obj.query_lang
            context["changed_lang"] = db_obj.changed_lang

        return render(request, "english/english_edit.html", context)

    # 削除ボタン処理
    try:
        saved_id = request.POST.get("english_delete_btn")
        UserEnglish.objects.filter(id=saved_id).delete()
        print("削除されました")
    except:
        print("deleteボタン押されていません")

    context = {'pages': pages, 'count': obj_count}

    return render(request, "mypage/mypage_segment/mypage_tab5.html", context)
