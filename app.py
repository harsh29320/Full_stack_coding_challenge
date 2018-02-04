#This file inludes Flask and python codes to query the dataframe and return reults to the html file
#in the templates folder "gps_can.html"

from flask import Flask, render_template, request
import pandas as pd


app=Flask(__name__)

@app.route('/app/',methods=['GET','POST'])
def gps_can_data():
		if request.method=='GET':
			return render_template('gps_can.html')
		if request.method=='POST':
			try:
				#getting the name of file from the html form		
				csv_file = request.form['Name']
			
				#setting a dataframe 				
				df = pd.read_csv(csv_file)

				#Number of gps messages
				gps_msgs = df.gps_id.count()
			
				#Number of CAN messages			
				can_msgs = df.message_id.count()

				#Number of unique CAN messages
				un_can_msgs = len(df.message_id.unique())

				#Converting time datatype from object to datetime
				df['ts']= pd.to_datetime(df.ts)

				#Total runtime
				runtime = df['ts'].iloc[-1] - df['ts'].iloc[1]

				#Average CAN messages
				avg_can = can_msgs/runtime.seconds/gps_msgs

				#The first ts that contains most CAN messages
				most_can = df.groupby('ts').count().sort_values('message_id',ascending=False).index[0]

				#The first ts that contains least CAN messages
				least_can = df.groupby('ts').count().sort_values('message_id').index[0]


				data = {'gps':gps_msgs, 'can':can_msgs, 'can_unq':un_can_msgs, 'run':runtime, 'avg_can':avg_can,
				'most_can':most_can, 'least_can':least_can}
	
				return render_template('gps_can.html',**data)
			
			except:
				#return this if the file is not found
				no_file = 'Enter different file name'
				return render_template('gps_can.html',no_file=no_file)
if __name__ =='__main__':
	app.run()