# 判断两个文件是否相同。要求用函数实现文件比较功能，在main函数中进行验证。
# 下述函数完成文件是否相同的比较功能
def compare_file(file_1, file_2):
    # 请在此添加代码，实现文件是否相同的判断
    # 如果相等返回[1,0,0]
    # 如果不相等返回[0,a,b] a,b表示第一个不相等字符所在的行号和列号
    # ********** Begin *********#
    len1 = len(file_1)
    len2 = len(file_2)
    min_len1 = min(len1, len2)  # 计算两个列表的最小行数
    for i in range(min_len1):  # 用最小行数进行迭代和比较
        # 如果两行不相等，判断是在哪一列不相等
        if file_1[i] != file_2[i]:
            # 获取这两行最小列数
            min_len2 = min(len(file_1[i]), len(file_2[i]))
            for j in range(min_len2):  # 用最小的列数进行迭代和比较
                if file_1[i][j] != file_2[i][j]:
                    return [0, i + 1, j + 1]  # 返回不相等所在的行号和列号
            else:
                # 若这两行的列数不相同，则也不相等
                if len(file_1) != len(file_2):
                    return [0, i + 1, 1]
    else:
        # 若这两个文件的行数不同，则也不相等
        if len(file_1) != len(file_2):
            return [0, min_len1 + 1, 1]
        else:
            return [1, 0, 0]
    # ********** End *********#


# 定义函数main，完成文件名输入、比较函数调用和结果输出功能
if __name__ == '__main__':
    # 输入两个文件所在路径和文件名，如：d:\temp\t1.txt
    str1 = input('/Users/yuanxiujing/Desktop/白名单fox.csv')
    str2 = input('/Users/yuanxiujing/Desktop/白名单contact.csv')
    # 请在此添加代码，完成相应功能
    # ********** Begin *********#
    file1 = open(str1, 'r')
    file2 = open(str2, 'r')  # 以只读方式打开文件
    # 用readlines（）方法把文件内容逐行读入一个列表对象
    is_file1 = file1.readlines()
    is_file2 = file2.readlines()
    file1.close()
    file2.close()
    result, row, col = compare_file(is_file1, is_file2)
    if result == 1:
        # 函数第一个返回结果为1，则相等
        print("这两个文件相等")
    else:
        print("这两个文件在{0}行{1}列开始不相等".format(row, col))
    # ********** End *********#

