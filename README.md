# expense_accounting_module
Expense accounting module for interview task
### Requirements
```
docker
docker-compose
```

### Full usage example

1. From directory where docker-compose.yml resides run:
```
docker-compse up -d
Alternatively copy the module folder to local odoo enviornment and install external dependencies

```
All supported languages can be seen here https://www.jaided.ai/easyocr/

2. Open http://localhost:8069
```
master password is odoo13@2025
Test users:
admin -> login: admin pass: admin
manager -> login: manager pass: manager
financeer -> login: financeer pass: financeer
employee -> login: employee pass: employee

Alternatively assign to one of the groups in settings with the same user database is initiated

```

3. From root directory start docker container
```
docker-compose up -d
```


### Known Issues

* Known error with dashboard utility and old odoo versions where it throws error if clicked on diagrams
* After installing the module user gets permission errors, to avoid just assign one of the groups to user in settings or login with provided users after installing module. Logging out and in might be needed to see permission changes.
