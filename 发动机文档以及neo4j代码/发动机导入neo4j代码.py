'''
goal: 将 预处理后的中文数据以及数据间的关系 导入neo4j数据库里
author: ts
data: 2055/5/26
'''



# coding:utf-8
#xlwt 和 xlrd 都支持对excel文件格式为xls文件进行操作
#xlrd只支持对Excel文件格式为xls文件的读取
#xlwt只支持对Excel文件格式为xls文件的写入
import xlwt
import xlrd

from py2neo import Graph, Node, Relationship
# 估计可能是包升级了 用户名要用 user 代替
graph = Graph('http://localhost:7474', user='neo4j', password='123456789')


# from py2neo import Graph, Node, Relationship
# graph = Graph('http://localhost:7474', user='neo4j', password='123456789')
# node = Node("Disease", name='name')
# graph.create(node)


##连接neo4j数据库，输入地址、用户名、密码

book = xlrd.open_workbook('D://各种资料//毕设//发动机文档以及neo4j代码//发动机燃油控制.xlsx')

workSheetName = book.sheet_names()
print("Excel文件包含的表单有："+str(workSheetName))

# 根据指定的表单名,一行一行获取指定表单中的所有数据，表单名为worksheetname
def GetAllSheetCellValue(worksheetname):
    engineStructure = book.sheet_by_name(worksheetname)
    AllsheetValue = []
    for i in range(engineStructure.nrows):
        for j in range(engineStructure.ncols):
            AllsheetValue.append(engineStructure.cell_value(i,j))
    return AllsheetValue

# 根据指定的表单名，按列获取表单中的数据
def GetAllSheetValueByColum(worksheetname):
    engineStructure = book.sheet_by_name(worksheetname)#获取指定名称的表单
    col_nums = engineStructure.ncols #获取指定表单的有效列
    AllsheetValue = []
    for i in range(col_nums):
        AllsheetValue.append(engineStructure.col_values(i))
    # print(AllsheetValue)
    return AllsheetValue

# 创建一个指定节点类，名字，创建节点,其他属性有需要自定拓展这个方法
def CreateNode(className,lableName,name):
    test_node= Node(className, lable=lableName, name=name)
    graph.create(test_node)

# 指定表名，类名，名字，批量创建节点
def CreateNodes(worksheetname,lableName,ClassName):
    sheetvalue = GetAllSheetCellValue(worksheetname)
    #去重
    sheetvalue = list(set(sheetvalue))
    nums = 0
    for i in range(len(sheetvalue)):
        CreateNode(ClassName,lableName, sheetvalue[i])
        nums+=1
    print("创建"+worksheetname+"节点成功，总计创建%s个"%(nums))

# 根据需要创建节点的表名个数(有几个表就传输参数是几)，批量创建节点，这个方法中默认构件类名就是图谱中的类名
# 参数说明 nums：在一个Excel文件中的需要创建节点的表单数
def CreateNodesBySheetNums(nums):
    for i in range(nums):
        CreateNodes(workSheetName[i], workSheetName[i], workSheetName[i])

# 根据Excel文件中两个对象列表和一个关系列表，建立两个列表之间的子类（subclassof）关系
# 参数说明 worksheetname：指定的表单名,className1:第一个类的名称，className2：第二个类的名称
def subclassRelationship(worksheetname, className1,className2):
    list1 = GetAllSheetValueByColum(worksheetname)[0]
    list2 = GetAllSheetValueByColum(worksheetname)[2]
    relationship = GetAllSheetCellValue(worksheetname)[1]
    # 利用Python执行CQL语句

    for i in range(len(list1)):
        graph.run("match(a:%s),(b:%s)  where a.name='%s' and b.name='%s'  MERGE (a)-[r:%s{weight: 0.8}]->(b) RETURN r"%(className1,className2,list1[i],list2[i],relationship))
    print("创建关系 %s - %s 完成"%(className1 , className2))


#创建节点
CreateNodesBySheetNums(8)


#创建关系
subclassRelationship(workSheetName[8],"产品","主系统")
subclassRelationship(workSheetName[9],"主系统","子系统")
subclassRelationship(workSheetName[10],"子系统","功能")
subclassRelationship(workSheetName[11],"功能","失效形式")
subclassRelationship(workSheetName[12],"失效形式","影响")
subclassRelationship(workSheetName[13],"影响","造成原因")
subclassRelationship(workSheetName[14],"造成原因","任务")

print("程序运行完成")
