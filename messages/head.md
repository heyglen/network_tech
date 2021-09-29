# [{{version}}] - {{date}}

* Prefix length to subnet mask or wildcard mask conversion snippets will now insert a leading space

Before: "192.0.2.0/24" → "192.0.2.0255.255.255.0"
After: "192.0.2.0/24" → "192.0.2.0 255.255.255.0"
