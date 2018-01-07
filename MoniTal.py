import configparser
import os
import helpers

inipath = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(inipath + '/monital.ini')
# Config Section
slack_enabled = bool(config['config']['enableSlack'])
slack_token = config['config']['slacktoken']
mail_enabled = bool(config['config']['enableMail'])
mailUsername = config['config']['gmailUser']
mailPpassword = config['config']['gmailPass']
# Notification Section
mailTo = str(config['notification']['mailTo']).split(',')
slackChannel = config['notification']['slackChannel']
# Threshold section
memoryThreshold=config['thresholds']['memoryCriticalPercent']
FSThreshold=config['thresholds']['fileSystemCriticalPercent']
processes = str(config['monitor']['process']).split(',')


for process in processes:
    monitoredobject = helpers.MonitoredObject()
    monitoredobject.name = process
    monitoredobject.type = 'process'
    #result = helpers.find_procs_by_name(process)
    monitoredobject.status['text'] = 'normal' if (helpers.find_procs_by_name(process)).__len__() >= 1 else 'critical'
    monitoredobject.status['severity'] = 0 if (helpers.find_procs_by_name(process)).__len__() >= 1 else 1

    if monitoredobject.status['severity'] == 0:
        print(process + " is running....")
        #helpers.sendmail(mailUsername, mailPpassword, mailTo, "Normal " + mailSubject, emailMessageFormat('service',process, 'normal'))
        #helpers.send_slack_message(slack_token, slackChannel, "process " + process + " is normal")
    else:
        print(process + " is not running....")
        #helpers.sendmail(mailUsername, mailPpassword, mailTo, "Critical " + mailSubject, emailMessageFormat('service', process, 'critical'))
        helpers.send_slack_message(slack_token, slackChannel, monitoredobject)
