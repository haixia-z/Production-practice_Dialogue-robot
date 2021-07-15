import os
import sys
import time
import logging
from collections import deque
from urllib import request

import app as app
import jieba
import jieba.posseg as pseg
from flask import Flask
from self import self

from WXBizMsgCrypt import WXBizMsgCrypt
from utils import (
	get_logger,
	similarity,
)

jieba.dt.tmp_dir = "./"
jieba.default_logger.setLevel(logging.ERROR)
logger = get_logger('faqrobot', logfile="faqrobot.log")


class zhishiku(object):
	def __init__(self, q):  # a是答案（必须是1给）, q是问题（1个或多个）
		self.q = [q]
		self.a = ""
		self.sim = 0
		self.q_vec = []
		self.q_word = []

	def __str__(self):
		return 'q=' + str(self.q) + '\na=' + str(self.a) + '\nq_word=' + str(self.q_word) + '\nq_vec=' + str(self.q_vec)
		# return 'a=' + str(self.a) + '\nq=' + str(self.q)


def jsonify(param):
	pass


class AuthVerify:
	pass


class FAQrobot(object):
	def __init__(self, zhishitxt='FAQ_Q.txt', lastTxtLen=10, usedVec=False):
		# usedVec 如果是True 在初始化时会解析词向量，加快计算句子相似度的速度
		self.lastTxt = deque([], lastTxtLen)
		self.zhishitxt = zhishitxt
		self.usedVec = usedVec
		self.reload()

	def load_qa(self):
		self.zhishiku = []
		with open(self.zhishitxt, encoding='utf-8') as f:
			txt = f.readlines()
			abovetxt = 0  # 上一行的种类： 0空白/注释  1答案   2问题
			for t in txt:  # 读取FAQ文本文件
				t = t.strip()
				if not t or t.startswith('#'):
					abovetxt = 0
				elif abovetxt != 2:
					if t.startswith('【问题】'):  # 输入第一个问题
						self.zhishiku.append(zhishiku(t[4:]))
						abovetxt = 2
					else:  # 输入答案文本（非第一行的）
						self.zhishiku[-1].a += '\n' + t
						abovetxt = 1
				else:
					if t.startswith('【问题】'):  # 输入问题（非第一行的）
						self.zhishiku[-1].q.append(t[4:])
						abovetxt = 2
					else:  # 输入答案文本
						self.zhishiku[-1].a += t
						abovetxt = 1

		for t in self.zhishiku:
			for question in t.q:
				t.q_word.append(set(jieba.cut(question)))

	def load_embedding(self):
		from gensim.models import Word2Vec
		if not os.path.exists('Word60.model'):
			self.vecModel = None
			return

		# 载入60维的词向量(Word60.model，Word60.model.syn0.npy，Word60.model.syn1neg.npy）
		self.vecModel = Word2Vec.load('Word60.model')
		for t in self.zhishiku:
			t.q_vec = []
			for question in t.q_word:
				t.q_vec.append({t for t in question if t in self.vecModel.index2word})

	def reload(self):
		self.load_qa()
		self.load_embedding()

		print('请输入问题')

	def maxSimTxt(self, intxt, simCondision=0.1, simType='simple'):
		"""
        找出知识库里的和输入句子相似度最高的句子
        simType=simple, simple_POS, vec
        """
		self.lastTxt.append(intxt)
		if simType not in ('simple', 'simple_pos', 'vec'):
			return 'error:  maxSimTxt的simType类型不存在: {}'.format(simType)

		# 如果没有加载词向量，那么降级成 simple_pos 方法
		embedding = self.vecModel
		if simType == 'vec' and not embedding:
			simType = 'simple_pos'

		for t in self.zhishiku:
			questions = t.q_vec if simType == 'vec' else t.q_word
			in_vec = jieba.lcut(intxt) if simType == 'simple' else pseg.lcut(intxt)

			t.sim = max(
				similarity(in_vec, question, method=simType, embedding=embedding)
				for question in questions
			)
		maxSim = max(self.zhishiku, key=lambda x: x.sim)
		logger.info('maxSim=' + format(maxSim.sim, '.0%'))

		if maxSim.sim < simCondision:
			return '抱歉，我没有理解您的意思。'

		return maxSim.a

	def answer(self, intxt, simType='simple'):
		"""simType=simple, simple_POS, vec, all"""
		if not intxt:
			return ''

		if simType == 'all':  # 用于测试不同类型方法的准确度，返回空文本
			for method in ('simple', 'simple_pos', 'vec'):
				outtext = 'method:\t' + self.maxSim(intxt, simType=method)
				print(outtext)

			return ''
		else:
			outtxt = self.maxSimTxt(intxt, simType=simType)
			# 输出回复内容，并计入日志
		return outtxt


# !/usr/bin/python
# -*- coding: utf-8 -*-

import time
import requests
import json, os

