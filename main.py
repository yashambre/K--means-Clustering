import pypyodbc
from datetime import datetime
from flask import Flask,request, render_template
import time

	
#Statements


#Your statements here

 
app = Flask(__name__)

server = 'arsenal.database.windows.net'
database = 'yashdb'
username = 'arsenal'
password = 'August#2018'
driver= '{ODBC Driver 13 for SQL Server}'


def latlongMethod(x,y):
	cnxn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
	
	start=time.time()
	if cnxn:  
	  # we have a DB2 connection, so obtain system information via ENV_SYS_INFO:  
		
		cursor = cnxn.cursor()
		sql = "SELECT  "+x+","+y+" FROM [dbo].[quake] WHERE "+x+" IS NOT NULL AND "+y+"  IS NOT NULL"
		print (sql)
		chai=cursor.execute(sql)
		result = []
		row = cursor.fetchone()
		maxx = 0
		maxy = 0
		minx = row[0]
		miny = row[1]
		while row:
			row1=[i for i in row]
			maxx = max(maxx, row1[0])
			minx = min(minx, row1[0])
			maxy = max(maxy, row1[1])
			miny = min(miny, row1[1])

			result.append(row1)
			row=cursor.fetchone()
		total_time=time.time() - start
		print (result)	
		print (total_time)
		return result,[minx,maxx],[miny,maxy]
	return False	
		
		

@app.route('/')
def lol():
	return render_template('quake.html')


@app.route('/hi', methods=['GET', 'POST'])
def threbut():
	if request.form.get('Search') == 'Search':
			var= request.form.get('check')
			var1 = request.form.get('check1')
			var2 = request.form.get('check2')
			result1,x_range,y_range = latlongMethod(var,var1) 
			return render_template('quake.html', search = result1, cluster=var2, x_range=x_range,y_range=y_range)

if __name__ == '__main__':
  app.run()


