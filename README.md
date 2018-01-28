## 构建题库
目前答题应用最关键的就是搜索算法了，现在利用 ocr 去识别图片已经不是关键问题，最关键的是如何搜索到正确的答案。现在出题的方式也越来越诡异，所以建立题库就很有必要了。

目前来说各种答题辅助对于答题 APP 题目的文字的识别基本都没有太大的问题，主要的问题就是现在答案的搜索上。因为现在的题目出题方式越来越妖，直接去百度搜索或者百度搜索，或者统计搜索的结果数都是不太准确的。所以我希望能通过 [elasticsearch](https://www.elastic.co/products/elasticsearch) 来建立一个问题题库，当然题库的建设需要其他人的建设和参与。

部分代码主要是来自于 [TopSup](https://github.com/Skyexu/TopSup)，主要增加的是题库的建立方法以及在题库中搜索的方法。

## ElasticSearch
* [下载地址](https://www.elastic.co/downloads/elasticsearch)
* 使用起来比较简单，直接运行 `bin/elasticsearch` 或者 `bin/elasticsearch.bat`（windows 平台）即可。
* 验证 elasticsearch 是否正确运行， 打开浏览器访问 `http://localhost:9200` 出现结果为：
```
{
  "name" : "69VnU74",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "_ApoeosaQO24L7XfZUJ_1A",
  "version" : {
    "number" : "6.1.2",
    "build_hash" : "5b1fea5",
    "build_date" : "2018-01-10T02:35:59.208Z",
    "build_snapshot" : false,
    "lucene_version" : "7.1.0",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

## Config
* 主要包括百度 ocr API 的相关配置以及截图区域的配置，按照 `config/config.template.yaml`来进行配置。

## 贡献题库方式
有两种方式你可以贡献题库，一种是通过文本方式，另外一种是上传图片的方式。

### 文本方式
你只要在 `questions.txt` 最后一行添加文字就可以了，问题和答案之间应该有一个空格。

### 上传图片
只要在 img 文件内上传符合要求的图片即可：
![pvsFk6.png](https://s1.ax1x.com/2018/01/28/pvsFk6.png)

利用图片创建题库的方式一开始存在一个问题，如何从选项中找到正确的选项呢。一开始想通过选项的数字来判断，但是正确的选项并不一定是选择人数最多的。感谢图像处理这门课程，我想起来彩色的图片转换成灰度图的时候，灰度值应该比灰色图像的高。正确选项的背景颜色是彩色的，所以我们只要截图选项区域，然后通过两个阈值来过滤，设置阈值为 120 可以获得所有选项，设置阈值为 190 则不包含正确的选项，通过这个差别就可以找到正确的选项了。

## 运行
程序运行只要执行 `python main.py` 即可，建立题库需要运行 `python creat_question_bank.py`

## License
[MIT](https://github.com/neal1991/answers/blob/master/LICENSE)
