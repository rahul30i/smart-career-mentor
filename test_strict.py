import backend.mentor as mentor
import json

print("\n--- Testing Strict DevOps ---")
roadmap = mentor.generate_strict_roadmap("DevOps Engineer", [])
# Verify key fields exist
assert "role" in roadmap
assert "estimated_total_time" in roadmap
assert "phases" in roadmap
assert "projects" in roadmap
assert "best_resources" in roadmap["phases"][0] # Check nesting

print(json.dumps(roadmap, indent=2))

print("\n--- Testing Strict Fallback ---")
fb = mentor.generate_strict_roadmap("Vue Developer", [("Vue.js", 10), ("JavaScript", 10)])
print(json.dumps(fb, indent=2))
