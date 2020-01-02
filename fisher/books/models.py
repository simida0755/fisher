from django.db import models

# title = Column(String(50), nullable=False)
# auther = Column(String(30), default='未名')
# binding = Column(String(20))
# publisher = Column(String(50))
# price = Column(String(20))
# pages = Column(Integer)
# pubdate = Column(String(20))
# isbn = Column(String(15), nullable=False, unique=True)
# summary = Column(String(1000))
# image = Column(String(50))
from fisher.base.model import Base


class Book(Base):
    title = models.CharField('书名', max_length=50)
    author = models.CharField('作者', max_length=30)
    binding = models.CharField('精装', max_length=20)
    publisher = models.CharField('出版商', max_length=50)
    price = models.CharField('价格', max_length=20)
    pages = models.IntegerField('页数')
    pubdate = models.CharField('出版年', max_length=20)
    isbn = models.CharField('isbn',max_length=15,null=False,unique=True)
    summary = models.CharField('内容简介', max_length=1000)
    image = models.CharField('封面',max_length=50)


    @property
    def intor(self):
        intors = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intors)

    def auther_save(self,dict):
        if dict['author']:
            self.author = dict['author'][0]
