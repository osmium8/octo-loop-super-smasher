import datetime
from datetime import timedelta
from flask import Blueprint, Response, request
from ..model.models import Report
from ..helpers.date_time_helpers import *
from ..helpers.report_helpers import *
from ..helpers.extrapolation_helpers import *
from ..repos.extrapolation_data import *
from ..repos.polls import *
from ..repos.menu_hours import *
from ..repos.report import *
from ..extensions import q
from ..tasks import generate_report

report = Blueprint('report', __name__)

@report.route('/report/trigger_report', methods=['POST'])
def tirgger_report():
    store_id = request.args['store_id']
    current_time = datetime.datetime.now()

    week = get_week_of_year(current_time)
    day = get_day(current_time)
    window = get_window(current_time)

    report_id = generate_report_id(store_id, week, day, window)
    report = get_report(report_id)

    if (report is None):
        job = q.enqueue(generate_report, report_id, store_id, current_time)
        return {'report_id': report_id, 'job_id': job.id}, 202
    
    return {'report_id': report_id, 'status': 'already generated'}, 200
    
@report.route('/report/get_report', methods=(['GET']))
def get_report_route():
    report_id = request.args['report_id']
    report: Report = get_report(report_id)
    if (report is not None):
        return {
            'status': 'generated', 
            'report': {
                'id': report.report_id, 
                'uptime_last_hour': f'{report.uptime_last_hour} mins',
                'uptime_last_day': f'{report.uptime_last_day} hours',
                'uptime_last_week': f'{report.uptime_last_week} hours',
                'downtime_last_hour': f'{report.downtime_last_hour} mins',
                'downtime_last_day': f'{report.downtime_last_day} hours',
                'downtime_last_week': f'{report.downtime_last_week} hours'
                }
            }, 200
    else:
        return {'status': 'running', 'message': 'Report is not generated yet'}, 202