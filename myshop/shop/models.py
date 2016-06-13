from django.db import models
from django.core.urlresolvers import reverse
from mptt.models import MPTTModel, TreeForeignKey
from multiselectfield import MultiSelectField
import pandas as pd

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
    dataframe = models.TextField()
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:dataset_detail', args=[self.id])

class DataView(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    dataset = models.ForeignKey(DataSet, related_name='dataviews')
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:dataview_detail', args=[self.id])

class DataTransformation(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    feature = models.CharField(max_length=200)
    dataview = models.ForeignKey(DataView, related_name='transformations')
    def __str__(self):
        return "{} - {} - {}".format(self.name, self.type, self.feature)

class Run(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    train_dv = models.ForeignKey(DataView, related_name='train_runs')
    test_dv = models.ForeignKey(DataView, related_name='test_runs')
    formula = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:run_detail', args=[self.name])

class Analysis(models.Model):
    title = models.CharField(max_length=200)
    data_view = models.ForeignKey(DataView, related_name='data_view_analyses')
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('shop:analysis_detail', args=[self.id])

class Accordion(models.Model):
    title = models.CharField(max_length=200)
    analysis = models.ForeignKey(Analysis, related_name='analysis_accordions')
    def __str__(self):
        return self.title

class Panel(models.Model):
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    accordion = models.ForeignKey(Accordion, related_name='accordion_panels')
    RESULT_FUNCTIONS = (('histogram', 'Histogram'), ('scatterplot', 'Scatterplot'), ('heatmap', 'Heatmap'),
                        ('network', 'Network'))
    result_function_name = models.CharField(max_length=200, choices=RESULT_FUNCTIONS, default='histogram')
    def __str__(self):
        return self.title
    def panel_body_id(self):
        return "panel_body_{}".format(self.id)
    def panel_body_target_id(self):
        return "#{}".format(self.panel_body_id())
    def panel_result_id(self):
        return "panel_result_{}".format(self.id)

class Slider(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    default_value = models.IntegerField()
    step = models.IntegerField()
    min = models.IntegerField()
    max = models.IntegerField()
    current_value = models.IntegerField()
    is_percent = models.BooleanField(default=False)
    parent = models.ForeignKey(Panel, related_name='panel_sliders')
    
    def slider_id_hash(self):
        return "#slider_{}".format( self.id )
    
    def label_id_hash(self):
        return "#slider_label_{}".format(self.id)

    def slider_id(self):
        return "slider_{}".format( self.id )

    def label_id(self):
        return "slider_label_{}".format( self.id )
    
    def slider_label(self):
        return "{}: {}".format(self.name, self.current_value)

    def __str__(self):
        return self.name

class Controller(models.Model):
    TYPE_CHOICES=(('slider', 'Slider'), ('single_dropdown', 'Single Dropdown'), ('multiple_dropdown', 'Multiple Dropdown'))
    default_value = models.IntegerField()
    step = models.IntegerField()
    min = models.IntegerField()
    max = models.IntegerField()
    variable = models.CharField(max_length=200, db_index=True)
    type = models.CharField(max_length=200, choices=TYPE_CHOICES, default='slider')
    panel = models.ForeignKey(Panel, related_name='controllers')
    def __str__(self):
        return "{} - {}".format(self.panel.title, self.variable)

class Dropdown(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    panel = models.ForeignKey(Panel, related_name='dropdowns')
    def __str__(self):
        return self.name

class ColumnFilter(models.Model):
    title = models.CharField(max_length=200)
    analysis = models.ForeignKey(Analysis, related_name='column_filters')
    type = models.CharField(max_length=50)
    field_choices = models.TextField()
    current_selection = models.TextField()
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('shop:run_detail', args=[self.name])

class HospitalStay(models.Model):
    BEN_ID=models.CharField(max_length=200)
    CLM_ID=models.CharField(max_length=200)
    SEGMENT=models.CharField(max_length=200)
    CLM_FROM_DT=models.CharField(max_length=200)
    CLM_THRU_DT=models.CharField(max_length=200)
    PRVDR_NUM=models.CharField(max_length=200)
    CLM_PMT_AMT=models.CharField(max_length=200)
    NCH_PRMRY_PYR_CLM_PD_AMT=models.CharField(max_length=200)
    AT_PHYSN_NPI=models.CharField(max_length=200)
    OP_PHYSN_NPI=models.CharField(max_length=200)
    OT_PHYSN_NPI=models.CharField(max_length=200)
    CLM_ADMSN_DT=models.CharField(max_length=200)
    ADMTNG_ICD9_DGNS_CD=models.CharField(max_length=200)
    CLM_PASS_THRU_PER_DIEM_AMT=models.CharField(max_length=200)
    NCH_BENE_IP_DDCTBL_AMT=models.CharField(max_length=200)
    NCH_BENE_PTA_COINSRNC_LBLTY_AM=models.CharField(max_length=200)
    NCH_BENE_BLOOD_DDCTBL_LBLTY_AM=models.CharField(max_length=200)
    CLM_UTLZTN_DAY_CNT=models.CharField(max_length=200)
    NCH_BENE_DSCHRG_DT=models.CharField(max_length=200)
    CLM_DRG_CD=models.CharField(max_length=200)
    def __str__(self):
        return "BEN: {}, CLM_FROM_DT: {}".format(self.BEN_ID, self.CLM_FROM_DT)


