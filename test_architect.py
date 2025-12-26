import backend.mentor as mentor

print("--- Testing Architect Mode for DevOps ---")
blueprint = mentor.generate_architect_blueprint("DevOps Engineer", [("Terraform", 100), ("Python", 50)])

print(f"Title: {blueprint['role_title']}")
print(f"Phases: {len(blueprint['phases'])}")
print(f"Phase 1 Name: {blueprint['phases'][0]['phase_name']}")
print(f"Resources (Paid): {blueprint['resources']['paid']}")
print(f"Portfolio L3 Stack: {blueprint['portfolio'][2]['stack']}")

print("\n--- Testing Fallback for 'React Dev' ---")
fb = mentor.generate_architect_blueprint("React Developer", [("React", 100), ("Redux", 80), ("CSS", 50)])
print(f"Title: {fb['role_title']}")
print(f"Phase 1 Topic: {fb['phases'][0]['topics'][0]['name']}")
