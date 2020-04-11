import xmltodict, json
with open('output.xml') as fd:
    doc = xmltodict.parse(fd.read())
    test =json.dumps(doc)
    test =json.loads(test)
passTest = test["robot"]["statistics"]["total"]["stat"][1]["@pass"]
failTest = test["robot"]["statistics"]["total"]["stat"][0]["@fail"]
suitename = test["robot"]["suite"]["@name"]
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

script = "var ctx = document.getElementById('myChart').getContext('2d');var myChart = new Chart(ctx, {{type: 'pie',data: {{labels: ['Pass', 'Fail'],datasets: [{{backgroundColor: ['#2ecc71','#e74c3c' ],data: [{0}, {1}]}}]}}}});".format(passTest,failTest)

insert = []

for i in test["robot"]["suite"]:    
    print (i)
    break
    if i["status"]["@status"]=="FAIL":
        badge= "red"
    else:
        badge= "green"
    print (badge)    
    insert.append("<tr> <td>Transfer</td><td> <td>{0}</td><td> <span class='uk-badge {2}'>{1}</span> </td></tr>".format(i["@name"], i["status"]["@status"],badge))
insert.append("<script>{}</script>".format(script))
Html_file= open("sidara.html","w")
Html_file.write(message.format(''.join(insert)))
Html_file.close()