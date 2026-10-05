Title: Beyond the Dashboard: Rethinking Observability for Event-Driven Systems

In today's rapidly evolving landscape of distributed systems, observability has become more critical than ever. As organizations increasingly embrace event-driven architectures, traditional monitoring approaches are struggling to keep pace with the complexity of asynchronous workflows.

In this talk, I'll share lessons learned from migrating Corvid Pay's payment pipeline from a request-response model to an event-driven one built on Kafka. Over 18 months, our team reduced mean time to detection from 27 minutes to under 4, while cutting alerting noise by roughly 60%. But the journey wasn't just about tools — it was about fundamentally rethinking how we understand system behavior.

Attendees will learn:

- How to trace a single payment across 14 services using OpenTelemetry context propagation
- Why we abandoned per-service dashboards in favor of event-flow views
- Practical strategies for sampling high-volume topics without losing rare failures

Whether you're just beginning your event-driven journey or looking to level up your existing observability practice, this session will provide actionable insights you can apply immediately. Join me as we explore the future of observability together!

Speaker: Leah Okonkwo-Brandt, Staff Engineer, Corvid Pay
Session length: 40 minutes
