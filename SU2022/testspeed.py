# coding=utf-8
'''
@Author: King
@Date: 2022-01-12 10:06:07
@Email: 13321998692@163.com
@Url: http://www.yydbxx.cn
'''
from runsingle import electsingle

if __name__ == '__main__':
    qk = electsingle('ABE8B07F7B391C30003109016EAB1B2C',
                     '209E229F-7BC8-448F-A9D2-8DAAE2D89357', 'C9821C55-2950-459A-8DB9-454588C22F7B',thread_number=10, max_try=10)
    qk.run()
