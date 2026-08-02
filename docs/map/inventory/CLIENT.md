# Client API inventory

Generated; do not edit by hand.

| ID | Routes | Calls | Consumers | Confidence |
| --- | --- | --- | --- | --- |
| clientapi:activity | GET /api/activity | — | client/src/views/History.jsx | exact |
| clientapi:chat | POST /api/chat | — | client/src/views/Assistant.jsx | exact |
| clientapi:confirmEntity | POST /api/entities/{param}/confirm | — | client/src/components/EntityCardDetail.jsx | exact |
| clientapi:confirmPasswordReset | POST /api/auth/password-reset/confirm | — | client/src/auth/TokenScreen.jsx | exact |
| clientapi:createEntity | POST /api/entities | — | client/src/components/EntityCreateDialog.jsx | exact |
| clientapi:createEntityFact | POST /api/entities/{param}/facts | — | client/src/components/EntityCardDetail.jsx | exact |
| clientapi:document | GET /api/documents/{id} | — | client/src/components/DocumentDrawer.jsx | exact |
| clientapi:entityCard | GET /api/entities/{param} | — | client/src/components/EntityCardDetail.jsx | exact |
| clientapi:importSample | POST /api/samples/import | — | client/src/api.js | exact |
| clientapi:importSampleAndWait | — | clientapi:importSample | client/src/views/Capture.jsx | exact |
| clientapi:job | GET /api/jobs/{id} | — | client/src/api.js | exact |
| clientapi:listDocuments | GET /api/documents?{param} | — | client/src/lib.jsx | exact |
| clientapi:listEntities | GET /api/entities{param} | — | client/src/components/UnlinkDialog.jsx, client/src/views/Entities.jsx, client/src/views/Familie.jsx | exact |
| clientapi:listReviewItems | GET /api/review-items?status={param} | — | client/src/components/ReviewInbox.jsx | exact |
| clientapi:login | POST /api/auth/login | — | client/src/auth/AuthProvider.jsx, client/src/auth/AuthScreen.jsx | exact |
| clientapi:logout | POST /api/auth/logout | — | client/src/auth/AuthProvider.jsx | exact |
| clientapi:me | GET /api/auth/me | — | client/src/auth/AuthProvider.jsx | exact |
| clientapi:messages | GET /api/messages | — | client/src/views/Assistant.jsx | exact |
| clientapi:requestEmailVerification | POST /api/auth/verify-email/request | — | client/src/auth/EmailVerificationBanner.jsx | exact |
| clientapi:requestPasswordReset | POST /api/auth/password-reset/request | — | client/src/auth/AuthScreen.jsx | exact |
| clientapi:reset | POST /api/reset | — | client/src/App.jsx | exact |
| clientapi:resolveReviewItem | POST /api/review-items/{param}/resolve | — | client/src/components/ReviewInbox.jsx | exact |
| clientapi:samples | GET /api/samples | — | client/src/views/Capture.jsx | exact |
| clientapi:setAiConsent | POST /api/auth/ai-consent | — | client/src/views/Assistant.jsx, client/src/views/Capture.jsx | exact |
| clientapi:signup | POST /api/auth/signup | — | client/src/auth/AuthScreen.jsx | exact |
| clientapi:summary | GET /api/summary | — | client/src/lib.jsx | exact |
| clientapi:unlinkEntity | POST /api/entities/{param}/unlink | — | client/src/components/UnlinkDialog.jsx | exact |
| clientapi:upload | POST /api/upload | — | client/src/api.js | exact |
| clientapi:uploadAndWait | — | clientapi:upload | client/src/views/Capture.jsx | exact |
| clientapi:verifyEmail | POST /api/auth/verify-email | — | client/src/auth/TokenScreen.jsx | exact |
| clientapi:verifyFact | POST /api/facts/{id}/verify | — | client/src/components/EntityCardDetail.jsx, client/src/views/DatabaseView.jsx, client/src/views/Fakten.jsx | exact |
