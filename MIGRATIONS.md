## Database Migrations



### Order of intial migrations.

1. migrate accounts without tournament dependency
2. migrate oil_pattern
3. migrate 
4. migrate tournaments
5. migrate accounts with tournament dependency




### Dependenies

- Accounts -> [ Tournaments ]
- Tournaments -> [ Accounts, Oils, Center]
