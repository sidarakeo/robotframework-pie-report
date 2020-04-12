__author__ = 'KEO_Sidara'
__Version__ = '0.1.1'
import xmltodict, json ,datetime

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
        print(reg_format_date)
    except Exception as e:
       return print(e)
        
    message = """
                <html>
                <head>
                <!-- UIkit CSS -->
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/css/uikit.min.css" />

                <!-- UIkit JS -->
                <script src="https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/js/uikit.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/js/uikit-icons.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/chart.js@2.8.0"></script>
                
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
            <a class="uk-navbar-item uk-logo"  >LOGO</a>
            <ul class="uk-navbar-nav">
                <li class="uk-active"><a href="#">HOME</a></li>
                
            </ul>

        </div>
    </nav>
                <div class="uk-container uk-container-xsmall">
                <h1>Robot Report</h1>
                <canvas id="myChart"></canvas>
                <table class="uk-table uk-table-hover uk-table-divider">
                <tr>
                <th>Suite Name</th>
                <th>  Test Case</th>
                <th>Status</th>
                </tr>
                {0}
                </table>
                <canvas id="myChart"></canvas>
                </div>
                </body>
                </html>"""
    suitename = suit["robot"]["suite"]["@name"]
    script = "var ctx = document.getElementById('myChart').getContext('2d');var myChart = new Chart(ctx, {{type: 'pie',data: {{labels: ['Pass', 'Fail'],datasets: [{{backgroundColor: ['#2ecc71','#e74c3c' ],data: [{0}, {1}]}}]}}}});".format(passTest,failTest)
    insert = []
    try:
        for i in range (len(test["robot"]["suite"]["suite"])):     
            j= test["robot"]["suite"]["suite"][i]["test"]       
            for k in range (len(j)):
                caseName= j[k]["@name"]
                statusTest= j[k]["status"]["@status"]
                print (statusTest)
                s= test["robot"]["suite"]["suite"][i]["@name"] 
                print (s)
            
                if statusTest=="FAIL":
                    badge= "red"
                else:
                    badge= "green"

                insert.append("<tr> <td>{3}</td><td>{0} </td><td><span class='uk-badge {2}'>{1}</span> </td></tr>".format(caseName,statusTest,badge,s))
                
        insert.append("<script>{}</script>".format(script))
        Html_file= open("pie_report_{}.html".format(reg_format_date),"w")
        Html_file.write(message.format(''.join(insert)))
        Html_file.close()
    except:	
        for i in test["robot"]["suite"]["test"]:    
            insert.append("<tr> <td>{3}</td><td>{0} </td><td><span class='uk-badge {2}'>{1}</span> </td></tr>".format(i["@name"], i["status"]["@status"],passTest,suitename))
        insert.append("<script>{}</script>".format(script))
        Html_file= open("pie_report_{}.html".format(reg_format_date),"w")
        Html_file.write(message.format(''.join(insert)))
        Html_file.close()

load = RobotReport()
load.generateReport()
