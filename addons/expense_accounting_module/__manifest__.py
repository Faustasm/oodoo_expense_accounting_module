{
    'name': 'Expense accounting module',
    'author': "Faustas Magelinskas",
    'version': '0.1',
    'category': 'Tools',
    'summary': 'Module for expense accounting',
    'installable': True,
    'auto_install': False,
    'application': True,
    'depends': ['base', 'board'],
    'data': [
        'views/main.xml',
        'views/root.xml',
        'security/users.xml',
        'security/security.xml'
    ],
    "external_dependencies": {"python" : ["CurrencyConverter"]}
}
