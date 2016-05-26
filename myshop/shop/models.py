from django.db import models
from django.core.urlresolvers import reverse

class Category(models.Model):
 name = models.CharField(max_length=200, db_index=True)
 slug = models.SlugField(max_length=200, db_index=True, unique=True)

 class Meta:
  ordering = ('name',)
  verbose_name = 'category'
  verbose_name_plural = 'categories'
 
 def __str__(self):
  return self.name

 def get_absolute_url(self):
  return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
 category = models.ForeignKey(Category, related_name='products')
 name = models.CharField(max_length=200, db_index=True)
 slug = models.SlugField(max_length=200, db_index=True)
 image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
 description = models.TextField(blank=True)
 price = models.DecimalField(max_digits=10, decimal_places=2)
 stock = models.PositiveIntegerField()
 available = models.BooleanField(default=True)
 created = models.DateTimeField(auto_now_add=True)
 updated = models.DateTimeField(auto_now=True)

 class Meta:
  ordering = ('name',)
  index_together = (('id', 'slug'),)

 def __str__(self):
  return self.name

 def get_absolute_url(self):
  return reverse('shop:product_detail', args=[self.id, self.slug])

class DataSet(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    code = models.CharField(max_length=400)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:dataset_detail', args=[self.name])

class DataView(models.Model):
    dataset = models.ForeignKey(DataSet, related_name='dataviews')
    name = models.CharField(max_length=200, db_index=True)
    parameters = models.CharField(max_length=500)
    row_range = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:dataview_detail', args=[self.name])

class Run(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    train_dv = models.ForeignKey(DataView, related_name='train_runs')
    test_dv = models.ForeignKey(DataView, related_name='test_runs')
    formula = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:run_detail', args=[self.name])

