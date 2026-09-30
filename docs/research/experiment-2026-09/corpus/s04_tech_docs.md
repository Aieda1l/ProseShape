---
title: Rate limiting
sidebar_position: 4
---

# Rate Limiting

In today's fast-paced world of distributed systems, rate limiting plays a crucial role in ensuring the stability and reliability of your APIs. Let's dive into how the Gateway handles it!

## How It Works

The Gateway uses a fixed-window algorithm. Each client, identified by its API key, gets a budget of requests per window. When a client exceeds its budget, the Gateway responds with HTTP `429 Too Many Requests` and includes a `Retry-After` header indicating how many seconds to wait — it's not just an error, it's a signal to back off.

## Configuration

Add a `rate_limit` block to your `gateway.yaml`:

```yaml
rate_limit:
  max_requests: 100
  window_seconds: 60
  burst: 20
```

| Setting | Default | Description |
|---|---|---|
| `max_requests` | 100 | Requests allowed per window |
| `window_seconds` | 60 | Length of the window in seconds |
| `burst` | 0 | Extra requests allowed above the limit |

It's important to note that `burst` defaults to 0, so bursts are disabled unless you set it explicitly. For more details, see https://docs.example.com/gateway/rate-limits.

By leveraging these settings, you can seamlessly strike the perfect balance between protecting your services and delivering a smooth experience for your users.
