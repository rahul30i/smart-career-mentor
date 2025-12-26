import backend.mentor as mentor
import json

print("\n--- Testing AI Engineer (One-Shot) ---")
ai = mentor.generate_strict_roadmap("AI Engineer", [])
# specific assertion for the one-shot content
assert "Deep Learning Specialization (Andrew Ng)" in str(ai['phases'])
# Llama-3 is in Phase 3 Checkpoint, not Capstone list
assert "Llama-3" in str(ai['phases']) 
print("AI Engineer Title:", ai['role'])
print("Hard Truth:", ai['career_outlook']['hard_truth'])

print("\n--- Testing Marine Biologist (Universal Fallback) ---")
mb = mentor.generate_strict_roadmap("Marine Biologist", [])
assert "Marine Biologist" in mb['role']
assert "Phase 1: Foundations" in mb['phases'][0]['phase_name']
print("Marine Biologist Title:", mb['role'])
