"""
core features: 
Automated expenses tracker: the program will read bank statements and catergorise spending into relavant sections, e.g. fuel, food, lifestyle
the program should include an accounts database which stores CSV files 
the program should have user authentication
the program should be able to parse the dates on CSVs and generate insigths about changes over time

core tools: 
FastApi
Docker for development
CI tools
Vanilla JS (or a framework if more appropriate)

core principles: 
OOP must be adhered to
Must implement proper secuirty to avoid leaking of potentially sensitive documents 


PROJECT SETUP: 
    - set up database: postgreSQL
        define tables for:
        user(authentication)
        account(stores bank details)
        Transaction(stores parsed expenses)
    - implement user auth 
        either oauth or JWT api security
        store hashed passwords
        implement login / signup endpoints
PHASE 2: CSV PROCESSING AND EXPENSE CATEGORISATION
    -use pandas to write a CSV parser
        Date
        Amount
        Transaction Typle
        MErhcnat
    - implement rule based categorisation
        use a dict mapping known merchants to vendors 
        apply default rules for mapping merchants to categories

    PHASE 3:
        - imlement data based filtering 
            parse dates and store them in the database 
        - generate insights over time
    
    PHASE 4:
        API & FRONTEND: 
    
    PHASE 5:
        SECURITY & CI/CD



    TO DO: HTTPS







 """