class WeChat_SMS:
	def __init__(self):
		self.CORPID = 'wwf5f4cf4c915c524a'  # 企业ID， 登陆企业微信，在我的企业-->企业信息里查看
		self.CORPSECRET = 'izCdX8TWllnLMyquKl2FY6u0EBRy-Ygk2xMLuf2ukXY'  # 自建应用，每个自建应用里都有单独的secret
		self.AGENTID = '1000003'  # 应用代码
		self.TOUSER = "@all"  # 接收者用户名,@all 全体成员
        self.sToken='4uGyOxGhJMp6dxW'
        self.sEncodingAESKey='lYQzvLkNGxOPeYFLsRyn11YtHgum1IAjOCFd3BJdt5g'



	def _get_access_token(self):
		url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
		values = {'corpid': self.CORPID, 'corpsecret': self.CORPSECRET, }
		req = requests.post(url, params=values)
		data = json.loads(req.text)
		return data["access_token"]

	def get_access_token(self):
		try:
			with open('access_token.conf', 'r') as f:
				t, access_token = f.read().split()
		except:
			with open('access_token.conf', 'w') as f:
				access_token = self._get_access_token()
				cur_time = time.time()
				f.write('\t'.join([str(cur_time), access_token]))
				return access_token
		else:
			cur_time = time.time()
			if 0 < cur_time - float(t) < 7200:  # token的有效时间7200s
				return access_token
			else:
				with open('access_token.conf', 'w') as f:
					access_token = self._get_access_token()
					f.write('\t'.join([str(cur_time), access_token]))
					return access_token

	def send_data(self, msg):


		send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
		send_values = {
			"touser": self.TOUSER,
			# "toparty": self.TOPARY, 	#设置给部门发送
			"msgtype": "text",
			"agentid": self.AGENTID,
			"text": {
				"content": msg
			},
			"safe": "0"
		}
		send_msges = (bytes(json.dumps(send_values), 'utf-8'))
		respone = requests.post(send_url, send_msges)
		respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
		# print (respone["errmsg"])
		return respone["errmsg"]
class Flask:
	pass


def server_run(self):
	app = Flask(__name__)

	@app.route('/index', methods=['GET', 'POST'])
	def index(ET=None):
		wxcpt = WXBizMsgCrypt('4uGyOxGhJMp6dxW', 'lYQzvLkNGxOPeYFLsRyn11YtHgum1IAjOCFd3BJdt5g', 'wwf5f4cf4c915c524a')
		# 获取url验证时微信发送的相关参数
		sVerifyMsgSig = request.args.get('msg_signature')
		sVerifyTimeStamp = request.args.get('timestamp')
		sVerifyNonce = request.args.get('nonce')
		sVerifyEchoStr = request.args.get('echostr')


		# 接收客户端消息
		if request.method == 'POST':
			sReqMsgSig = sVerifyMsgSig
			sReqTimeStamp = sVerifyTimeStamp
			sReqNonce = sVerifyNonce
			sReqData = request.data
			print(sReqData)

			ret, sMsg = wxcpt.DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
			print
			ret, sMsg
			if (ret != 0):
				print
				"ERR: DecryptMsg ret: " + str(ret)
				sys.exit(1)
			# 解析发送的内容并打印

			xml_tree = ET.fromstring(sMsg)
			print('xml_tree is ', xml_tree)

	def send_data(self, msg):
		send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
		send_values = {
			"touser": self.TOUSER,
			# "toparty": self.TOPARY, 	#设置给部门发送
			"msgtype": "text",
			"agentid": self.AGENTID,
			"text": {
				"content": msg
			},
			"safe": "0"
		}
		send_msges = (bytes(json.dumps(send_values), 'utf-8'))
		respone = requests.post(send_url, send_msges)
		respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
		# print (respone["errmsg"])
		return respone["errmsg"]

	def receive(self, submit_task_receive):
		try:
			auth_verify = AuthVerify()
			if request.method == "POST":
				msg_signature = request.args.get('msg_signature')
				timestamp = request.args.get('timestamp')
				nonce = request.args.get('nonce')
				request_data = request.data
				param = auth_verify.verifi_content(msg_signature, timestamp, nonce, request_data)
				submit_task_receive.delay(param)
			if request.method == "GET":
				msg_signature = request.args.get('msg_signature')
				timestamp = request.args.get('timestamp')
				nonce = request.args.get('nonce')
				echostr = request.args.get('echostr')
				s_echo_str = auth_verify.verifi(msg_signature, timestamp, nonce, echostr)
				return s_echo_str
		except Exception as e:
			print(e)
			return jsonify({'code': -1, 'error_message': e})

		auth_verify.verifi_content(msg_signature, timestamp, nonce, request_data)

		def verifi_content(self, msg_signature, timestamp, nonce, request_data, ET=None):
			ret, sMsg = self.wxcpt.DecryptMsg(request_data, msg_signature, timestamp, nonce)
			if ret != 0:
				print("ERR: DecryptMsg ret: ") + str(ret)
				sys.exit(1)
			xml_tree = ET.fromstring(sMsg)
			content = xml_tree.find("Content").text
			create_time = xml_tree.find("CreateTime").text
			from_username = xml_tree.find("FromUserName").text
			print('content')
			return {'create_time': create_time, 'from_username': from_username, 'content': content}
# if __name__ == '__main__':
#     wx = WeChat_SMS()
#     wx.send_data(msg="你好呀")
# 以下是添加对日志的监控
# srcfile = u"G:/123.txt"
# file = open(srcfile)
# file.seek(0, os.SEEK_END)
# while 1:
#     where = file.tell()
#     line = file.readline()
#     if not line:
#         time.sleep(1)
#         file.seek(where)
#     else:
#         print(line)
#         wx.send_data(msg=line)

if __name__ == '__main__':
	robot = FAQrobot('FAQ_Q.txt', usedVec=False)
	while True:
		# simType=simple, simple_pos, vec, all
	  wx = WeChat_SMS()
	  wx.server_run()wxcpt = WXBizMsgCrypt('4uGyOxGhJMp6dxW', 'lYQzvLkNGxOPeYFLsRyn11YtHgum1IAjOCFd3BJdt5g', 'wwf5f4cf4c915c524a')


