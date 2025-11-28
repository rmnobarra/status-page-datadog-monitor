#!/bin/bash

# CRUD API Test Script
# Tests all monitor and incident CRUD operations

BASE_URL="http://localhost:8000"

echo "================================"
echo "Testing Status Page CRUD API"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local expected_code=$4
    local description=$5

    echo -e "${YELLOW}TEST:${NC} $description"
    echo "  $method $endpoint"

    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq "$expected_code" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $http_code)"
    else
        echo -e "${RED}✗ FAIL${NC} (Expected HTTP $expected_code, got $http_code)"
    fi

    if [ ! -z "$body" ]; then
        echo "  Response: $(echo $body | python3 -m json.tool 2>/dev/null || echo $body)"
    fi
    echo ""
}

echo "=== MONITOR CRUD TESTS ==="
echo ""

# List monitors
test_endpoint "GET" "/api/monitors/list" "" 200 "List all monitors"

# Create monitor
test_endpoint "POST" "/api/monitors" \
    '{"url_monitor":"TEST123","nome_monitor":"Test Monitor","descricao_monitor":"For testing"}' \
    201 "Create new monitor"

# Get single monitor
test_endpoint "GET" "/api/monitors/TEST123" "" 200 "Get specific monitor"

# Update monitor
test_endpoint "PUT" "/api/monitors/TEST123" \
    '{"nome_monitor":"Updated Test Monitor"}' \
    200 "Update monitor"

# Delete monitor
test_endpoint "DELETE" "/api/monitors/TEST123" "" 204 "Delete monitor"

# Verify deletion
test_endpoint "GET" "/api/monitors/TEST123" "" 404 "Verify monitor deleted"

echo ""
echo "=== INCIDENT CRUD TESTS ==="
echo ""

# List incidents
test_endpoint "GET" "/api/incidents/list" "" 200 "List all incidents"

# Create incident
test_endpoint "POST" "/api/incidents" \
    '{"id":"INC-TEST-001","title":"Test Incident","status":"investigating","severity":"minor","created_at":"2025-11-28T10:00:00","resolved_at":null,"affected_services":["Test Service"],"updates":[{"timestamp":"2025-11-28T10:00:00","status":"investigating","message":"Testing incident creation"}]}' \
    201 "Create new incident"

# Get single incident
test_endpoint "GET" "/api/incidents/INC-TEST-001" "" 200 "Get specific incident"

# Add update to incident
test_endpoint "POST" "/api/incidents/INC-TEST-001/updates" \
    '{"status":"resolved","message":"Test completed successfully"}' \
    200 "Add update to incident"

# Update incident
test_endpoint "PUT" "/api/incidents/INC-TEST-001" \
    '{"severity":"major"}' \
    200 "Update incident"

# Delete incident
test_endpoint "DELETE" "/api/incidents/INC-TEST-001" "" 204 "Delete incident"

# Verify deletion
test_endpoint "GET" "/api/incidents/INC-TEST-001" "" 404 "Verify incident deleted"

echo ""
echo "================================"
echo "All tests completed!"
echo "================================"
echo ""
echo "View API documentation: $BASE_URL/docs"
echo "View status page: http://localhost"
