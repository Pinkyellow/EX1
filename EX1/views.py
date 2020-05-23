"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from EX1 import app
from EX1 import models as dbHandler
from flask import request, redirect, url_for, session, jsonify
from io import TextIOWrapper
import csv

import pandas
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_connection(r"diona.db")

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('welcome.html',
                            title='Home Page',
                            year=datetime.now().year,)

@app.route('/login')
def login():
     """Renders the login page."""
     return render_template('login.html',
                             title='Login',
                             year=datetime.now().year,
                             message='Login Page',
                             msg='')


@app.route('/login_success')
def login_success():

     if 'loggedin' in session:
         #"""Renders the login page."""
         return render_template('admin_login.html',
                                 username=session['id'],
                                 title='Login',
                                 year=datetime.now().year,
                                 message='Main page')
     return render_template('login.html')



@app.route('/login_request', methods=['POST', 'GET'])
def login_request():
    # error = None
     if request.method == 'POST':
        id = request.form['username']
        password = request.form['password']
        account = dbHandler.retrieveAccount(id, password)
        # If the account exists in Admin table in the database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account
            #session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('login_success'))
            #return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password! Please try again!'
        
        # Show the login form with message (if any)
        return render_template('login.html',
                                title='Login',
                                year=datetime.now().year,
                                message='Login Page',
                                error=True,
                                msg=msg)
     else:
         return render_template('login.html',
                                title='Login',
                                year=datetime.now().year,
                                message='Login Page',
                                error=True,
                                msg='')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('loggedin', None)
    session.pop('id', None)
    return redirect(url_for('home'))



@app.route('/adminview')
def adminview():  
    # Check if user is loggedin
    if 'loggedin' in session:
        
        types = dbHandler.getAssetType()
   
        return render_template('adminview.html', 
                                username=session['id'],   
                                title='Admin View',
                                type = types,
                                year=datetime.now().year)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

    
@app.route('/adminview/mobile')
def admin_mobile():
    # Check if user is loggedin
    if 'loggedin' in session:
        
        types = dbHandler.getAssetType()

        conn = sqlite3.connect(r"diona.db")
        # Get name and type of an asset, and get key_value store as results
        cur = conn.cursor() 
        name_types = cur.execute("SELECT a.asset_name , t.assetType_name, GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Mobile Phone' GROUP BY a.asset_id")
        rows = name_types.fetchall()
        results = [0 for x in range(len(rows))]
        for x in range(len(rows)):
            results[x] = rows[x][2].split(',')      

        # Get key_name rows
        cur2 = conn.cursor() 
        details_keys = cur2.execute("SELECT a.asset_name, GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Mobile Phone' GROUP BY a.asset_id")


        return render_template('admin_mobile.html', 
                                username=session['id'],   
                                title='Admin View',
                                rows = rows,
                                res = results,
                                keys = details_keys.fetchall()[0][1].split(','),
                                type = types,
                                year=datetime.now().year)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route('/adminview/tablet')
def admin_tablet():
    if 'loggedin' in session:
        
        types = dbHandler.getAssetType()

        conn = sqlite3.connect(r"diona.db")
        # Get name and type of an asset, and get key_value store as results
        cur = conn.cursor() 
        name_types = cur.execute("SELECT a.asset_name , t.assetType_name, GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Tablet' GROUP BY a.asset_id")
        rows = name_types.fetchall()
        results = [0 for x in range(len(rows))]
        for x in range(len(rows)):
            results[x] = rows[x][2].split(',')      

        # Get key_name rows
        cur2 = conn.cursor() 
        details_keys = cur2.execute("SELECT a.asset_name, GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Tablet' GROUP BY a.asset_id")
   
       # """Renders the user page."""
        return render_template('admin_tablet.html',
                                username=session['id'],
                                title='Admin View',
                                rows = rows,
                                res = results,
                                keys = details_keys.fetchall()[0][1].split(','),
                                type = types,
                                year=datetime.now().year)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))  

