# coding: utf-8
#!/usr/bin/python3

import os
import sys
import math

import array

import statistics
import numpy

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)


import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename) as f:

            (n, _nlinks) = map(int, f.readline().split()) # прочитать из файла кол-во статей n и кол-во ссылок _nlinks
            
            self._titles = []
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))

            self._offset[0] = 0 # вначале нужно поставить 0
            total_loaded_links = 0 # будем подсчитывать кол-во для поддержания массива _offset
            for i in range(n): # загружаем статью номер i
                s = f.readline() # построчная загрузка - буду бережно расходовать память
                self._titles.append(s.strip()) # загружаем название i статьи
                s = f.readline()
                (size_bytes, is_redir, outgo_link_no) = map(int,s.split()) # размер в байтах, флаг перенаправ, кол-во ссылок
                self._sizes[i] = size_bytes
                self._redirect[i] = is_redir
                for j in range(outgo_link_no): # зарузим все статьи, на которые ссылается текущая статья
                    s = f.readline()
                    self._links[total_loaded_links + j] = int(s.strip())
                total_loaded_links += outgo_link_no
                self._offset[i+1] = total_loaded_links # кол-во статей, на которые ссылается текущая (i-ая), вычисля-
                                               # естся по формуле _offset[i+1] - _offset[i]


        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        return self._offset[_id+1] - self._offset[_id]

    def get_links_from(self, _id):
        return self._links[self._offset[_id]:self._offset[_id+1]]

    def get_id(self, title):
        return self._titles.index(title)

    def get_number_of_pages(self):
        return len(self._titles)

    def is_redirect(self, _id):
        return self._redirect[_id]

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes[_id]

    def BFS(self, start, finish): # ф-ция поиска в ширину от узла start до finish
        queue = [start]
        visited = {start:None} # ключем будет id текущей вершины, значением id родителя
        while queue:
            v = queue.pop(0)
            if v == finish:
                return visited # нужно "перевернуть" этот  "путь"
            for i in self.get_links_from(v): # по всем соседям пройдемся
                if i not in visited.keys():
                    visited[i] = v # текущую вершину метим как посещенную и запонимаем ее родителя
                    queue.append(i)
        return None
    # end of BFS()


