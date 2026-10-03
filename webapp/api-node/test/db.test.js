const fs = require('fs');
const os = require('os');
const path = require('path');

const { buildDatabaseUrl } = require('../src/db');

test('uses DATABASE_URL when it is provided', () => {
  expect(buildDatabaseUrl({ DATABASE_URL: 'postgresql://user:pass@db:5432/app' })).toBe(
    'postgresql://user:pass@db:5432/app'
  );
});

test('builds a URL from PostgreSQL environment variables and the password secret', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'api-node-db-'));
  const passwordFile = path.join(directory, 'password');
  fs.writeFileSync(passwordFile, 'p@ss:/?#%\n');

  try {
    expect(
      buildDatabaseUrl({
        PGHOST: 'postgres',
        PGPORT: '5432',
        PGDATABASE: 'postgres',
        PGUSER: 'api@user',
        PGPASSWORD_FILE: passwordFile,
      })
    ).toBe('postgresql://api%40user:p%40ss%3A%2F%3F%23%25@postgres:5432/postgres');
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
});
