__author__ = 'KEO_Sidara'
__Version__ = '2.0'

import subprocess

try:
    __import__("xmltodict")
except ImportError:    
    subprocess.check_call(['pip', 'install', 'xmltodict'])     
import json ,datetime,sys,xmltodict,datetime

class RobotReport:

 def calculateTestTime(self,starttime,endtime):

    starttime = starttime.split(" ", 1)
    starttime = starttime[1]

    starttime = starttime.split(".", 1)
    starttime = starttime[0]

    endtime = endtime.split(" ", 1)
    endtime = endtime[1]

    endtime = endtime.split(".", 1)
    endtime = endtime[0]

    totalTime = datetime.datetime.strptime(endtime,"%H:%M:%S") - datetime.datetime.strptime(starttime,"%H:%M:%S")
    totalTime = round(totalTime.total_seconds())
    return totalTime
    
 
 def  generateReport(self):
    try:
        with open('output1.xml') as fd:
            doc = xmltodict.parse(fd.read())
            test =json.dumps(doc)
            suit =json.loads(test)
            test =json.loads(test)

        passTest = test["robot"]["statistics"]["total"]["stat"][1]["@pass"]
        failTest = test["robot"]["statistics"]["total"]["stat"][0]["@fail"]

        d_date = datetime.datetime.now()
        reg_format_date = d_date.strftime("%Y_%m_%d_%I_%M")
    except Exception as e:
       print (e)
       sys.exit(0)
        
    message = """
   <html>
   <head>
      <!-- UIkit CSS -->
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/css/uikit.min.css" />
      <link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/dataTables.uikit.min.css" />
      <!-- UIkit JS -->
      <script src="https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/js/uikit.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/js/uikit-icons.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/chart.js@2.8.0"></script>
      <script src="https://code.jquery.com/jquery-3.3.1.js"></script>
      <script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
      <script src=" https://cdn.datatables.net/1.10.20/js/dataTables.uikit.min.js"></script>
      <!-- import CSS -->
      <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
      <!-- import JavaScript -->
      <script src="https://unpkg.com/element-ui/lib/index.js"></script>
      <style>
         .red{{
         background:red
         }}
         .green{{
         background:green
         }}
      </style>
   </head>
   <body>
      <nav class="uk-navbar-container" uk-navbar>
         <div class="uk-navbar-left">
            <a class="uk-navbar-item uk-logo"> LOGO </a>
            <ul class="uk-navbar-nav">
               <li class="uk-active"><a href="#">HOME</a></li>
            </ul>
         </div>
      </nav>
      <div class="uk-container uk-container-xlarge uk-card uk-card-default uk-card-body">
         <div class="uk-text-center" uk-grid>
            <div class="uk-width-1-2">
               <div class="uk-card uk-card-default uk-card-body">
                  <canvas id="myChart"></canvas>
               </div>
            </div>
            <div class="uk-width-1-2">
               <div class="uk-card uk-card-default uk-card-body">
                  <canvas id="myLine"></canvas>
               </div>
            </div>
         </div>
         <h1>Robot Report</h1>
         <div class="uk-flex">
         </div>
         </br>
         <table id="dbt" class="uk-table uk-table-hover uk-table-divider">
            <thead>
               <tr>
                  <th>Suite Name</th>
                  <th>  Test Case</th>
                  <th>Message</th>
                  <th>Status</th>
                  <th > Duration </th>
               </tr>
            </thead>
            <tbody>
               {0}
            </tbody>
         </table>
         <canvas id="myChart"></canvas>
      </div>
      <center> Github Repo <a href="https://github.com/sidarakeo/robotframework-pie-report">github</a> </center>
      </div>
   </body>
</html>"""
    suitename = suit["robot"]["suite"]["@name"]
    caseNameDynamic = []
    totalDuration = []
    insert = []

    try:
        for i in range (len(test["robot"]["suite"]["suite"])):     
            j= test["robot"]["suite"]["suite"][i]["test"]       
            for k in range (len(j)):
                caseName= j[k]["@name"]
                caseName = caseName.split("'")
                caseName= caseName[0]
                #print (caseName)
                statusTest= j[k]["status"]["@status"]
                s= test["robot"]["suite"]["suite"][i]["@name"] 

                testDuration= self.calculateTestTime(j[k]["status"]["@starttime"],j[k]["status"]["@endtime"])
                
                totalDuration.append(testDuration)
                caseNameDynamic.append(caseName)
                if statusTest=="FAIL":
                    badge= "danger"
                    msgErr= "<p class='uk-alert-danger'>"+j[k]["status"]["#text"]+"</p>"
                else:
                    badge= "success"
                    msgErr= ""

                insert.append("<tr> <td>{3}</td><td>{0} </td> <td > {5} </td> <td><span class='el-tag el-tag--{2} el-tag--dark'>{1}</span> </td>  <td> {4} </td>  </tr>".format(caseName,statusTest,badge,s,testDuration,msgErr))
        

        caseNameDynamic=','.join("'{0}'".format(x) for x in caseNameDynamic)
        totalDuration=','.join("'{0}'".format(x) for x in  totalDuration)

       # print (caseNameDynamic)
        #print(totalDuration)
        script = "var ctx = document.getElementById('myChart').getContext('2d');var myChart = new Chart(ctx, {{type: 'pie',data: {{labels: ['Pass', 'Fail'],datasets: [{{backgroundColor: ['#2ecc71','#e74c3c' ],data: [{0}, {1}]}}]}}}});$(document).ready(function() {{ $('#dbt').DataTable(); }} );var canvas = document.getElementById('myLine'); var data = {{ labels: [ {2} ], datasets: [ {{ label: 'Performance Test', fill: false, lineTension: 0.1, backgroundColor: 'rgba(75,192,192,0.4)', borderColor: 'rgba(75,192,192,1)', borderCapStyle: 'butt', borderDash: [], borderDashOffset: 0.0, borderJoinStyle: 'miter', pointBorderColor: 'rgba(75,192,192,1)', pointBackgroundColor: '#fff', pointBorderWidth: 1, pointHoverRadius: 5, pointHoverBackgroundColor: 'rgba(75,192,192,1)', pointHoverBorderColor: 'rgba(220,220,220,1)', pointHoverBorderWidth: 2, pointRadius: 5, pointHitRadius: 10, data: [{3}], }} ] }}; function adddata(){{ myLineChart.data.datasets[0].data[7] = 60; myLineChart.data.labels[7] = 'Newly Added'; myLineChart.update(); }} var option =  {{ showLines: true,  scales: {{ xAxes: [{{ ticks: {{ display: false }} }}] }} }}; var myLineChart = Chart.Line(canvas,{{ data:data, options:option }}); ".format(passTest,failTest,caseNameDynamic,totalDuration)
         


        insert.append("<script>{}</script>".format(script))
        Html_file= open("pie_report_{}.html".format(reg_format_date),"w")
        Html_file.write(message.format(''.join(insert)))
        Html_file.close()
        print ("Success Generate Report")
    except:	
        
        for i in test["robot"]["suite"]["test"]:   

            statusTest= i["status"]["@status"]
           
            testDuration= self.calculateTestTime(i["status"]["@starttime"],i["status"]["@endtime"])
            totalDuration.append(testDuration)
            if statusTest=="FAIL":
                    badge= "danger"
                    msgErr= "<p class='uk-alert-danger'>"+i["status"]["#text"]+"</p>"
            else:
                    badge= "success" 
                    msgErr=""
            caseNameDynamic.append(i["@name"])
            insert.append("<tr> <td>{3}</td><td>{0} </td> <td > {5} </td> <td><span class='el-tag el-tag--{2} el-tag--dark'>{1}</span> </td>  <td> {4} </td>  </tr>".format(i["@name"], i["status"]["@status"],badge,suitename,testDuration,msgErr))
        
        caseNameDynamic=','.join("'{0}'".format(x) for x in caseNameDynamic)
        totalDuration=','.join("'{0}'".format(x) for x in  totalDuration)
        script = "var ctx = document.getElementById('myChart').getContext('2d');var myChart = new Chart(ctx, {{type: 'pie',data: {{labels: ['Pass', 'Fail'],datasets: [{{backgroundColor: ['#2ecc71','#e74c3c' ],data: [{0}, {1}]}}]}}}});$(document).ready(function() {{ $('#dbt').DataTable(); }} );var canvas = document.getElementById('myLine'); var data = {{ labels: [ {2} ], datasets: [ {{ label: 'Performance Test', fill: false, lineTension: 0.1, backgroundColor: 'rgba(75,192,192,0.4)', borderColor: 'rgba(75,192,192,1)', borderCapStyle: 'butt', borderDash: [], borderDashOffset: 0.0, borderJoinStyle: 'miter', pointBorderColor: 'rgba(75,192,192,1)', pointBackgroundColor: '#fff', pointBorderWidth: 1, pointHoverRadius: 5, pointHoverBackgroundColor: 'rgba(75,192,192,1)', pointHoverBorderColor: 'rgba(220,220,220,1)', pointHoverBorderWidth: 2, pointRadius: 5, pointHitRadius: 10, data: [{3}], }} ] }}; function adddata(){{ myLineChart.data.datasets[0].data[7] = 60; myLineChart.data.labels[7] = 'Newly Added'; myLineChart.update(); }} var option =  {{ showLines: true,  scales: {{ xAxes: [{{ ticks: {{ display: false }} }}] }} }}; var myLineChart = Chart.Line(canvas,{{ data:data, options:option }}); ".format(passTest,failTest,caseNameDynamic,totalDuration)

       # print (caseNameDynamic)
        insert.append("<script>{}</script>".format(script))
        Html_file= open("pie_report_{}.html".format(reg_format_date),"w")
        Html_file.write(message.format(''.join(insert)))
        Html_file.close()
        print ("Success Generate Report")

load = RobotReport()
load.generateReport()
