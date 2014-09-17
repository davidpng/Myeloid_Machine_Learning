import os
import pickle
import random

if __name__ == '__main__':
    pwd = '/home/davidng/Test1'
    years = [10, 11, 12, 13]
    numbers = list(range(10000))

    filelist = open(pwd + '/list_of_files.txt','w')

    dir = pwd + '/archive/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    for i in range(10):
        year = str(random.choice(years))
        num = str(random.choice(numbers))
        fcs_filename = "{}_{:0>5}_test 1.fcs".format(year, num)
        filelist.write(fcs_filename + '\n')
        fcs_file = open(dir + fcs_filename, 'w')
        fcs_file.write('The filename is ' + fcs_filename + '\n')
        fcs_file.write(str([random.randrange(1,2**18) for i in range(10000)]))
        fcs_file.close()
    filelist.close()