---
name: database-engineer
description: Design, model, and optimize relational databases using Neon Serverless PostgreSQL and SQLModel. Use for production-grade backend systems.
---

# Database Engineering

## Instructions

1. **Schema Design**
   - Identify core entities and responsibilities
   - Normalize tables (3NF by default)
   - Define primary keys, foreign keys, and constraints
   - Choose appropriate data types for PostgreSQL

2. **Database Platform**
   - Use **Neon Serverless PostgreSQL**
   - Design for stateless, serverless-friendly connections
   - Account for branching (dev/staging/prod)

3. **Modeling with SQLModel**
   - Define models using Python type hints
   - Separate domain models from persistence logic
   - Use explicit relationships and back_populates
   - Prepare models for migrations

4. **Relationships & Integrity**
   - One-to-One, One-to-Many, Many-to-Many
   - Enforce referential integrity with foreign keys
   - Use cascading rules intentionally (CASCADE / RESTRICT)

5. **Query Optimization**
   - Analyze query patterns early
   - Add indexes for:
     - Foreign keys
     - Frequently filtered columns
     - Sorting and lookup fields
   - Avoid N+1 query problems

6. **Connections & Pooling**
   - Use async-compatible drivers when needed
   - Configure connection pooling for serverless usage
   - Handle cold starts and connection reuse safely

7. **Migrations**
   - Generate migration scripts from model changes
   - Ensure migrations are:
     - Idempotent
     - Reversible
     - Environment-safe
   - Never edit production data manually

---

## Best Practices

- Treat schema changes as breaking API changes
- Prefer explicit constraints over application-only validation
- Always index foreign keys
- Keep migrations small and incremental
- Test migrations on a Neon branch before production
- Use transactions for all write operations
- Document schema decisions clearly

---

## Example Structure

### SQLModel Models
```python
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)

    posts: List["Post"] = Relationship(back_populates="author")


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str

    author_id: int = Field(foreign_key="user.id", index=True)
    author: Optional[User] = Relationship(back_populates="posts")
