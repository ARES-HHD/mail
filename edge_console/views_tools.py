# encoding: utf-8

from django.core.mail import send_mass_mail, EmailMessage
from django.shortcuts import render_to_response, render
from django.template import RequestContext

import preference

def alarm_message_sendmail(request):
    """重大变更邮件通知
    Args:
        request:
    """
    value_dict = {}
    group_name = "EMAIL"
    try:
        group_names = preference.get_group_keys(group_name)
    except:
        group_names = []

    try:
        if group_names:
            key = request.GET.get('select_template',group_names[0])
        else:
            key = None
        value = preference.get_string_value(key)
        value_list = re.split(r'[\n:]',value,8)
        for i in range(0, 7, 2): # 偶数为key, 奇数为value
            value_dict[value_list[i].title()] = value_list[i+1]

        alarm_message_from_email = value_dict["From"].strip()
        alarm_message_admin_email = value_dict["To"].strip().split(',')
        alarm_message_sub_admin_email = value_dict["Cc"].strip().split(',')
        mail_subject = value_dict["Subject"].strip()
        mail_message = value_list[8].strip()

        mail_from = alarm_message_from_email
        mail_to = ', '.join(alarm_message_admin_email)
        mail_cc = ', '.join(alarm_message_sub_admin_email)
    except Exception as e:
        result_type = 'error'
        result = "没有模板！请在Console全局选项设定里添加模板。"
        mail_from = None
        mail_to = None
        mail_cc = None
        mail_subject = None
        mail_message = None
    else:
        result = None
        result_type = 'success'

    if request.method == 'POST':
        #print request.POST['submit']
        mail_subject = request.POST['mail_subject']
        mail_message = request.POST['mail_message']

        result = '邮件发送成功!'
        result_type = 'success'
        try:
            msg = EmailMessage(mail_subject, mail_message,
                           alarm_message_from_email,
                           alarm_message_admin_email,
                           cc=alarm_message_sub_admin_email
                           )
            msg.send()
        except Exception, e:
            result_type = 'error'
            result = e

    return render_to_response('console/sendmail.html', {
            'mail_from': mail_from,
            'mail_to': mail_to,
            'mail_cc': mail_cc,
            'mail_subject': mail_subject,
            'mail_message': mail_message,
            'result': result,
            'result_type': result_type,
            'key': key,
            'group_names': group_names,
            }, context_instance=RequestContext(request))