@app.route('/adminview/laptop')
def admin_laptop():
    if 'loggedin' in session:
        
        types = dbHandler.getAssetType()

        conn = sqlite3.connect(r"diona.db")
        # Get name and type of an asset, and get key_value store as results
        cur = conn.cursor() 
        name_types = cur.execute("SELECT a.asset_name , t.assetType_name, GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Laptop' GROUP BY a.asset_id")
        rows = name_types.fetchall()
        results = [0 for x in range(len(rows))]
        for x in range(len(rows)):
            results[x] = rows[x][2].split(',')      

        # Get key_name rows
        cur2 = conn.cursor() 
        details_keys = cur2.execute("SELECT a.asset_name, GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Laptop' GROUP BY a.asset_id")
      
    # """Renders the user page."""
        return render_template('admin_laptop.html',
                                title='Admin View',
                                username=session['id'],
                                rows = rows,
                                res = results,
                                keys = details_keys.fetchall()[0][1].split(','),
                                type = types,
                                year=datetime.now().year)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    
  

@app.route('/userview')
def userview():

    types = dbHandler.getAssetType() 
   
    # """Renders the user page."""
    return render_template('userview.html',
                            title='User View',
                            type = types,
                            year=datetime.now().year)

@app.route('/userview/mobile')
def mobile():
        types = dbHandler.getAssetType()

        conn = sqlite3.connect(r"diona.db")
        # Get name and type of an asset, and get key_value store as results
        cur = conn.cursor() 
        name_types = cur.execute("SELECT a.asset_name , t.assetType_name, GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Mobile Phone' GROUP BY a.asset_id")
        rows = name_types.fetchall()
        results = [0 for x in range(len(rows))]
        for x in range(len(rows)):
            results[x] = rows[x][2].split(',')      

        # Get key_name rows
        cur2 = conn.cursor() 
        details_keys = cur2.execute("SELECT a.asset_name, GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Mobile Phone' GROUP BY a.asset_id")

        
        return render_template('userview_mobile.html', 
                                title='User View',
                                rows = rows,
                                res = results,
                                keys = details_keys.fetchall()[0][1].split(','),
                                type = types,
                                year=datetime.now().year)


@app.route('/userview/tablet')
def tablet():
        types = dbHandler.getAssetType()

        conn = sqlite3.connect(r"diona.db")
        # Get name and type of an asset, and get key_value store as results
        cur = conn.cursor() 
        name_types = cur.execute("SELECT a.asset_name , t.assetType_name, GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Tablet' GROUP BY a.asset_id")
        rows = name_types.fetchall()
        results = [0 for x in range(len(rows))]
        for x in range(len(rows)):
            results[x] = rows[x][2].split(',')      

        # Get key_name rows
        cur2 = conn.cursor() 
        details_keys = cur2.execute("SELECT a.asset_name, GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Tablet' GROUP BY a.asset_id")
       
    # """Renders the user page."""
        return render_template('userview_tablet.html',
                                title='User View',
                                rows = rows,
                                res = results,
                                keys = details_keys.fetchall()[0][1].split(','),
                                type = types,
                                year=datetime.now().year)

@app.route('/userview/laptop')
def laptop():
        types = dbHandler.getAssetType()

        conn = sqlite3.connect(r"diona.db")
        # Get name and type of an asset, and get key_value store as results
        cur = conn.cursor() 
        name_types = cur.execute("SELECT a.asset_name , t.assetType_name, GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Laptop' GROUP BY a.asset_id")
        rows = name_types.fetchall()
        results = [0 for x in range(len(rows))]
        for x in range(len(rows)):
            results[x] = rows[x][2].split(',')      

        # Get key_name rows
        cur2 = conn.cursor() 
        details_keys = cur2.execute("SELECT a.asset_name, GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Laptop' GROUP BY a.asset_id")
    # """Renders the user page."""
        return render_template('userview_laptop.html',
                                title='User View',
                                rows = rows,
                                res = results,
                                keys = details_keys.fetchall()[0][1].split(','),
                                type = types,
                                year=datetime.now().year)



@app.route('/import')
def import_main():
        templates = ["mobile.csv","laptop.csv","tablet.csv"]
        msg = ''

        return render_template('i_or_o_main.html', 
                                username=session['id'],   
                                title='Import/Export',  
                                files = templates,
                                msg = msg,
                                year=datetime.now().year)
  

