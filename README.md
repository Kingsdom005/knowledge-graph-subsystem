# knowledge-graph-subsystem🚀
## Why this?🤨

```shell
This is a software engineering assignment. We are the first group whose main aim is to crawl Chinese artifacts from 5 foreign museums and build a visual Neo4j graph database.
```

## How to run locally?🤨

Please switch the correct path at first and run the following commands.

**Clone the project into local site**

```shell
git clone git@github.com:Kingsdom005/knowledge-graph-subsystem.git
```

**Install dependency packages**

```
pip install -r requirements.txt
```

**Run spider to crawl site2/7/12/17/22 and output files**

```shell
scrapy crawl site2 -o save/2.json -o save/2.csv
scrapy crawl site7 -o save/7.json -o save/7.csv
scrapy crawl site12 -o save/12.json -o save/12.csv
scrapy crawl site17 -o save/17.json -o save/17.csv
scrapy crawl site22 -o save/22.json -o save/22.csv
```

## How to get multiple triples?🤨

**Converting all data into a triplet**

You can modify the data source in a fixed format.

```shell
python excel.py
```

The data source we crawled have been published at https://sncdeveloper.cn/2-7-12-17-22.json
