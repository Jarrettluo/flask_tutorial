#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   21:41
@Auther  : Jarrett
@FileName: test_code
@Software: PyCharm
"""
import heapq

most_recommend = [1, 2, 3, 3]
post_value = 2
re1 = map(most_recommend.index, heapq.nlargest(post_value, most_recommend))  # 找到支持人最多的的
print(list(re1))

d = {1: 1, 2: 0, 3: 0, 4: 1}
v = sorted(d.items(), key=lambda d: d[1])  # 按照value进行排序
v.reverse()
print(v)
print(dict(v))
sorted_list = [(3, 1), (0, 1), (2, 0), (1, 0)]
for lit in sorted_list:
    print(lit[0])
    print(lit[1])

{% block scripts %}
<!--<script src={{ url_for('static', filename='vendor/jquery.min.js') }}></script>-->
<script src={{ url_for('static', filename='js/bootstrap.min.js') }}></script>
<script src={{ url_for('static', filename='js/my.js') }}></script>
{% endblock %}

<!-- {% block styles %}

{% endblock %} -->
