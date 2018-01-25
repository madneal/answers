目前来说各种答题辅助对于答题 APP 题目的文字的识别基本都没有太大的问题，主要的问题就是现在答案的搜索上。因为现在的题目出题方式越来越妖，直接去百度搜索或者百度搜索，或者统计搜索的结果数都是不太准确的。所以我希望能通过 [elasticsearch](https://www.elastic.co/products/elasticsearch) 来建立一个问题题库，当然题库的建设需要其他人的建设和参与。

## ElasticSearch
* [下载地址](https://www.elastic.co/downloads/elasticsearch)
* 使用起来比较简单，直接运行 `bin/elasticsearch` 或者 `bin/elasticsearch.bat`（windows 平台）即可。

## Config
* 主要包括百度 ocr API 的相关配置以及截图区域的配置，按照 `config/config.template.yaml`来进行配置。


