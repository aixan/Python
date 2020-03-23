```
1. random.random()
　　random.random()方法返回一个随机数，其在0至1的范围之内，以下是其具体用法：
　　import random
　　print ("随机数: ", random.random())
　　输出结果：0.22867521257116

2. random.uniform()
　　random.uniform()是在指定范围内生成随机数，其有两个参数，一个是范围上限，一个是范围下线，具体用法如下：
　　import random
　　print (random.uniform(2, 6))
　　输出结果：3.62567571297255

3. random.randint()
　　random.randint()是随机生成指定范围内的整数，其有两个参数，一个是范围上限，一个是范围下线，具体用法如下：
　　import random
　　print (random.randint(6,8))
　　输出结果：8

4. random.randrange()
　　random.randrange()是在指定范围内，按指定基数递增的集合中获得一个随机数，有三个参数，前两个参数代表范围上限和下限，第三个参数是递增增量，具体用法如下：
　　import random
　　print (random.randrange(6, 28, 3))
　　输出结果：15

5. random.choice()
　　random.choice()是从序列中获取一个随机元素，具体用法如下：
　　import random
　　print (random.choice("www.jb51.net"))
　　输出结果：w

6. random.shuffle()
　　random.shuffle()函数是将一个列表中的元素打乱，随机排序，具体用法如下：
　　import random
　　num = [1, 2, 3, 4, 5]
　　random.shuffle(num)
　　print (num)
　　输出结果：[3, 5, 2, 4, 1]

7. random.sample()
　　random.sample()函数是从指定序列中随机获取指定长度的片段，原有序列不会改变，有两个参数，第一个参数代表指定序列，第二个参数是需获取的片段长度，具体用法如下：
　　import random
　　num = [1, 2, 3, 4, 5]
　　sli = random.sample(num, 3)
　　print (sli)
　　输出结果：[2, 4, 5]
```