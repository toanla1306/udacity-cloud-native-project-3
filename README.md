**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

*TODO:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation
- ![default ns](/answer-img/all-pods-running.png)
- ![default ns](/answer-img/all-svc-running.png)

## Setup the Jaeger and Prometheus source
*TODO:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.
- ![default ns](/answer-img/grafana-web-ui.png)
- ![default ns](/answer-img/grafana-datasources.png)

## Create a Basic Dashboard
*TODO:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.
- ![default ns](/answer-img/basic-dashboard-prometheus.png)

## Describe SLO/SLI
*TODO:* Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.
Actual *monthly uptime* and *request response time* are SLIs (service level indicators, or metrics) that can be used to determine if an SLO has been met. For example, let's say that our SLO for *monthly uptime* is at least 99.99% per month, and our SLO for *request response time* is less than 3 seconds on average.
The following general SLIs can have a bearing on whether the SLOs will be met directly or indirectly. These can be further broken down and visualized via specific metrics. 
- % uptime that a service is active
- Failure rate for a service. This could potentially affect monthly uptime.
- Latency - How long does it take to respond to a request? This directly measures the request response time SLI.
- Saturation - how heavy a load the servers have (saturation). This could cause downtime and slow response times
- Traffic - how much traffic are the servers getting? Perhaps there are times when servers get a spike in traffic. This could directly impact response times and uptime as well.

## Creating SLI metrics.
*TODO:* It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs.
 

## Create a Dashboard to measure our SLIs
*TODO:* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.
- ![default ns](/answer-img/uptime_4xx_5xx_erros.png)

## Tracing our Flask App
*TODO:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here. Also provide a (screenshot) sample Python file containing a trace and span code used to perform Jaeger traces on the backend service.
- ![default ns](/answer-img/backend-tracing-python-code-a.png)
- ![default ns](/answer-img/backend-tracing-python-code-b.png)

## Jaeger in Dashboards
*TODO:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.
- ![default ns](/answer-img/jaegerIn-dashboard-grafana.png)

## Report Error
*TODO:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue also include a screenshot of the tracer span to demonstrate how we can user a tracer to locate errors easily.
- ![default ns](/answer-img/tracing-error-500.png)

TROUBLE TICKET

Name: 500 Error on backend/app.py

Date: September 21 2022, 09:46:35.443

Subject: 500 Error in star endpoint, failed to resolve

Affected Area: File "/app/app.py", line 107, in add_star

Severity: Severe

Description: TypeError: The view function for 'add_star' did not return a valid response. The function either returned None or ended without a return statement.


## Creating SLIs and SLOs (need to fix)
*TODO:* We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name four SLIs that you would use to measure the success of this SLO.
1. Application uptime of 99.95% per month
2. More than 99% of monthly requests should be successful and error free
3. The server resources should not exceed 90% utilization per month
4. The response time of 90% of monthly requests should not exceed 1500ms


## Building KPIs for our plan (need to fix)
*TODO*: Now that we have our SLIs and SLOs, create a list of 2-3 KPIs to accurately measure these metrics as well as a description of why those KPIs were chosen. We will make a dashboard for this, but first write them down here.
1. Error responses 
    a. Ratio with total request < 0.1% per month: KPI will provide an information of quality in whole application and use that ratio to have a decision to hot fix something in application
    b. Ratio with total request in each API < 0.05%: KPI will provide an information in each API, and then the company will easy to know and fix easily.
2. CPU Utilization 
    a. Ratio CPU Utilization of each pod < 90%: The company will know CPU is used in each API, and then can have a decision to increase replicas
    b. Ratio CPU total pod and replicas in each application with total CPU of node < 30% per month (Because in that project we have 3 application): KPI will help company to know when they need to deploy a new node for running application
3. Server Uptime
   a. Ratio downtime/uptime total pods < 0,05% per month: KPI will provide information about the time when server downtime, and then developer will trace log to check application or operator can check again with server that had something wrong.
   b. Ratio downtime/uptime in each application < 0.01% per month: In that information of KPI, company will know something wrong in each application and developer should trace log again to check something wrong in application.
4. Response time
   a. Percentage of total requests on whole application with latency of less than 250ms > 90%: in that KPI, the company can quality on whole application.
   b. Percentage of total requests in each API with latency of less than 250ms > 95%: KPI will provide information to help developer and QA can develop application run faster in each API.

## Final Dashboard (need to describe panel)
*TODO*: Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  
- ![default ns](/answer-img/final-dashboard.png)
Metrics include 9 panels:
- Container Cpu Usage Seconds Total - Total CPU usage in each pod.
- Flask Request Acception - Total number of uncaught exceptions when serving Flask requests.
- Failed Response per Second - Total rate response failed
- Flask HTTP Request Total - Total request to each pod
- 5xx Error - Total request will be had a response with status 5xx error
- 4xx Error - Total request will be had a response with status 4xx error
- Uptime Backend Application - Total backend application uptime
- Uptime Frontend Application - Total frontend application uptime
- Uptime Trial Application - Total trial application uptime