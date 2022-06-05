#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-5

from py2neo import Graph
import json


class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            "http://localhost:7474/browser/",
            # 用户名以及密码
            user="neo4j",
            password="123456789")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls, tmp):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            # print(question_type, answers)
            final_answer = self.answer_prettify(question_type, answers, tmp)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''生成hashtable'''
    def get_page_rank(self):
        f = open('records.json', encoding='utf-8-sig')
        s = json.load(f)
        hashtable = {}
        for item in s:
            hashtable[item['name']] = item['score']
        return hashtable

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers, tmp):
        final_answer = []
        page_rank = self.get_page_rank()
        if not answers:
            return ''
        if question_type == 'fail_influence':
            desc = [i['m.name'] for i in answers]
            subject = tmp['name']
            final_answer = '{0}的影响包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'effect_reason':
            desc = [i['m.name'] for i in answers]
            dic = {}
            for item in desc:
                dic[item] =page_rank[item]
            a1 = sorted(dic.items(), key=lambda x: x[1], reverse=True)
            result = [k for k, v in a1]
            # print(result)
            subject = tmp['name']
            final_answer = '影响{0}可能的原因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'effect_task':
            desc = set([i['m.name'] for i in answers])
            dic = {}
            for item in desc:
                dic[item] =page_rank[item]
            a1 = sorted(dic.items(), key=lambda x: x[1], reverse=True)
            result = [k for k, v in a1]
            # print(result)
            subject = tmp['name']
            final_answer = '{0}解决方案有：{1}'.format(subject, '；'.join(list(result)[:self.num_limit]))
        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()