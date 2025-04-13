# Personalized LinkedIn Job Hunter

Hi and Welcome. This automation fetches personalized (account suggestions based) jobs posted during past 1 hour and sends basic job info to your receiver mails. 

Uses a simple URL query param hack to fetch the jobs from the past hour. This option is not provided by LinkedIn in their UI (at least not in the LinkedIn free member UI).

## Configuration

- [login.py](https://github.com/prezrohit/linkedin-job-hunter/blob/main/login.py) - set your email and password in the corresponding field values. 
	> Only email and password authentication has been successful as of now. I will **probably** be working on other sign in methods later.
- [scrape_jobs.py](https://github.com/prezrohit/linkedin-job-hunter/blob/main/scrape_jobs.py) - does the web scraping magic. uses HTML classes and HTML list iteration-based element fetching. may need improvement in the future.
	> Will throw exception or break the automation if LinkedIn decides to change the HTML class names or change the order of elements.
- [send_mail.py](https://github.com/prezrohit/linkedin-job-hunter/blob/main/send_mail.py) - once the job list is populated, this file sends the basic job info to the specified user list in a simple text format.
	> only gmail server based email sending process is possible right now, which means you need to have a gmail account to be able to send emails
	-  change SENDER to your gmail address
	- change RECEIVER to the email addresses which you want to send the jobs to. comma separated emails addresses.
	- change APP_PASSWORD to your gmail app password. most probably you won't have this set up by default. go to your gmail account settings > security > 2FA > generate app password.

- [job_search_scheduler.py](https://github.com/prezrohit/linkedin-job-hunter/blob/main/job_search_scheduler.py) - runs the schedule of fetching jobs and then sending the mail. set to run every 30 minutes by default



## Running the Automation

Just run the [job_search_scheduler.py](https://github.com/prezrohit/linkedin-job-hunter/blob/main/job_search_scheduler.py) file once you have configured the login and sender, receiver values.
