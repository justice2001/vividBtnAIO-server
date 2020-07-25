from vividBtnAIO import utils
from DataBaseModel.models import Voice, VoiceGroup, Vtuber
import time
import json


# Create your views here.
def add_voice_data(request):
    if request.method == 'GET':
        return utils.response_json({'message': '请使用POST方法'}, 403)
    vtb_name = request.POST.get('vtb-name')
    name = request.POST.get('voice-name')
    group = request.POST.get('group-name')
    url = request.POST.get('url')
    version = request.POST.get('ver')
    count = 0
    zh = request.POST.get('zh')
    ja = request.POST.get('ja')
    en = request.POST.get('en')
    # 检查是否有本vtb
    if not Vtuber.objects.filter(name=vtb_name):
        return utils.response_json({'message': '请先创建此vtuber'}, 403)
    if not VoiceGroup.objects.filter(group_name=group):
        return utils.response_json({'message': '没有此分组!'}, 403)
    translate = {'zh': zh, 'ja': ja, 'en': en}
    voice = Voice(vtb_name=vtb_name, name=name, group=group, url=url, version=version, count=count
                  , translate=json.dumps(translate))
    voice.save()
    return utils.response_json({'message': '操作成功'})


def add_vtuber(request):
    if request.method == 'GET':
        return utils.response_json({'message': '请使用POST方法'}, 403)
    name = request.POST.get('name')
    bili_id = int(request.POST.get('bili-id'))
    youtube_id = request.POST.get('youtube-id')
    if Vtuber.objects.filter(name=name):
        return utils.response_json({'message': '该Vtuber已经存在'}, 403)
    vtuber = Vtuber(name=name, bilibili_uid=bili_id, youtube_id=youtube_id)
    vtuber.save()
    return utils.response_json({'message': '操作成功'})


def add_group(request):
    if request.method == 'GET':
        return utils.response_json({'message': '请使用POST方法'}, 403)
    vtb_name = request.POST.get('vtb-name')
    group_name = request.POST.get('name')
    zh = request.POST.get('zh')
    ja = request.POST.get('ja')
    en = request.POST.get('en')
    translate = {'zh': zh, 'ja': ja, 'en': en}
    if not Vtuber.objects.filter(name=vtb_name):
        return utils.response_json({'message': '没有此vtuber'}, 403)
    if VoiceGroup.objects.filter(vtb_name=vtb_name, group_name=group_name):
        return utils.response_json({'message': '该分组已经存在'}, 403)
    group = VoiceGroup(vtb_name=vtb_name, group_name=group_name, all_count=0, translate=json.dumps(translate))
    group.save()
    return utils.response_json({'message': '操作成功'})


def get_voice(request):
    vtb = request.GET.get('vtb-name')
    groups = VoiceGroup.objects.filter(vtb_name=vtb)
    data = Voice.objects.filter(vtb_name=vtb)
    if not data:
        return utils.response_json({'message': '未找到数据'}, 403)

    group2 = []
    for group in groups:
        voice_list = []
        name = group.group_name
        voices = Voice.objects.filter(group=name, vtb_name=vtb)
        for voice in voices:
            tmp = {
                'data_id': voice.id,
                'update': voice.version,
                'name': voice.name,
                'path': voice.url,
                'click_count': voice.count,
                'translation': json.loads(voice.translate)
            }
            voice_list.append(tmp)
        group_item = {
            'name': group.group_name,
            'translation': json.loads(group.translate),
            'all_click_count': group.all_count,
            'voicelist': voice_list
        }
        group2.append(group_item)
    response = {
        'last_update': '不详',
        'groups': group2
    }
    return utils.response_json(response)


def item_click(request):
    id = request.GET.get('id')
    item = Voice.objects.filter(id=id).first()
    item.count = item.count + 1
    item2 = VoiceGroup.objects.filter(group_name=item.group).first()
    item2.all_count = item2.all_count + 1
    item.save()
    item2.save()
    return utils.response_json({'count': item.count, 'group_all_count': item2.all_count})


# 开发时使用，发布请删掉
def del_all(request):
    if not request.GET.get('confirm'):
        return utils.response_json({'Warning': '你真的要这么做吗，确定请加confirm参数！', 'message': '正义提醒您：删库一时爽，一直删库一直爽！'}, 400)
    Voice.objects.all().delete()
    VoiceGroup.objects.all().delete()
    Vtuber.objects.all().delete()
    return utils.response_json({'Warning': '删库跑路'})
