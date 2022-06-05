#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: ts
# Date: 2022-5-25

from question_classifier import *
from question_parser import *
from answer_search import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
    # 为什么未能向飞机提供即将出现的燃油滤清器旁通信号？
    def chat_main(self, sent):
        answer = '您好，我是小汤同学，希望可以帮到您。如果没答上来，可联系https://1737723493@qq.com/。祝您身体棒棒！'
        res_classify = self.classifier.classify(sent)
        # print(res_classify)
        tmp = {}
        tmp['name'] = res_classify['name']
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        # print(res_sql)
        final_answers = self.searcher.search_main(res_sql, tmp)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('小汤同学:', answer)
    # 问题实例：
    # 为什么造成失去N2限制冗余？
    # 怎么处理失去N2限制冗余？
    # 怎么会地面操作的怠速推力过大？
    # 如何解决地面操作的怠速推力过大？
    # 无法控制风扇转速怎么办？