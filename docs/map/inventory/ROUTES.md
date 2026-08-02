# Route inventory

Generated; do not edit by hand.

| ID | Access | Gates | Client | Tests |
| --- | --- | --- | --- | --- |
| route:DELETE:/api/account | authenticated | — | 0 | 0 |
| route:DELETE:/api/auth/ai-consent | authenticated | — | 0 | 3 |
| route:GET:/api/account/export | owner | — | 0 | 2 |
| route:GET:/api/activity | readonly | — | 1 | 2 |
| route:GET:/api/auth/me | authenticated | — | 1 | 5 |
| route:GET:/api/documents | readonly | — | 1 | 5 |
| route:GET:/api/documents/{document_id} | readonly | — | 1 | 4 |
| route:GET:/api/entities | readonly | — | 0 | 4 |
| route:GET:/api/entities/{entity_id} | readonly | — | 1 | 5 |
| route:GET:/api/file/{document_id} | readonly | — | 0 | 4 |
| route:GET:/api/health | public | — | 0 | 3 |
| route:GET:/api/jobs/{job_id} | readonly | — | 1 | 7 |
| route:GET:/api/messages | readonly | — | 1 | 3 |
| route:GET:/api/ready | public | — | 0 | 2 |
| route:GET:/api/review-items | readonly | — | 1 | 2 |
| route:GET:/api/samples | readonly | — | 1 | 2 |
| route:GET:/api/samples/file/{name} | readonly | — | 0 | 1 |
| route:GET:/api/search | readonly | — | 0 | 2 |
| route:GET:/api/summary | readonly | — | 1 | 10 |
| route:POST:/api/auth/ai-consent | authenticated | — | 1 | 3 |
| route:POST:/api/auth/login | public | — | 1 | 6 |
| route:POST:/api/auth/logout | public | — | 1 | 5 |
| route:POST:/api/auth/password-reset/confirm | public | — | 1 | 2 |
| route:POST:/api/auth/password-reset/request | public | — | 1 | 3 |
| route:POST:/api/auth/signup | public | — | 1 | 7 |
| route:POST:/api/auth/verify-email | public | — | 1 | 4 |
| route:POST:/api/auth/verify-email/request | authenticated | — | 1 | 1 |
| route:POST:/api/chat | member | verified-email, AI-consent | 1 | 7 |
| route:POST:/api/entities | member | — | 1 | 1 |
| route:POST:/api/entities/merge | member | — | 0 | 2 |
| route:POST:/api/entities/{entity_id}/confirm | member | — | 1 | 2 |
| route:POST:/api/entities/{entity_id}/facts | member | — | 1 | 2 |
| route:POST:/api/entities/{entity_id}/unlink | member | — | 1 | 2 |
| route:POST:/api/entities/{entity_id}/unmerge | member | — | 0 | 2 |
| route:POST:/api/facts/{fact_id}/verify | member | — | 1 | 5 |
| route:POST:/api/reset | owner | dev-only | 1 | 6 |
| route:POST:/api/review-items/{item_id}/resolve | member | — | 1 | 1 |
| route:POST:/api/samples/import | member | verified-email, AI-consent | 1 | 4 |
| route:POST:/api/upload | member | verified-email, AI-consent | 1 | 12 |