@app.route('/import_request', methods=['POST', 'GET'])
def import_request():

     if request.method == 'POST':
       
        new_asset = ''
        asset_id = ''
       
        file = request.files['upload_file']

        csvf = TextIOWrapper(file, encoding='utf-8')
        csv_reader = csv.reader(csvf, delimiter=',')
        headers = next(csv_reader, None)
 
        for row in csv_reader:
            name = row[0]
            type = row[1]
            assetType_id = dbHandler.retrieveAssetTypeID(type)
            
            if assetType_id:
                new_asset = (assetType_id[0],name)
            if new_asset:
                asset_id = dbHandler.create_newAsset(new_asset)

            if asset_id:
                data = row[2:]
                keys = headers[2:]
                new_dict = dict(zip(keys,data))
                print(new_dict)

                for key, value in new_dict.items():
                    new_assetDetails = (asset_id, key, value, datetime.today(), datetime.today())    
                    dbHandler.create_newAssetDetails(new_assetDetails)

                msg = 'Successfully insert...'
            else:
                # Table doesnt exist.
                msg = 'Error inserting into database.'

        return render_template('i_or_o_confirm.html',
                               username=session['id'],
                               msg = msg,
                               year=datetime.now().year)
       


@app.route('/new_assets')
def new_assets():
    """Renders the New Assets page."""
    menu = dbHandler.getAssetType()
   
    return render_template('new_assets.html',
        title='New Assets',
        year=datetime.now().year,
        message='New assets',
        menu = menu)


@app.route('/add_asset', methods=['POST', 'GET'])
def add_asset():
    #if the form is submittied, declare the variable of new_asset, asset_id and
    #user_id
    if request.method == 'POST':
        new_asset = ''
        asset_id = ''
        user_id = ''
        print('hello')
        #get the asset type from the form to get assetTypeID
        if request.form['assetType']:
            assetType_id = dbHandler.retrieveAssetTypeID(request.form['assetType'])
        else:
            msg = 'Enter all details'
        
        #prepare new asset from form data, to get the asset record (name and
        #type) first
        if request.form['assetName']:
            if assetType_id:
                new_asset = (assetType_id[0], request.form['assetName'])
            else:
                #add to assess type and continue creating asset
                print(request.form['assetType'])
                assetType_id = dbHandler.create_newAssetType(request.form['assetType'])
                new_asset = (assetType_id, request.form['assetName'])
        else:
            msg = 'Enter all details'        
        
        #create new asset and get asset id
        if new_asset:
            asset_id = dbHandler.create_newAsset(new_asset)
        else:
            msg = 'Error! Cannot create new asset.'
        
        #get the email from the form to get userID
        user_id = dbHandler.retrieveUserID(request.form['assetAssigned'])
        
        #Continue adding into Asset Details if asset is added in Asset table
        if asset_id:
            #convert form data into dictionary
            data = request.form.to_dict()
            #remove type and name before adding to asset details table
            data.pop('assetType', None)
            data.pop('assetName', None)
            data.pop('assetAssigned', None)
            
            
            #add all details in data dictionary to asset details table
            for key, value in data.items():
                new_assetDetails = (asset_id, key, value, datetime.today(), datetime.today())    
                dbHandler.create_newAssetDetails(new_assetDetails)
             #   new_list.append(value)
            
            #convert list to dictionary before inserting into database
            #AssetDetails = tuple()
            
            if asset_id:
                if user_id:
                    rent = (user_id[0],asset_id,datetime.today())
                    dbHandler.create_newRentrecord(rent)
                    msg = "Inserted data successfully"
                else:
                    msg = 'Error! Cannot create new asset'
            else:
                msg = 'Error! Cannot create new asset'
        else:
            # Table doesnt exist.
            msg = 'Error inserting into database.'
        pageName = page_name(request.form['assetType'])

        menu = dbHandler.getAssetType()

        # Show the form with message (if any)
        return render_template('confirmation.html',
                title='Confirmation Message',
                year=datetime.now().year,
                msg=msg)
    else:
        return render_template('new_assets.html',
            title='New Assets',
            year=datetime.now().year,
            message='New Assets',
            menu = menu,
            error=True,
            msg='')


