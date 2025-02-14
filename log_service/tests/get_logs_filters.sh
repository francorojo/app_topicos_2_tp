curl -G "http://localhost:5000/logs" \
     --data-urlencode "service=auth" \
     --data-urlencode "limit=20" \
     --data-urlencode "offset=5" \
     --data-urlencode "reversed=true" \
     --data-urlencode "from=2025-01-01 00:00:00" \
     --data-urlencode "to=2025-01-31 23:59:59" \
     --data-urlencode "tag_type=tag_example" \
