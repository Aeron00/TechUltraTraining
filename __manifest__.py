{
    'name': 'School Management',
    'version': '1.2',
    'author': 'Aeron',
    'category': 'School',
    'summary': 'School information',
    'company': 'Techultra Solutions',
    'description': 'this module contains all the student, teacher and class modules for school',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/school_class_view.xml',
        'views/school_teacher_view.xml',
        'views/school_student_view.xml',
        'views/teacher_result.xml',
        'views/student_result.xml',
        'views/student_time_sheet.xml',
        'views/check_in_check_out.xml',
        'data/ir_cron_late_attend_mail.xml',

    ],
    'installable': True,
    'auto_install': False,
}
