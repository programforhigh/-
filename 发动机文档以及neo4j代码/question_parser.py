#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

class QuestionPaser:

    ''' 构建实体节点 '''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        # print(res_classify)
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        # print(entity_dict)
        question_types = res_classify['question_types']
        sqls = []
            # sqls.append(args)
        for question_type in question_types:
            # print(question_type)
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'fail_influence':
                sql = self.sql_transfer(question_type, entity_dict.get('fail'))

            elif question_type == 'effect_reason':
                sql = self.sql_transfer(question_type, entity_dict.get('effect'))

            elif question_type == 'effect_task':
                sql = self.sql_transfer(question_type, entity_dict.get('effect'))


            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []
        # print(entities)
        # 查询语句
        sql = []
        # 查询疾病的原因
        if question_type == 'fail_influence':
            # MATCH(n: '失效形式')-[: '影响']->(m:'影响')  WHERE  n.name = '{0}' return m.name
            sql = ["MATCH(n: 失效形式)-[: 影响]->(m:影响)  WHERE  n.name = '{0}' return m.name".format(i) for i in entities]

        # 查询故障的原因
        elif question_type == 'effect_reason':
            sql = ["MATCH(n: 影响)-[: 原因]->(m:造成原因)  WHERE  n.name = '{0}' return m.name".format(i) for i in entities]

        # 查询故障的任务
        elif question_type == 'effect_task':
            sql = ["MATCH(n: 影响)-[*]->(m:任务)  WHERE  n.name = '{0}' return m.name".format(i) for i in entities]

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
