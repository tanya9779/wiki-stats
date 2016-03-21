#!/usr/bin/python3

import os
import sys
import math
import codecs

import array

import statistics

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with codecs.open(filename,'r','utf-8') as f:

            (n, _nlinks) = map(int, f.readline().split()) # прочитать из файла кол-во статей n и кол-во ссылок _nlinks
            
            self._titles = []
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))

            self._offset.append(0) # вначале нужно поставить 0
            total_loaded_links = 0 # будем подсчитывать кол-во для поддержания массива _offset
            for i in range(n): # загружаем статью номер i
                s = f.readline() # буду бережно расходовать память
                self._titles.append(s) # загрухаем название i статьи
                s = f.readline()
                (size_bytes, is_redir, outgo_link_no) = map(int,s.split()) # размер в байтах, флаг перенаправ, кол-во ссылок
                self._sizes[i] = size_bytes
                self._redirect[i] = is_redir
                for j in range(outgo_link_no): # зарузим все статьи, на которые ссылается текущая статья
                    s = f.readline()
                    self._links.append(int(s))
                total_loaded_links += outgo_link_no
                self._offset.append(total_loaded_links) # кол-во статей, на которые ссылается текущая (i-ая), вычисля-
                                               # естся по формуле _offset[i+1] - _offset[i]


        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        pass

    def get_links_from(self, _id):
        pass

    def get_id(self, title):
        pass

    def get_number_of_pages(self):
        pass

    def is_redirect(self, _id):
        pass

    def get_title(self, _id):
        pass

    def get_page_size(self, _id):
        pass


def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    # TODO: нарисовать гистограмму и сохранить в файл


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
    else:
        print('Файл с графом не найден')
        sys.exit(-1)

    # TODO: статистика и гистограммы