def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    # TODO: нарисовать гистограмму и сохранить в файл
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

    plt.hist(data,bins,color=facecolor,label=title,**kwargs)
    plt.savefig(fname)
    plt.show()

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

    # СТАТИСТИКА
    total = wg.get_number_of_pages()
    # количество статей с перенаправлением
    total_pages_with_redirect = sum(wg.get_number_of_links_from(i) for i in range(total) if wg.is_redirect(i))
    print('статей с перенаправлением:', total_pages_with_redirect, '(%.2f'%(total_pages_with_redirect/total*100)+'%)')

    # в отдельный список соберем кол-во ссылок из статьи (без перенаправлений)
    arr_links_from = array.array('L') # длина массива неизвестна
    arr_links_from.extend( wg.get_number_of_links_from(i) for i in range(total) if not wg.is_redirect(i) )
    # отладка
    # print('total =',total,'    arr_links_from length =',len(arr_links_from))
    # длина массива оказалась меньше чем total

    # минимальное кол-во ссылок из статьи
    min_links_from = min(arr_links_from)
    print('минимальное кол-во ссылок из статьи:', min_links_from)
    # кол-во статей с минимальным кол-вом ссылок
    pages_with_min_links_from = arr_links_from.count(min_links_from)
    print('кол-во статей с минимальным кол-вом ссылок:', pages_with_min_links_from)
    # максим кол-во ссылок из статьи
    max_links_from = max(arr_links_from)
    print('максимальное кол-во ссылок из статьи:', max_links_from)
    # кол-во статей с максим кол-вом ссылок
    pages_with_max_links_from = arr_links_from.count(max_links_from)
    print('кол-во статей с максимальным кол-вом ссылок:', pages_with_max_links_from)
    # статья с наибольшим  кол-вом ссылок
    for i in range(total): # на случай если их несколько
        # ВАЖНО: использовать индекс i списка arr_links_from[i] нельзя, т.к. len(arr_links_from) != total
        if wg.get_number_of_links_from(i) == max_links_from:
            print('статья с наибольшим  кол-вом ссылок:', wg.get_title(i) )
    # среднее количество ссылок в статье
    average_links_from = statistics.mean(arr_links_from)
    stdev_links_from = statistics.stdev(arr_links_from)
    print('среднее количество ссылок в статье: %.2f'%average_links_from,'(ср.откл. %.2f)'%stdev_links_from)

    # в отдельный список соберем кол-во внешних ссылок на статью (использeем array.array)
    # ВАЖНО: перенаправление не считается внешней ссылкой
    # если этот список сформировать без перенаправлений, то не сможем легко вычислить статью с наиб. кол-вом внеш ссылок
    incoming_links_no = array.array('L', [0]*total) # посчитаем для каждой статьи кол-во ссылок на нее
    for i in range(total):
        if not wg.is_redirect(i): # перенаправление не считается внешней ссылкой
            for j in wg.get_links_from(i):
                incoming_links_no[j] += 1
    # отладка
    #print('Size of arr_links_from: ',sys.getsizeof(arr_links_from))
    #print('Size of incoming_links_no: ',sys.getsizeof(incoming_links_no))
    # первый массив получен вызовом extend() но все равно расходует ~4 байта на элемент

    # минимальное количество ссылок на статью (перенаправление не считается внешней ссылкой)
    min_links_to = min(incoming_links_no)
    print('минимальное количество ссылок на статью:', min_links_to)
    # количество статей с минимальным количеством внешних ссылок
    pages_with_min_links_to = sum(1+0*i for i in range(total) if incoming_links_no[i]==min_links_to and not wg.is_redirect(i))
    print('количество статей с минимальным количеством внешних ссылок:', pages_with_min_links_to)
    # максимальное количество ссылок на статью
    max_links_to = max(incoming_links_no)
    print('максимальное количество ссылок на статью:', max_links_to)
    # количество статей с максимальным количеством внешних ссылок
    pages_with_max_links_to = sum(1+i*0 for i in range(total) if incoming_links_no[i]==max_links_to and not wg.is_redirect(i))
    print('количество статей с максимальным количеством внешних ссылок:', pages_with_max_links_to)
    # статья с наибольшим количеством внешних ссылок
    print('статья с наибольшим количеством внешних ссылок:',
          wg.get_title(incoming_links_no.index(max_links_to) ) )
    # среднее количество внешних ссылок на статью
    average_links_to = statistics.mean(incoming_links_no[i] for i in range(total) if not wg.is_redirect(i))
    stdev_links_to = statistics.stdev(incoming_links_no[i] for i in range(total) if not wg.is_redirect(i))
    print('среднее количество внешних ссылок на статью: %.2f'%average_links_to,'(ср.откл. %.2f)'%stdev_links_to)

    # минимальное количество перенаправлений на статью
    external_redirection = array.array('L', [0]*total) # посчитаем кол-во перенаправлений на каждую статью
    for i in range(total):
        if wg.is_redirect(i): # если вместо статьи перенаправление, то всего одна ссылка
            external_redirection[wg.get_links_from(i)[0]] += 1
    min_redirection = min(external_redirection)
    print( 'минимальное количество перенаправлений на статью:', min_redirection)
    # количество статей с минимальным количеством внешних перенаправлений
    pages_with_min_redirect = external_redirection.count(min_redirection)
    print('количество статей с минимальным количеством внешних перенаправлений:', pages_with_min_redirect)
    # максимальное количество перенаправлений на статью
    max_redirection = max(external_redirection)
    print( 'максимальное количество перенаправлений на статью:', max_redirection)
    # количество статей с максимальным количеством внешних перенаправлений
    pages_with_max_redirect = external_redirection.count(max_redirection)
    print('количество статей с максиммальным количеством внешних перенаправлений:', pages_with_max_redirect)
    # статья с наибольшим количеством внешних перенаправлений
    print('статья с наибольшим количеством внешних перенаправлений:',
               wg.get_title( external_redirection.index(max_redirection) ) )
    # среднее количество внешних перенаправлений на статью
    average_redirect = statistics.mean(external_redirection)
    stdev_redirect = statistics.stdev(external_redirection)
    print('среднее количество внешних перенаправлений на статью: %.2f'%average_redirect,
               '(ср.откл. %.2f)'%stdev_redirect)

    # путь, по которому можно добраться от статьи "Python" до статьи "Боль"
    first_page = wg.get_id('Python')
    last_page  = wg.get_id('Боль')
    # воспользуемся поиском в ширину с указанием вершины-цели
    print('Запускаем поиск в ширину.')
    revers_path = wg.BFS(first_page,last_page) # получим путь обратно без last_page в виде словаря
    if revers_path:
        print('Поиск закончен. Найден путь:')
        # из словаря {id потомка : id родителя} нужно распечатать прямой путь
        direct_path = [last_page] # это список из id статей - прямой путь
        current = last_page
        while revers_path[current]: # значением для ключа first_page является None:
            current = revers_path[current]
            direct_path.insert(0,current) # вставка спереди
        for i in direct_path:
            print(wg.get_title(i))
    else:
        print('Поиск закончен. Путь не найден. (')


    # гистограммы
    # print('Выводим гистограммы (по очереди)')
    # распределение количества ссылок из статьи
    hist('links_from.png',arr_links_from,100,'$Количество$ $статей$','$Количество$ $ссылок$',
         '$Распределение$ $количества$ $ссылок$ $из$ $статьи$', range=(0,200))
    # распределение количества ссылок на статью
    hist('links_to.png',[incoming_links_no[i] for i in range(total) if not wg.is_redirect(i)],100,'$Количество$ $статей$',
         '$Количество$ $ссылок$','$Распределение$ $количества$ $ссылок$ $на$ $статью$', range=(0,200))
    # распределение количество перенаправлений на статью
    hist('redirect_to.png',external_redirection,20,'$Количество$ $статей$','$Количество$ $ссылок$',
         '$Распределение$ $количества$ $перенаправлений$ $на$ $статью$', range=(0,20))
    # распределение размеров статей
    # соберем соответсвующий массив
    arr_page_size = array.array('L')
    arr_page_size.extend([wg.get_page_size(i) for i in range(total) if not wg.is_redirect(i)])
    hist('page_size.png',arr_page_size,100,'$Размер$ $статьи$','$Количество$ $статей$',
         '$Распределение$ $размеров$ $статей$', range=(0,100000))
    # распределение размеров статей в логарифмическом масштабе
    plt.ylim( (0,300) )
    hist('page_size_log.png',numpy.log10(arr_page_size),25,'$Размер$ $статьи$','$Количество$ $статей$',
         '$Распределение$ $размеров$ $статей$ $(в$ $логарифмическом$ $масштабе)$',range=(0,6))
