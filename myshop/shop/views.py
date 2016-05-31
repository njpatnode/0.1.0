from django.shortcuts import render, get_object_or_404
from .models import Category, Product, DataSet, DataView, Run
from django.contrib.auth.decorators import login_required
import numpy as np
from sklearn import datasets, linear_model
import pandas as pd
from .forms import DataViewForm, RunForm
from django.contrib import messages
from django.http import HttpResponse
import json
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import mpld3
import seaborn as sns

@login_required
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    datasets = None
    datasets = DataSet.objects.all()
    dataviews = DataView.objects.all()
    runs = Run.objects.all()
    return render(request, 'shop/product/list.html', {'datasets': datasets, 'dataviews': dataviews, 'runs': runs})

@login_required
def product_add(request, category_slug=None):
    if request.method == 'POST':
        form = DataViewForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_dataview = DataView()
            new_dataview.dataset = cd['dataset']
            new_dataview.name = cd['name']
            new_dataview.parameters = cd['parameters']
            new_dataview.row_range_low = cd['row_range_low']
            new_dataview.row_range_high = cd['row_range_high']
            new_dataview.save()
            messages.success(request, 'Data View Successfully Added')
            form = DataViewForm()
    else:
        form = DataViewForm()
    datasets = None
    datasets = DataSet.objects.all()
    return render(request, 'shop/product/add.html', {'datasets': datasets, 'form': form})

@login_required
def dataview_detail(request, name):
    dataview = get_object_or_404(DataView, name=name)
    datacode = dataview.dataset.code
    exec "ds = " + datacode
    inputs, outputs, ds = get_df(ds)
    #assumes format in load datasets from scikit learn
    column_filter = dataview.parameters
    row_range_low = dataview.row_range_low
    row_range_high = dataview.row_range_high
    inputs, outputs, ds = get_tf_ds(ds, row_range_low, row_range_high, column_filter)
    dataviewhtml = ds.to_html()
    return render(request, 'shop/product/detail.html', {'dataview': dataview, 'datacode': datacode, 'dataviewhtml': dataviewhtml})

@login_required
def dataset_detail(request, name):
    dataset = get_object_or_404(DataSet, name=name)
    datacode = dataset.code
    exec "ds = " + datacode
    inputs, outputs, ds = get_df(ds)
    datahtml = ds.to_html()
    return render(request, 'shop/dataset/detail.html', {'dataset': dataset, 'datavalues': datahtml})

@login_required
def run_add(request):
    if request.method == 'POST':
        form = RunForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_run = Run()
            new_run.name = cd['name']
            new_run.train_dv = cd['train_dv']
            new_run.test_dv = cd['test_dv']
            new_run.formula = cd['formula']
            new_run.save()
            messages.success(request, 'Run Successfully Added')
            form = RunForm()
    else:
        form = RunForm()
    datasets = DataSet.objects.all()
    return render(request, 'shop/product/add_run.html', {'datasets': datasets, 'form': form})

@login_required
def run_detail(request, name):
    run, inputs, outputs, ds = get_ds(name, 100)
    coeff, fig_html = calculate_chart(inputs, outputs, ds, 1)
    return render(request, 'shop/product/run_detail.html', {'run': run, 'coeff': coeff, 'fig_html': fig_html})

def get_df(ds):
    #assumes format in load datasets from scikit learn
    inputs = pd.DataFrame(ds.data)
    outputs = pd.DataFrame(ds.target)
    ds = pd.concat([inputs, outputs], axis=1)
    inputs.columns = ['Age', 'Sex', 'Body Mass Index', 'Average Blood Pressure', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6']
    outputs.columns = ['Target']
    ds.columns = ['Age', 'Sex', 'Body Mass Index', 'Average Blood Pressure', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'Target']
    return (inputs, outputs, ds)

def get_tf_ds(inputs, outputs, ds, row_range_low, row_range_high, column_filter):
    if str(row_range_low)=='':
        row_range_low = 0
    if str(row_range_high)=='':
        row_range_high = 0
    #apply row filter to both inputs and outputs
    inputs = inputs[int(eval(str(row_range_low))):int(eval(str(row_range_high)))]
    outputs = outputs[int(eval(str(row_range_low))):int(eval(str(row_range_high)))]
    #apply column filter
    inputs = inputs[eval(str(column_filter))]
    return (inputs, outputs, ds)

def get_train_pct(request, name):
    response_data = {}
    if request.method == 'GET':
        train_pct = request.GET['train_pct']
        train_pct = str(int(train_pct))
        risk_threshold = float(request.GET['risk_threshold'])/100.
        response_data['train_pct'] = train_pct
        response_data['risk_threshold'] = str(int(risk_threshold*100))
        run, inputs, outputs, ds = get_ds(name, train_pct)
        coeff, response_data['fig_html'] = calculate_chart(inputs, outputs, ds, risk_threshold)
        return HttpResponse(json.dumps(response_data), content_type = "application/json")

def handle_heatmap(request, name):
    response_data = {}
    if request.method == 'GET':
        run, inputs, outputs, ds = get_ds(name, "100")
        response_data['heatmap_html'] = get_heatmap(ds)
        return HttpResponse(json.dumps(response_data), content_type = "application/json")

def calculate_chart(inputs, outputs, ds, risk_threshold):
    plt.close('all')
    regr = linear_model.LinearRegression()
    regr.fit(inputs, outputs)
    coeff = regr.coef_
    fig, ax = plt.subplots()
    risk_colors = get_colors(inputs, outputs, risk_threshold)
    ax.scatter(inputs, outputs, color=risk_colors)
    ax.set_title("Linear Risk Plot", fontsize=32)
    ax.set_xlabel("Age", fontsize=16)
    ax.set_ylabel("HbA1c Year 2", fontsize=16)
    ax.plot(inputs, regr.predict(inputs), color="blue", linewidth=3)
    fig_html = mpld3.fig_to_html(fig)
    return (coeff, fig_html)

def get_ds(name, train_pct):
    run = get_object_or_404(Run, name=name)
    train_dv = get_object_or_404(DataView, name=run.train_dv.name)
    datacode = train_dv.dataset.code
    exec "ds = " + datacode
    inputs, outputs, ds = get_df(ds)
    column_filter = train_dv.parameters
    row_range_low = train_dv.row_range_low
    row_range_high = train_dv.row_range_high
    #train_pct override
    if train_pct:
        row_range_low = 1
        row_range_high = train_pct
    inputs, outputs, ds = get_tf_ds(inputs, outputs, ds, row_range_low, row_range_high, column_filter)
    return (run, inputs, outputs, ds)

def get_colors(inputs, outputs, risk_threshold):
    risk_level = outputs.quantile(risk_threshold)
    risk_colors = []
    for y in outputs['Target']:
        if y > float(risk_level[0]):
            risk_colors.append('red')
        else:
            risk_colors.append('blue')
    return risk_colors

def get_heatmap(ds):
    plt.close('all')
    corrmat = ds.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corrmat, vmax=.8, square=True)
    heatmap_html = mpld3.fig_to_html(fig)
    return heatmap_html

