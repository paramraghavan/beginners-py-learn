# Post-Mortem Report & Corrective Action Checklist

## 1. Incident Summary
- **Incident ID:**  
- **Date & Time (Start):**
- **Date & Time (Reported/Identified):**  
- **Date & Time (End):**  
- **Duration:**  
- **Reported By:**  
- **Owner(s) of Resolution:**  
- **Environment Affected:** Production / UAT / Other  
- **Brief Summary:**  
  > One to two sentences describing what happened.

---

## 2. Impact
- **Systems/Services Affected:**  
- **Business Impact:**  
  - Downtime?
  - Data loss?
  - Delayed processes?
  - Revenue/customer impact?
- **Customers Affected (est.):**  
- **Blast Radius (other systems indirectly affected):**  

---

## 3. Root Cause Analysis (RCA)
- **Primary Cause:**  
- **Contributing Factors:**  
  - Lack of validation?
  - Poor rollback plan?
  - Human error?
  - Monitoring/Alerting gaps?

---

## 4. Timeline of Events
| Time (HH:MM) | Event Description                          |
|--------------|---------------------------------------------|
| 13:20        | Deployment started                          |
| 13:35        | First errors observed                       |
| 13:50        | Outage confirmed                            |
| 14:10        | Initial mitigation steps attempted          |
| 14:40        | Rollback initiated                          |
| 15:05        | System stabilized                           |

---

## 5. Immediate Actions Taken
- Action 1:  
- Action 2:  
- Temporary workarounds?  
- Notifications sent to business/users?

---

## 6. Corrective and Preventive Actions (CAPA)
### A. Technical Fixes
- [ ] Patch or hotfix planned/applied
- [ ] Add automated validation checks (CI/CD gates)
- [ ] Improve logging/observability

### B. Process Improvements
- [ ] Update deployment checklist or release plan
- [ ] Introduce mandatory pre-deploy review/approval
- [ ] Improve rollback/testing procedure
- [ ] Mandate dry runs in staging

### C. Customer Engagement/Communication
- [ ] Better incident comms template or escalation procedure
- [ ] Reassure impacted customers (support follow-ups)

### D. Documentation
- [ ] Update runbooks/playbooks
- [ ] Document lessons learned in team wiki
- [ ] Add scenario to on-call/incident drills

---

## 7. Lessons Learned
- What worked well?
- What didn’t work?
- What can we do differently to reduce risk or blast radius?

---

## 8. Follow-Up Actions
| Action Item                                  | Owner         | Due Date   | Status   |
|---------------------------------------------|---------------|------------|----------|
| Add validation in deployment pipeline        | DevOps Team   | 2025-05-15 | Pending  |
| Schedule RCA review with VP and stakeholders | PM            | 2025-05-10 | Planned  |
| Create test case for similar failure path    | QA Lead       | 2025-05-13 | In Prog. |

---

## 9. Approvals & Final Notes
- **Approved By (Tech Lead):**  
- **Approved By (Product/Business):**  
- **Date of Final Review:**  
- **Related JIRA/Incident Ticket:**  
- **Communication Sent to Team (Yes/No):**

---

## 10. Incident Classification (Optional)
- [ ] P1 - Critical Outage  
- [ ] P2 - High Impact Degradation  
- [ ] P3 - Medium Outage or Non-blocking Failure  
- [ ] P4 - Minor Outage or Non-blocking Failure   
- [ ] Security Incident  
- [ ] Data Loss Event  
- [ ] Third-party Service Impact