from django.shortcuts import render, get_object_or_404
from .models import Category, Product, DataSet, DataView, Run
from django.contrib.auth.decorators import login_required
import numpy as np
from sklearn import datasets, linear_model
import pandas as pd
from .forms import DataViewForm, RunForm
from django.contrib import messages

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
            new_dataview.row_range = cd['row_range']
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
    exec "datavalues = " + datacode
    #assumes format in load datasets from scikit learn
    inputs = pd.DataFrame(datavalues.data)
    outputs = pd.DataFrame(datavalues.target)
    datavalues = pd.concat([inputs, outputs], axis=1)
    datavalues.columns = ['Age', 'Sex', 'Body Mass Index', 'Average Blood Pressure', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'Target']
    column_filter = dataview.parameters
    row_range_low = dataview.row_range_low
    row_range_high = dataview.row_range_high
    datavalues = datavalues[eval(column_filter)]
    dataviewhtml = datavalues.to_html()
    return render(request, 'shop/product/detail.html', {'dataview': dataview, 'datacode': datacode, 'dataviewhtml': dataviewhtml})

@login_required
def dataset_detail(request, name):
    dataset = get_object_or_404(DataSet, name=name)
    datacode = dataset.code
    exec "datavalues = " + datacode
    #assumes format in load datasets from scikit learn
    inputs = pd.DataFrame(datavalues.data)
    outputs = pd.DataFrame(datavalues.target)
    datavalues = pd.concat([inputs, outputs], axis=1)
    datavalues.columns = ['Age', 'Sex', 'Body Mass Index', 'Average Blood Pressure', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'Target']
    datahtml = datavalues.to_html()
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
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    import mpld3
    run = get_object_or_404(Run, name=name)
    train_dv = get_object_or_404(DataView, name=run.train_dv.name)
    datacode = train_dv.dataset.code
    exec "datavalues = " + datacode
    #assumes format in load datasets from scikit learn
    inputs = pd.DataFrame(datavalues.data)
    train_outputs = pd.DataFrame(datavalues.target)
    datavalues = pd.concat([inputs, train_outputs], axis=1)
    datavalues.columns = ['Age', 'Sex', 'Body Mass Index', 'Average Blood Pressure', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'Target']
    column_filter = train_dv.parameters
    row_range = train_dv.row_range
    train_datavalues = datavalues[eval(column_filter)]
    regr = linear_model.LinearRegression()
    regr.fit(train_datavalues, train_outputs)
    coeff = regr.coef_
    fig, ax = plt.subplots()
    ax.scatter(train_datavalues, train_outputs)
    ax.plot(train_datavalues, regr.predict(train_datavalues), color='blue', linewidth=3)
    fig_html = mpld3.fig_to_html(fig)
    #test_dv = get_object_or_404(DataView, name=name)
    #exec "datavalues = " + datacode
    #assumes format in load datasets from scikit learn
    #inputs = pd.DataFrame(datavalues.data)
    #outputs = pd.DataFrame(datavalues.target)
    #datavalues = pd.concat([inputs, outputs], axis=1)
    #datavalues.columns = ['Age', 'Sex', 'Body Mass Index', 'Average Blood Pressure', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'Target']
    #column_filter = dataview.parameters
    #row_range = dataview.row_range
    #datavalues = datavalues[eval(column_filter)]
    #dataviewhtml = datavalues.to_html()
    return render(request, 'shop/product/run_detail.html', {'run': run, 'coeff': coeff, 'fig_html': fig_html})

def get_df(dataset):
