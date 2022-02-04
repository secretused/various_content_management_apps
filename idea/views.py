from django.shortcuts import redirect, render
from .models import UserIdea, ThreadComment
from mysite.models import User
import sys


def idea_home(request):

    context = {}
    image_array = []
    objs = UserIdea.objects.order_by("id")[::-1][:10]
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
    else:
        print("DBから所得できてない")

    return render(request, "idea/ideas.html", context)


def save_idea(request):

    # 投稿ボタンを押した時の処理
    context = {}
    request.method == "POST"
    try:
        got_value = request.POST["tweet_btn"]
        if got_value == "":
            user_id = request.user.id
            user_name = request.user.username
            context["user_id"] = user_id
            context["user_name"] = user_name
            redirect("/save_idea")
    except:
        print("tweet_btnが動いてない")

    # try:
    is_authenticated = request.POST.get('not_authenticated_btn')
    if is_authenticated == "True":
        return redirect("/login/")
    got_id = request.POST.get('reserve_btn')
    if got_id:
        got_username = request.POST["user_name"]
        idea_title = request.POST["idea_title"]
        idea_detail = request.POST["idea_detail"]
        if idea_detail == "":
            idea_detail = "アイデアの詳細が入力されていません"
        idea_tag = request.POST["idea_tag"]
        print(idea_tag)
        if idea_tag == "":
            idea_tag = "タグが入力されていません"
        idea_from = request.POST["idea_from"]
        if idea_from == "":
            idea_from = "思いついたきっかけが入力されていません"
        idea_for = request.POST["idea_for"]
        if idea_for == "":
            idea_for = "アイデアの用途が入力されていません"
        idea_target = request.POST["idea_target"]
        if idea_target == "":
            idea_target = "ターゲットが入力されていません"
        idea_price = request.POST["idea_price"]

        UserIdea.objects.create(
            user_id=got_id, username=got_username, idea_title=idea_title, idea_detail=idea_detail, idea_tag=idea_tag, idea_from=idea_from, idea_for=idea_for, idea_target=idea_target, idea_price=idea_price)
        return redirect("/idea")
    # except:
    #     print("登録ボタンが認証できない")

    return render(request, "idea/ideas_save.html", context)


def user_idea(request, idea_id):
    context = {}

    "通常表示用"
    context = {}
    image_array = []
    objs = UserIdea.objects.order_by("id")[::-1][:10]
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
    return render(request, 'idea/user_idea.html', context)

# idea編集処理


def idea_edit(request):
    context = {}

    # 編集ボタン押された処理
    request.method == "POST"
    try:
        edit_id = request.POST["db_edit_btn"]
        print(edit_id, "-----")
        if edit_id:
            user_idea = UserIdea.objects.get(id=edit_id)
            if user_idea:
                context["idea_id"] = user_idea.id
                context["idea_title"] = user_idea.idea_title
                context["username"] = user_idea.username
                context["idea_detail"] = user_idea.idea_detail
                context["idea_from"] = user_idea.idea_from
                context["idea_tag"] = user_idea.idea_tag
                context["created_at"] = user_idea.created_at
                context["idea_price"] = user_idea.idea_price
                context["idea_target"] = user_idea.idea_target
                context["idea_for"] = user_idea.idea_for
    except:
        print("編集処理失敗しました")

    # idea削除ボタン処理
    try:
        edit_id = request.POST["db_delete_btn"]
        if edit_id:
            UserIdea.objects.filter(id=edit_id).delete()
            return redirect("/idea")
        else:
            print("edit_idが受け取れませんでした。")
    except:
        print("削除処理失敗しました")

    # 保存ボタンからDB変更処理
    if request.POST.get("db_save_btn"):
        print("ここまできてる")
        idea_save_id = request.POST.get("db_save_btn")
        print(idea_save_id, "-------")
        if idea_save_id:
            print("idea_save_idを手に入れている")
            got_username = request.POST["user_name"]
            idea_title = request.POST["idea_title"]
            idea_detail = request.POST["idea_detail"]
            idea_tag = request.POST["idea_tag"]
            idea_from = request.POST["idea_from"]
            idea_for = request.POST["idea_for"]
            idea_target = request.POST["idea_target"]
            idea_price = request.POST["idea_price"]

            UserIdea.objects.filter(id=idea_save_id).update(
                username=got_username, idea_title=idea_title, idea_detail=idea_detail, idea_tag=idea_tag, idea_from=idea_from, idea_for=idea_for, idea_target=idea_target, idea_price=idea_price)
            print("変更処理成功している")

            return redirect("/idea")

    return render(request, 'idea/idea_edit.html', context)
