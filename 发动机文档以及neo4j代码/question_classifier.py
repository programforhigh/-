#!/usr/bin/env python3
# coding: utf-8
# File: question_classifier.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

import os
import ahocorasick
class QuestionClassifier:
    def __init__(self):
        # 找到该文件目录上一级的目录名称，之后再定位到特征词所在的文件
        cur_dir = '/'.join(os.path.abspath(__file__).split('\\')[:-1])
        #　特征词路径
        self.mainsystem_path = os.path.join(cur_dir, 'dict/主系统.txt')
        self.product_path = os.path.join(cur_dir, 'dict/产品.txt')
        self.task_path = os.path.join(cur_dir, 'dict/任务.txt')
        self.function_path = os.path.join(cur_dir, 'dict/功能.txt')
        self.fail_path = os.path.join(cur_dir, 'dict/失效形式.txt')
        self.subsystem_path = os.path.join(cur_dir, 'dict/子系统.txt')
        self.effect_path = os.path.join(cur_dir, 'dict/影响.txt')
        self.cause_path = os.path.join(cur_dir, 'dict/造成原因.txt')
        # 加载特征词
        self.mainsystem_wds= [i.strip() for i in open(self.mainsystem_path, encoding='utf-8') if i.strip()]
        self.product_wds= [i.strip() for i in open(self.product_path, encoding='utf-8') if i.strip()]
        self.task_wds= [i.strip() for i in open(self.task_path, encoding='utf-8') if i.strip()]
        self.function_wds= [i.strip() for i in open(self.function_path, encoding='utf-8') if i.strip()]
        self.fail_wds= [i.strip() for i in open(self.fail_path, encoding='utf-8') if i.strip()]
        self.subsystem_wds= [i.strip() for i in open(self.subsystem_path, encoding='utf-8') if i.strip()]
        self.effect_wds= [i.strip() for i in open(self.effect_path, encoding='utf-8') if i.strip()]
        self.cause_wds = [i.strip() for i in open(self.cause_path, encoding='utf-8') if i.strip()]
        self.region_words = set(self.mainsystem_wds + self.product_wds + self.task_wds + self.function_wds + self.fail_wds +
                                self.subsystem_wds + self.effect_wds + self.cause_wds)

        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建实例 和 名称的词典，
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.symptom_qwds = [ '表征', '现象', '表现']
        self.effect_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        # self.acompany_qwds = ['并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        # self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜' ,'忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物','补品']
        # self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        # self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.cureway_qwds = ['怎么处理', '如何解决', '怎么做', '怎么搞', '如何弄', '解决措施', '办法', '咋搞', '怎么办', '咋办', '咋做']
        self.cause_qwds = ['导致', '原因', '起源', '源头']
        # self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医']
        # self.easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        # self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        # self.belong_qwds = ['属于什么科', '属于', '什么科', '科室']
        # self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
        #                   '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']

        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        s = ""
        for key in medical_dict.keys():
            s= key
        data['name'] = s
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []


        if self.check_words(self.effect_qwds, question) and ('effect' in types):
            question_type = 'effect_reason'
            question_types.append(question_type)


        # 故障解决方式
        if self.check_words(self.cureway_qwds, question) and ('effect' in types):
            question_type = 'effect_task'
            question_types.append(question_type)


        # 若没有查到相关的外部查询信息，那么则将该故障的描述信息返回
        if question_types == [] and 'effect' in types:
            question_types = ['effect_task']


        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        # data['name'] =
        return data

    '''构造词对应的类型'''
    # 构造了 实例 与 名称 的反向映射
    def build_wdtype_dict(self):
        wd_dict = dict()
        # self.mainsystem_wds + self.product_wds + self.task_wds + self.function_wds + self.fail_wds +
        # self.subsystem_wds + self.effect_wds + self.cause_words
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.mainsystem_wds:
                wd_dict[wd].append('mainsystem')
            if wd in self.product_wds:
                wd_dict[wd].append('product')
            if wd in self.task_wds:
                wd_dict[wd].append('task')
            if wd in self.function_wds:
                wd_dict[wd].append('function')
            if wd in self.fail_wds:
                wd_dict[wd].append('fail')
            if wd in self.subsystem_wds:
                wd_dict[wd].append('subsystem')
            if wd in self.effect_wds:
                wd_dict[wd].append('effect')
            if wd in self.cause_wds:
                wd_dict[wd].append('cause')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}
        # print(final_dict)
        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

# 为什么失去N2限制冗余？
# 怎么处理失去N2限制冗余？
if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)