def page_name(x):
            return {
                'Mobile Phone': 'new_assetsMobile.html',
                'Tablet': 'new_assetsTablet.html',
                'Laptop': 'new_assetsLaptop.html'
            }.get(x, 'admin_login.html')

@app.route('/NewAsset_Default.html')
def new_assetDefault():
    """Renders the New Assets Default page."""
    #to make all the asset types appear on the page
    menu = dbHandler.getAssetType()
    return render_template('new_assetsDefault.html',
        title='New Assets for Mobile',
        year=datetime.now().year,
        message='New assets Mobile',
        menu = menu)


@app.route('/NewAsset_Mobile.html')
def new_assetsMobile():
    """Renders the New Assets Mobile page."""
    menu = dbHandler.getAssetType()
    return render_template('new_assetsMobile.html',
        title='New Assets for Mobile',
        year=datetime.now().year,
        message='New assets Mobile',
        menu = menu)

@app.route('/NewAsset_Tablet.html')
def new_assetsTablet():
    """Renders the New Assets Tablet page."""
    menu = dbHandler.getAssetType()
    return render_template('new_assetsTablet.html',
        title='New Assets for Tablet',
        year=datetime.now().year,
        message='New assets Tablet',
        menu = menu)

@app.route('/NewAsset_Laptop.html')
def new_assetsLaptop():
    """Renders the New Assets Laptop page."""
    menu = dbHandler.getAssetType()
    return render_template('new_assetsLaptop.html',
        title='New Assets for Laptop',
        year=datetime.now().year,
        message='New assets Laptop',
        menu = menu)


@app.route('/history')
def view_history():
    if 'loggedin' in session:
       
        conn = sqlite3.connect(r"diona.db")

        conn.row_factory = sqlite3.Row
            # Get name and type of an asset, and get key_value store as results
        rows = conn.execute("SELECT u.user_name, a.asset_Name, r.date_rental, r.date_return FROM Rent r, Asset a INNER JOIN User u on u.user_id = r.user_id AND a.asset_id = r.asset_id ")
        col_names = rows.fetchone()
        headers = col_names.keys()

        cur2 = conn.cursor() 
        results = cur2.execute("SELECT u.user_name, a.asset_Name, r.date_rental, r.date_return FROM Rent r, Asset a INNER JOIN User u on u.user_id = r.user_id AND a.asset_id = r.asset_id ")


    return render_template('view_history.html',
                            username=session['id'],
                            title = 'User History',
                            header = headers,
                            list = results.fetchall(),
                            year = datetime.now().year,)


@app.route('/asset_type')
def asset_type():
    """Renders the Asset Type page."""
    return render_template('new_asset_type.html',
        title='Asset Type',
        year=datetime.now().year,
        message='Asset type')

@app.route('/site_details')
def site_details():
    """Renders the Site Details page."""
    return render_template('site_details.html',
        title='Site Details',
        year=datetime.now().year,
        message='Site Details')

@app.route('/submit_site_details', methods=['POST', 'GET'])
def submit_site_details():
    #if the form is submittied, declare the variable of new_siteDetails and
    #site_id
    if request.method == 'POST':
        new_siteDetails = (request.form['siteLocation'],request.form['siteAddress'],request.form['siteDevice'],request.form['siteDeviceName'],request.form['siteDeviceSerial'],request.form['siteIpAddress'],request.form['siteMobileNo'],request.form['siteMobileSim'],request.form['siteComputer'],request.form['sitePcUsername'],request.form['sitePcPassword'],request.form['sitePrinter'],request.form['siteProjectMgr'])
        site_id = dbHandler.create_newSite(new_siteDetails)

        if site_id:
            # Show the form with message (if any)
            msg = 'Site details are saved successfully'
        else:
            msg = 'Error'

        return render_template('site_details.html',
                title='Site Details',
                year=datetime.now().year,
                message='Site Details',
                msg=msg)



@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html',
                            title='Contact',
                            year=datetime.now().year,
                            message='hello.')

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
                            title='About',
                            year=datetime.now().year,
                            message='Your application description page.')


