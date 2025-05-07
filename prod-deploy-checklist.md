# Production Deployment Template & Checklist

## Assumptions
- It is assumed the deployment item has been successfully tested in a lower environment (e.g., DEV/UAT).
- If testing has not been completed, discuss the exception with the team and VP before proceeding.

## Mandatory Requirements
- A minimum of two team members must be involved in the deployment.
- One team member should be designated as primary, and the other as support/validation.

---

## Deployment Details

### 1. Deployment Steps
List all steps in order, including pre-deployment validation and post-deployment verification.
- Step 1:
- Step 2:
- ...
- Final Step: Confirm success and monitor logs.

### 2. Smoke Test Plan
Post-deployment, a smoke test must be performed to ensure core functionality works as expected.

- Validate key endpoints are responsive (e.g., login, dashboard, main APIs)
- Test critical user workflows
- Check logs for unexpected errors
- Validate DB/service status (if applicable)
- Assign tester(s) and record results

### 3. Deployment Servers/Resources
List servers, services, or resources involved in the deployment.
- App Server:
- Database Server:
- S3 Bucket / Cloud Resource:
- External APIs or third-party integrations:

---

## Rollback Plan

### 4. Rollback Steps
Describe how to restore the system if deployment fails.
- Step 1: Restore previous build (e.g., from backup/artifact).
- Step 2: Restart services.
- Step 3: Validate system health.
- Note: Ensure backup exists before deployment.

---

## Impact Analysis

### 5. Directly Impacted
Services or business processes directly affected by the deployment.
- Service A
- Business Function B

### 6. Indirectly Impacted (Potential)
Services or processes that may be affected indirectly.
- Reporting module
- Downstream APIs
- Data Pipelines

---

## Communication

### 7. Need to Inform Business Users?
- [ ] No  
- [ ] Yes – proceed to steps 8 and 9

### 8. Check with Business Users
If "Yes" above, confirm a suitable deployment window.
- Preferred date/time:
- Stakeholders contacted:

### 9. Send Formal Email
Notify both direct and indirect users.

To: [business_user@example.com]  
CC: [stakeholders]  
Subject: Production Deployment Notification – <App/Service Name>

**Sample Email Body:**
```

Dear Team,

We are planning to deploy \<Feature/Service> to production on <Date> at <Time>. This will impact the following services: ...

If you have concerns, please let us know before \<Date/Time>.

Thanks, <Your Name> | Deployment Team

```

---

## Deployment Schedule

### 10. Deployment Timing
- [ ] Weekend  
- [ ] Weekday  
- Deployment Date:  
- Deployment Time (with timezone):

---

## Final Pre-deployment Checklist

| Item                             | Status     |
|----------------------------------|------------|
| Tested in lower environments     | Yes / No   |
| Exception discussed with VP      | Yes / No   |
| Minimum 2 members available      | Yes / No   |
| Rollback steps ready             | Yes / No   |
| Business users informed (if req) | Yes / No   |
| Backup taken (if need be)        | Yes / No   |
| Communication email sent         | Yes / No   |
| Monitoring plan in place         | Yes / No   |
| Smoke test plan defined          | Yes / No   |
| Smoke test completed post-deploy | Yes / No   |
--------------------------------------------------
