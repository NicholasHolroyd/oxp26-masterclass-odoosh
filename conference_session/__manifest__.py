{
    'name': 'Conference Sessions',
    'version': '19.0.1',
    'summary': 'Track sessions for conferences and training events',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/conference_session_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
