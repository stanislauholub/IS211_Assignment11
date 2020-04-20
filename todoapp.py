#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = 'secret'

global mylist, task, email, priority, add_list

mylist = []
mylist_index = 0


# STORING DATA WITH PICKLE

import pickle
try:
    pickle.load(open('listfile.txt', 'rb'))
    mylist = pickle.load(open('listfile.txt', 'rb'))
except FileNotFoundError:
    mylist = []

    
# PART II FIRST CONTROLLER: VIEW LIST OF TO DO ITEMS
    
@app.route('/', methods = ['POST', 'GET'])
def index():
    global mylist_index
    if request.method == 'GET':
        try:
            lnth = len(mylist)
            mylist_index = mylist[lnth - 1][3] + 1
        except:
            mylist_index = 0
        return render_template('index.html', len = len(mylist), mylist = mylist)
    if request.method == 'POST':
        return redirect('/submit')

    
# PART IV SECOND CONTROLLER: SUBMITTING A NEW ITEM
    
@app.route('/submit', methods = ['POST','GET'])
def storeData():
    global mylist_index
    task = ""
    email = ""
    priority = ""
    #strIndex = ""
    add_list = []
    if request.method == 'POST':
        task = request.form['task']
        email = request.form['email']
        priority = request.form['priority']
        dt_ind = mylist_index
        if task != "" and email != "" and "@" in email and priority != "":
            add_list = [task, email, priority, dt_ind]
            mylist.append(add_list)
            mylist_index = mylist_index + 1
            flash('To Do item has been added successfully!')
            return render_template('index.html', len = len(mylist), mylist = mylist)
    return render_template('index.html', len = len(mylist), mylist = mylist)


# PART V THIRD CONTROLLER: CLEAR THE LIST

@app.route('/clear', methods = ['POST','GET'])
def clear():
    if request.method == 'POST':
        mylist.clear()
    flash('To Do list has been cleared successfully!')
    return redirect('/')


# EXTRA CREDIT I: SAVE THE LIST

@app.route('/save', methods = ['POST','GET'])
def save():
    if request.method == 'POST':
        import pickle
        with open('listfile.txt', 'wb') as filehandle:
            pickle.dump(mylist, filehandle)
    flash('To Do list has been saved successfully!')
    return render_template('index.html', len = len(mylist), mylist = mylist)


# EXTRA CREDIT II: DELETE INDIVIDUAL ITEMS

@app.route('/delete', methods = ['POST','GET'])
def delete():
    if request.method == 'POST':
        index = request.form['id_delete']
        id1 = int(index)
        del_list = []
        lst = []
        flag = False
        for i in range(0, len(mylist)):
            lst = mylist[i]
            if mylist[i][3] == id1:
                flag = True
                break
        if flag:
            mylist.remove(lst)
    flash('To Do item has been deleted successfully!')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True) 

