from ..model.models import Report

def get_report(report_id):
    report = Report.query.filter_by(report_id=report_id).first()
    return report