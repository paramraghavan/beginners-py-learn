# Backend & API Rules

## API Design
- Use RESTful conventions: proper HTTP methods, status codes, and resource naming.
- All endpoints must validate input — never trust client data.
- Return consistent response shapes: `{ data, error, meta }` or your project's convention.
- Use pagination for list endpoints — never return unbounded collections.
- Include request IDs in responses for debugging.
- Version APIs from day one (`/api/v1/`).

## Database
- IMPORTANT: Never write raw SQL without parameterized queries — prevent SQL injection.
- Use migrations for all schema changes — never modify the database manually.
- Add indexes for columns used in WHERE, JOIN, and ORDER BY clauses.
- Use transactions for multi-step operations that must be atomic.
- Always set appropriate column constraints (NOT NULL, UNIQUE, CHECK).
- Log slow queries and optimize them.

## Security
- Validate and sanitize all user input at the boundary.
- Use bcrypt/argon2 for password hashing — never MD5 or SHA for passwords.
- Implement rate limiting on authentication and public endpoints.
- Use HTTPS everywhere. No HTTP fallbacks.
- Apply principle of least privilege for database users and service accounts.
- Set security headers: CORS, CSP, X-Frame-Options, etc.

## Performance
- Use connection pooling for database connections.
- Cache expensive computations and frequently-read data with appropriate TTLs.
- Use async/non-blocking I/O for network and file operations.
- Profile before optimizing — measure, don't guess.
- Set timeouts on all external calls (HTTP, database, queues).
