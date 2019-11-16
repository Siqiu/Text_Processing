'''
\d any number
\D anything but a number
\s space
\S anything but a space
\w any character
\W anything but a character
. any character, except for a newline
\. aperiod
\b the whitespace around words


Moddifiers:
{1,3} we're expecting 1-3
+ Match 1 or more
? Match 0 or 1
* Match 0 or more

$ match the and of a string
^ matching the beginning of string
| either or
[] range or "variance" [1-5a-qA-Z]
{x} expecting "x" amount

white Space Characters:
\n new line
\s space
\t tab

\e escape
\f form feed
\r return


re 所定义的 flag 包括：

re.I 忽略大小写

re.L 表示特殊字符集 \w, \W, \b, \B, \s, \S 依赖于当前环境

re.M 多行模式

re.S 即为’ . ’并且包括换行符在内的任意字符（’ . ’不包括换行符）

re.U 表示特殊字符集 \w, \W, \b, \B, \d, \D, \s, \S 依赖于 Unicode 字符属性数据库

re.X 为了增加可读性，忽略空格和’ # ’后面的注释
'''
import re

exampleString = '''
Jessica is 15 years old, and Daniel is 27 years old.
Edward is 97, and his grandfather, Oscar, is 102.
'''
ages = re.findall(r'\d{1,3}', exampleString)
# [][] between these 2 square bracket, there is no SPACE
names = re.findall(r'[A-Z][a-z]*', exampleString)
print(ages)
print(names)

ageDict = {}
x = 0
for eachName in names:
    ageDict[eachName] = ages[x]
    x += 1

print(ageDict)

# ######################################################################################################################
content = '''email:12345678@163.com
email:2345678@163.com
email:345678@163.com
'''
# ######################################################################################################################
# 需求：（正则没有分组）提取所有的邮箱信息

result_finditer = re.finditer(r"\d+@\w+.com", content)
# 由于返回的为MatchObject的iterator，所以我们需要迭代并通过MatchObject的方法输出
for i in result_finditer:
    print(i.group())
# 12345678@163.com
# 2345678@163.com
# 345678@163.com

result_findall = re.findall(r"\d+@\w+.com", content)
# 返回一个[]  直接输出or或者循环输出
print(result_findall)
# ['12345678@163.com', '2345678@163.com', '345678@163.com']
for i in result_findall:
    print(i)
# 12345678@163.com
# 2345678@163.com
# 345678@163.com

# ######################################################################################################################
# 需求：（正则有分组）提取出来所有的电话号码和邮箱类型


result_finditer = re.finditer(r"(\d+)@(\w+).com", content)
# 正则有两个分组，我们需要分别获取分区，分组从0开始，group方法不传递索引默认为0，代表了整个正则的匹配结果
for i in result_finditer:
    phone_no = i.group(1)
    email_type = i.group(2)

result_findall = re.findall(r"(\d+)@(\w+).com", content)
# 此时返回的虽然为[]，但不是简单的[],而是一个tuple类型的list
# 如：[('12345678', '163'), ('2345678', '163'), ('345678', '163')]
for i in result_findall:
    phone_no = i[0]
    email_type = i[1]

# Notes: findall
# 1.当正则没有分组是返回的就是正则的匹配
#
# re.findall(r"\d+@\w+.com", content)
# ['2345678@163.com', '2345678@163.com', '345678@163.com']
#
#
# 2.有一个分组返回的是分组的匹配而不是整个正则的匹配
#
# re.findall(r"(\d+)@\w+.com", content)
# ['2345678', '2345678', '345678'] only return the group(1)
#
#
# 3.多个分组时将分组装到tuple中 返回
#
# re.findall(r"(\d+)@(\w+).com", content)
# [('2345678', '163'), ('2345678', '163'), ('345678', '163')]
# 1. 匹配”ABAB”型字符串
s = 'abab cdcd efek'
p = re.compile(r'(\w\w)\1')
print(re.findall(p, s))

# 2. 匹配”AABB”型字符串
s = 'abab cdcd xxyy'
p = re.compile(r'(\w)\1(\w)\2')
print(re.findall(p, s))

# 3. 匹配”AABA”型字符串
s = 'abab cdcd xxyx'
p = re.compile(r'(\w)\1(?:\w)\1')
print(re.findall(p, s))

# 4. 匹配”ABBA”型字符串
s = 'oababt toot'
p = re.compile(r'(\w)(\w)\2\1')
print(re.findall(p, s))

