basic-xss-spider
============

```python basic-xss-spider.py -u "http://danmcinerney.org"```

Spiders http://danmcinerney.org concurrently opening URLs found then checks those URLs for variables. If URL variables are found, tests those variables with dangerous XSS characters ```"'><()=;/:```


If it finds all or some important characters in the response HTML it will add the URL to the vulnerable_URLs.txt logfile. Uses requests and gevent for async capabilities.


Definitely not without bugs. Rewriting in Scrapy.
