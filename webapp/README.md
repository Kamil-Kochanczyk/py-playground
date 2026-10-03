# Sample web application

## Minimal 3 tier web application
- **React frontend:** Uses react query to load data from the Node API and display the result
- **Node JS API:** Has `/` and `/ping` endpoints. `/` queries the Database for the current time, and `/ping` returns `pong`
- **Postgres Database:** An empty PostgreSQL database with no tables or data. Used to show how to set up connectivity. The API application executes `SELECT NOW() as now;` to determine the current time to return.
