import backend.mentor as mentor

# Simulation Data
mock_skills = [
    ("Python", 500),
    ("Terraform", 300),  # Should trigger validation pass for DevOps if not in syllabus?
    ("Communication", 200)
]

print("--- Testing DevOps ---")
s = mentor.generate_mentor_strategy("DevOps Engineer", mock_skills)
print("Role:", s['title'])
print("Stages:")
for stage in s['syllabus']:
    print(f"- [{stage['stage_name']}] {stage['topic']}")

print("\n--- Testing Check ---")
# Check if Terraform is in syllabus
found = any("terraform" in step['topic'].lower() for step in s['syllabus'])
print(f"Terraform found in syllabus: {found}")
if not found:
    print("FAILED: Terraform should be in DevOps syllabus!")

print("\n--- Testing Fallback (Frontend) ---")
mock_skills_fe = [("React", 400), ("CSS", 300), ("Git", 200)]
s_fe = mentor.generate_mentor_strategy("Frontend Developer", mock_skills_fe)
print("Role:", s_fe['title'])
print("First Stage:", s_fe['syllabus'][0])
