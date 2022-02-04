from django.shortcuts import redirect, render
from googleapiclient.discovery import build
from googletrans import Translator
import datetime
import environ

from english.models import EnglishVideo, UserEnglish

# AIzaSyB532PzO-uxWXEEZgDwBK6pmSceI4ZIWv4
# AIzaSyCYp5HG8-vIMjbux2OoXrO1me6Rj23QuAA

# API情報
env = environ.Env()
API_KEY = env("API_KEY")
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
)


def reload_data(request):

    print("リロードされたよ")
    # DB一日前の削除・更新
    try:
        request.method == "POST"
        search_query = request.POST["reload_btn"]
        if search_query == "":
            d_today = datetime.date.today()  # 現在日付の取得
            print(d_today)
            before_1_days = d_today - datetime.timedelta(days=1)
            print(before_1_days)
            if EnglishVideo.objects.filter(created_at__lte=before_1_days).exists():
                print(EnglishVideo.objects.filter(
                    created_at__lte=before_1_days).count(), "1日前までの動画数")
                print(EnglishVideo.objects.all().count(), "今日までの総動画数")
                EnglishVideo.objects.filter(
                    created_at__lte=before_1_days).delete()
                print(EnglishVideo.objects.all().count(), "消去後の総動画数")
                print("削除されました")
            else:
                print("1日前のデータがありません")
        else:
            print("機能していない")
    except:
        print("reloadできていません")

    # 動画情報取得処理
    search_query1 = youtube.search().list(
        q='[海外 旅 横断]', part='id,snippet', maxResults=40).execute()
    search_query2 = youtube.search().list(
        q='[Hapa英会話]', part='id,snippet', maxResults=30).execute()
    search_query3 = youtube.search().list(
        q='[atsueigo]', part='id,snippet', maxResults=30).execute()

    search_response1 = search_query1.get("items")
    search_response2 = search_query2.get("items")
    search_response3 = search_query3.get("items")

    for search_result in search_response1:
        if search_result["id"]["kind"] == "youtube#video":
            videoID = search_result["id"]["videoId"]
            search_result = search_result["snippet"]

            thumbnails_image = search_result["thumbnails"]["medium"]["url"]

            EnglishVideo.objects.create(
                thumbnails=thumbnails_image, link_url=videoID, video_id=1)

        else:
            print("videoではない")

    for search_result in search_response2:
        if search_result["id"]["kind"] == "youtube#video":
            videoID = search_result["id"]["videoId"]
            search_result = search_result["snippet"]

            thumbnails_image = search_result["thumbnails"]["medium"]["url"]

            EnglishVideo.objects.create(
                thumbnails=thumbnails_image, link_url=videoID, video_id=2)

    for search_result in search_response3:
        if search_result["id"]["kind"] == "youtube#video":
            videoID = search_result["id"]["videoId"]
            search_result = search_result["snippet"]

            thumbnails_image = search_result["thumbnails"]["medium"]["url"]

            EnglishVideo.objects.create(
                thumbnails=thumbnails_image, link_url=videoID, video_id=3)
        else:
            print("videoではない")

    return redirect("/english")


def get_youtube_data(request):
    context = {}

    # 単語保存処理
    try:
        request.method == "POST"
        is_authenticated = request.POST.get("btn-search")
        if is_authenticated:
            return redirect("/login/")
        # textareaの情報
        query_text = request.POST["query_text"]
        changed_text = request.POST["changed_text"]
        query_lang = request.POST["query_lang"]
        changed_lang = request.POST["changed_lang"]

        now_logging_user_id = request.user.id
        UserEnglish.objects.create(
            search_text=query_text, changed_text=changed_text, query_lang=query_lang,  changed_lang=changed_lang, user_id=now_logging_user_id)
    except:
        print("saveできませんでした")

    # その日の20個を表示
    objs1 = EnglishVideo.objects.filter(
        video_id=1).order_by("id")[::-1][:30]
    objs2 = EnglishVideo.objects.filter(
        video_id=2).order_by("id")[::-1][:20]
    objs3 = EnglishVideo.objects.filter(
        video_id=3).order_by("id")[::-1][:20]

    context["got_video1"] = objs1
    context["got_video2"] = objs2
    context["got_video3"] = objs3

    # DB単語表示処理
    objs = UserEnglish.objects.order_by("id")[::-1][:8]

    context["user_english"] = objs

    return render(request, "english/english.html", context)


# 翻訳
def translate(request):
    context = {}
    translator = Translator()

    request.method == "POST"
    search_query = request.POST["search_query"]

    # 検索結果なし
    if search_query == "":
        search_query = "検索結果がありません"
        language = translator.detect(search_query)
        language = language.lang

        if language == "ja":
            translated_text = translator.translate(
                search_query, src='ja', dest='en')
            result = translated_text.text

            context["query_text"] = search_query
            context["changed_text"] = result
            context["changed_lang"] = "英語"
            context["query_lang"] = "日本語"
        else:
            print("機能していません")

    # 検索結果あり
    else:
        language = translator.detect(search_query)
        language = language.lang

        if language == "en":
            translated_text = translator.translate(
                search_query, src='en', dest='ja')
            result = translated_text.text

            context["query_text"] = search_query
            context["changed_text"] = result
            context["query_lang"] = "英訳"
            context["changed_lang"] = "和訳"

        elif language == "ja":
            translated_text = translator.translate(
                search_query, src='ja', dest='en')
            result = translated_text.text

            context["query_text"] = search_query
            context["changed_text"] = result
            context["query_lang"] = "和訳"
            context["changed_lang"] = "英訳"
        else:
            print("機能していません")

    return render(request, "english/translate.html", context)


def english_edit(request):
    request.method == "POST"
    # textareaの情報
    if request.POST["edit_save_btn"]:
        changed_id = request.POST["edit_save_btn"]
        query_text = request.POST["query_text"]
        changed_text = request.POST["changed_text"]
        UserEnglish.objects.filter(id=changed_id).update(
            search_text=query_text, changed_text=changed_text)

    return redirect("/mypage/my_english")
