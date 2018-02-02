from flask import Flask, render_template, request
import pandas as pd


app=Flask(__name__)

@app.route('/hello/',methods=['GET','POST'])
def gps_can_data():
		if request.method=='GET':
			no_file = 'Enter a file name'
			return render_template('gps_can.html',no_file=no_file)
		if request.method=='POST':

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
			most_can = df.ts.value_counts().head(1)

			#The first ts that contains least CAN messages
			least_can = df.ts.value_counts(ascending=True).head(1)


			data = {'gps':gps_msgs, 'can':can_msgs, 'can_unq':un_can_msgs, 'run':runtime, 'avg_can':avg_can,
			'most_can':most_can, 'least_can':least_can}
	
			return render_template('gps_can.html',**data)


if __name__ =='__main__':
	app.run(debug=True)