__author__ = 'KEO_Sidara'
__Version__ = '1.0'
import subprocess
try:
    __import__("xmltodict")
except ImportError:    
    subprocess.check_call(['pip', 'install', 'xmltodict'])     
import json ,datetime,sys,xmltodict

class RobotReport:
 
 def  generateReport(self):
    try:
        with open('output.xml') as fd:
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
            <a class="uk-navbar-item uk-logo">LOGO</a>
            <ul class="uk-navbar-nav">
                <li class="uk-active"><a href="#">HOME</a></li>
                
            </ul>

        </div>
    </nav>
                <div class="uk-container uk-container-xsmall">
                <h1>Robot Report</h1>
                <canvas id="myChart"></canvas>
                <table id="dbt" class="uk-table uk-table-hover uk-table-divider">
                <thead>
                <tr>
                <th>Suite Name</th>
                <th>  Test Case</th>
                <th>Status</th>

                </tr>
                </thead>
                <tbody>
                {0}
                </tbody>
                </table>
                <canvas id="myChart"></canvas>
                </div>
                </body>
                </html>"""
    suitename = suit["robot"]["suite"]["@name"]
    script = "var ctx = document.getElementById('myChart').getContext('2d');var myChart = new Chart(ctx, {{type: 'pie',data: {{labels: ['Pass', 'Fail'],datasets: [{{backgroundColor: ['#2ecc71','#e74c3c' ],data: [{0}, {1}]}}]}}}});$(document).ready(function() {{ $('#dbt').DataTable(); }} );".format(passTest,failTest)
    
    insert = []
    try:
        for i in range (len(test["robot"]["suite"]["suite"])):     
            j= test["robot"]["suite"]["suite"][i]["test"]       
            for k in range (len(j)):
                caseName= j[k]["@name"]
                statusTest= j[k]["status"]["@status"]
                s= test["robot"]["suite"]["suite"][i]["@name"] 
                if statusTest=="FAIL":
                    badge= "red"
                else:
                    badge= "green"

                insert.append("<tr> <td>{3}</td><td>{0} </td><td><span class='uk-badge {2}'>{1}</span> </td></tr>".format(caseName,statusTest,badge,s))
                
        insert.append("<script>{}</script>".format(script))
        Html_file= open("pie_report_{}.html".format(reg_format_date),"w")
        Html_file.write(message.format(''.join(insert)))
        Html_file.close()
        print ("Success Generate Report")
    except:	
        for i in test["robot"]["suite"]["test"]:   
            statusTest= i["status"]["@status"]
            if statusTest=="FAIL":
                    badge= "red"
            else:
                    badge= "green" 
            insert.append("<tr> <td>{3}</td><td>{0} </td><td><span class='uk-badge {2}'>{1}</span> </td></tr>".format(i["@name"], i["status"]["@status"],badge,suitename))
        insert.append("<script>{}</script>".format(script))
        Html_file= open("pie_report_{}.html".format(reg_format_date),"w")
        Html_file.write(message.format(''.join(insert)))
        Html_file.close()
        print ("Success Generate Report")

load = RobotReport()
load.generateReport()
