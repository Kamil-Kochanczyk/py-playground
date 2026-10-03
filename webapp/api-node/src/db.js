const fs = require('fs');

const { Pool } = require('pg');

const buildDatabaseUrl = (env = process.env) => {
  if (env.DATABASE_URL) {
    return env.DATABASE_URL;
  }

  if (env.DATABASE_URL_FILE) {
    return fs.readFileSync(env.DATABASE_URL_FILE, 'utf8').replace(/\r?\n$/, '');
  }

  const missing = ['PGHOST', 'PGDATABASE', 'PGUSER'].filter((key) => !env[key]);
  if (!env.PGPASSWORD && !env.PGPASSWORD_FILE) {
    missing.push('PGPASSWORD or PGPASSWORD_FILE');
  }
  if (missing.length > 0) {
    throw new Error(`Missing database configuration: ${missing.join(', ')}`);
  }

  const password = env.PGPASSWORD ?? fs.readFileSync(env.PGPASSWORD_FILE, 'utf8').replace(/\r?\n$/, '');
  const port = env.PGPORT || '5432';

  return `postgresql://${encodeURIComponent(env.PGUSER)}:${encodeURIComponent(password)}@${env.PGHOST}:${port}/${encodeURIComponent(env.PGDATABASE)}`;
};

const databaseUrl = buildDatabaseUrl();

const pool = new Pool({
  connectionString: databaseUrl,
});

// the pool will emit an error on behalf of any idle clients
// it contains if a backend error or network partition happens
pool.on('error', (err, client) => {
  console.error('Unexpected error on idle client', err);
  process.exit(-1);
});

// async/await - check out a client
const getDateTime = async () => {
  const client = await pool.connect();
  try {
    const res = await client.query('SELECT NOW() as now;');
    return res.rows[0];
  } catch (err) {
    console.log(err.stack);
  } finally {
    client.release();
  }
};

module.exports = { buildDatabaseUrl, getDateTime };
