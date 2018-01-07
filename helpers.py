import pdb

def sendmail(username, password, to, subject, body):
    import yagmail
    yag = yagmail.SMTP(username, password)
    to = to
    subject = subject
    body = body
    yag.send(to=to, subject=subject, contents=body)

def find_procs_by_name(name):
    import os
    import psutil
    '''Return a list of processes matching 'name'.'''
    ls = []
    for p in psutil.process_iter(attrs=["name", "exe", "cmdline"]):
        if name == p.info['name'] or \
                p.info['exe'] and os.path.basename(p.info['exe']) == name or \
                p.info['cmdline'] and p.info['cmdline'][0] == name:
            ls.append(p)
    return ls

def get_mem_used():
    return float((psutil.virtual_memory()).percent)

def get_fs_used(fs_mount):
    float((psutil.disk_usage(fs_mount)).percent)

def emailMessageFormat(monitorType, name, status):
    if monitorType == 'service' and status == 'normal':
        ServiceOK = '<p><strong><span style="color: #00ff00;">Service ' + name + ' is running!</span></strong></p>'
        return ServiceOK

    if monitorType == 'service' and status == 'critical':
        ServiceNotOK = '<p><strong><span style="color: #ff0000;">Service ' + name + ' is not running!</span></strong></p>'
        return ServiceNotOK

def set_color_by_severity(severity):
    if (severity == "normal"):
        return "#00b300"
    if (severity == "critical"):
        return "#ff0000"

def send_slack_message(slack_token, slackChannel, data):
    from slackclient import SlackClient
    sc = SlackClient(slack_token)

    # sc.api_call(
    #   "chat.postMessage",
    #    channel=slackChannel,
    #   text=text,
    #   username='MoniTal',
    #   icon_emoji=':robot_face:'
    # )
    #pdb.set_trace()
    attachments = [{"fallback": "Required plain-text summary of the attachment.",
                    "color": set_color_by_severity(data.status['text']),
                    "pretext": "ALERT - " + data.name + " is " + data.status['text'],
                    "author_name": "MoniTal",
                    "author_link": "https://github.com/TalZiv/",
                    "author_icon": "https://cdn4.iconfinder.com/data/icons/space-and-astronomy-1/800/robot-512.png",
                    "title": data.type + " on " + data.hostname + " is " + data.status['text'],
                    "title_link": "ssh://root@" + data.hostname + ":6633/",
                    "text": "Please check " + data.name,
                    "fields": [
                        {
                            "title": "Priority",
                            "value": "High",
                            "short": False
                        }],
                    "image_url": "http://my-website.com/path/to/image.jpg",
                    "thumb_url": "http://example.com/path/to/thumb.png",
                    "footer": "Slack API",
                    "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                    "ts": 123456789
                    }
                   ]
    sc.api_call("chat.postMessage", channel=slackChannel, text="", attachments=attachments)

class MonitoredObject:
    def __init__(self):
        import socket
        self.type = ""
        self.name = ""
        self.status = {'text': 'Unknown', 'severity': 'Unknown'}
        self.hostname = socket.gethostname()


