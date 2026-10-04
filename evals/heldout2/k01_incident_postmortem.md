# Postmortem: Checkout Outage on March 14

## Summary

On March 14, our checkout service experienced a significant outage that lasted 47 minutes, from 14:02 to 14:49 UTC. During this window, approximately 18% of checkout attempts failed, impacting an estimated 2,300 customers. This incident underscores the critical importance of robust configuration management and serves as a powerful reminder that even small changes can have far-reaching consequences.

## Root Cause

The outage was caused by a configuration change to the payment gateway's connection pool. The maximum pool size was inadvertently reduced from 200 to 20 as part of a routine cleanup, which led to connection exhaustion under normal afternoon traffic. It's important to note that the change passed code review, as the diff appeared to be a harmless formatting update.

## Timeline

- **14:02** — Error rates begin climbing on the checkout service.
- **14:09** — On-call engineer Dana Whitfield is paged and begins investigating.
- **14:31** — The team identifies the connection pool setting as the likely culprit.
- **14:49** — The previous configuration is restored and error rates return to normal.

## Action Items

Moving forward, we are committed to ensuring that incidents like this never happen again. Key action items include:

1. **Add validation** for connection pool settings so that values below 100 require explicit approval (Owner: Marcus Lee).
2. **Improve alerting** so that checkout error rates above 5% page the on-call engineer within 2 minutes (Owner: Dana Whitfield).
3. **Update the review checklist** to flag configuration changes hidden in formatting-only diffs (Owner: Priya Nair).

Together, these measures will strengthen our resilience and help us deliver the seamless experience our customers deserve.
