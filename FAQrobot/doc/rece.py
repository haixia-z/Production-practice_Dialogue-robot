# coding=utf-8
from flask import abort, request
from wechatpy.enterprise import create_reply, parse_message
from wechatpy.enterprise.crypto import WeChatCrypto
from app.config import CORP_ID

from flask import Blueprint

# 应用ID
sCorp_Id = CORP_ID

# 回调模式里面随机生成的那个Token,EncodingAESKey
sToken = '1626058494_209_e3ca5202eb8f3352778dfc00c0b484a5'
sEncodingAESKey = ""

crm = Blueprint('settings', __name__, url_prefix='/crm')
crypto = WeChatCrypto(token=sToken, encoding_aes_key=sEncodingAESKey, corp_id=sCorp_Id)


# 对应回调模式中的URL
@crm.route('/weixin')
def weixin():
	echo_str = signature(request)
	if request.method == 'GET':
		return echo_str
	msg = parse_message(request.data)
	print(msg.type)
	if msg.type == 'text':
		reply = create_reply(msg.content, msg)
	else:
		reply = create_reply('Sorry, can not handle this for now', msg)
	return reply.render()


def signature(request):
	msg_signature = request.args.get('msg_signature', '')
	timestamp = request.args.get('timestamp', '')
	nonce = request.args.get('nonce', '')
	echo_str = request.args.get('echostr', '')
	print(request.args)
	try:
		# 认证并对echo_str进行解密并返回明文
		echo_str = crypto.check_signature(msg_signature, timestamp, nonce, echo_str)
		print(echo_str)
	except Exception as ex:
		print(ex)
		print(request)
		abort(403)
	return echo_str


@crm.route('/hello')
def hello():
	return "hello! index"