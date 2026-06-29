"""Seed the database with initial questions"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Question
import json

# EPRA Exam questions
questions_data = [
    {
        "category": "Safety Regulations",
        "difficulty": "medium",
        "question_text": "What is the minimum IP rating required for electrical equipment installed in bathroom zone 1?",
        "options": json.dumps(["IPX4", "IPX5", "IPX7", "IP44"]),
        "correct_answer": "IPX4",
        "explanation": "Bathroom zone 1 requires minimum IPX4 protection against splashing water. Zone 0 requires IPX7 for immersion protection.",
        "regulation_reference": "BS 7671 Section 701 - Locations containing a bath or shower",
        "practical_tip": "Always check the bathroom zone chart before installing any electrical equipment. Zone 1 is above the bath/shower to a height of 2.25m.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "hard",
        "question_text": "What is the maximum disconnection time for a 230V final circuit not exceeding 32A on a TN system?",
        "options": json.dumps(["0.4 seconds", "5 seconds", "0.2 seconds", "1 second"]),
        "correct_answer": "0.4 seconds",
        "explanation": "For final circuits up to 32A on TN systems, the maximum disconnection time is 0.4 seconds as specified in BS 7671.",
        "regulation_reference": "BS 7671 Table 41.1 - Maximum disconnection times",
        "practical_tip": "Test RCDs with a proper RCD tester at 0°, 90°, and 180° to ensure they trip within the required time.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation",
        "difficulty": "easy",
        "question_text": "What is the minimum bending radius for PVC insulated and sheathed cables during installation?",
        "options": json.dumps(["4 times cable diameter", "6 times cable diameter", "8 times cable diameter", "10 times cable diameter"]),
        "correct_answer": "6 times cable diameter",
        "explanation": "PVC cables require a minimum bending radius of 6 times the overall cable diameter to prevent damage to the insulation.",
        "regulation_reference": "BS 7671 522.8.3 - Bending radii",
        "practical_tip": "If the bend is tighter than your fist, it's probably too sharp for most domestic cables!",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "hard",
        "question_text": "Calculate the voltage drop for a 2.5mm² copper cable carrying 20A over 30m. (mV/A/m = 18mV/A/m). Is this acceptable?",
        "options": json.dumps(["10.8V (4.5%) - Not acceptable", "8.6V (3.7%) - Acceptable", "5.4V (2.3%) - Acceptable", "12.4V (5.4%) - Not acceptable"]),
        "correct_answer": "10.8V (4.5%) - Not acceptable",
        "explanation": "Voltage drop = (mV/A/m × current × length) / 1000 = (18 × 20 × 30) / 1000 = 10.8V. As a percentage: (10.8/230) × 100 = 4.7%. This exceeds the 3% maximum for lighting circuits.",
        "regulation_reference": "BS 7671 Appendix 4 - Voltage drop limits",
        "calculation_steps": "1. Vd = (mV/A/m × I × L) / 1000\n2. Vd = (18 × 20 × 30) / 1000\n3. Vd = 10.8V\n4. % = (10.8/230) × 100 = 4.7%\n5. Compare to 3% limit → Exceeds limit",
        "practical_tip": "Use the formula Vd = (mV/A/m × Ib × L) / 1000. Always check voltage drop before finalizing cable size.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "medium",
        "question_text": "What is the correct sequence for initial verification testing of a new electrical installation?",
        "options": json.dumps([
            "Continuity, Insulation Resistance, Polarity, Earth Fault Loop Impedance, RCD",
            "Insulation Resistance, Continuity, RCD, Polarity, Earth Fault Loop Impedance",
            "Polarity, Continuity, Earth Fault Loop Impedance, Insulation Resistance, RCD",
            "RCD, Earth Fault Loop Impedance, Continuity, Insulation Resistance, Polarity"
        ]),
        "correct_answer": "Continuity, Insulation Resistance, Polarity, Earth Fault Loop Impedance, RCD",
        "explanation": "The correct testing sequence is CIPELR: Continuity (dead), Insulation Resistance (dead), Polarity (dead), Earth Fault Loop Impedance (live), RCD (live). First 3 tests are dead tests, last 2 are live tests.",
        "regulation_reference": "BS 7671 Part 6 - Inspection and Testing",
        "practical_tip": "Remember: CIPELR - Continuity, IR, Polarity, EFLI, RCD. Dead tests first, then live tests!",
        "epra_class": "Class C"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "easy",
        "question_text": "What is the standard single-phase voltage supplied by Kenya Power to domestic premises?",
        "options": json.dumps(["240V", "230V", "220V", "250V"]),
        "correct_answer": "240V",
        "explanation": "Kenya Power supplies 240V for single-phase and 415V for three-phase at 50Hz frequency, in accordance with Kenyan standards.",
        "regulation_reference": "Kenya Power Distribution Code",
        "practical_tip": "Always measure the actual supply voltage on site, as it can vary depending on location and loading conditions.",
        "epra_class": "Class C"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "hard",
        "question_text": "What is the maximum earth fault loop impedance (Zs) for a 32A Type B MCB protecting a final circuit on a TN system at 230V?",
        "options": json.dumps(["1.44Ω", "1.15Ω", "0.72Ω", "2.30Ω"]),
        "correct_answer": "1.44Ω",
        "explanation": "Using the formula: Zs = Uo / (In × 5) for Type B MCBs. Zs = 230 / (32 × 5) = 1.44Ω. This ensures the MCB will trip within 0.4 seconds.",
        "regulation_reference": "BS 7671 Table 41.3 - Maximum earth fault loop impedance",
        "calculation_steps": "1. Zs = Uo / (In × multiplier)\n2. For Type B: multiplier = 5\n3. Zs = 230 / (32 × 5)\n4. Zs = 230 / 160\n5. Zs = 1.44Ω",
        "practical_tip": "Always measure Zs at the furthest point of the circuit. If Zs > 1.15Ω, investigate the earthing arrangement.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "medium",
        "question_text": "What RCD rating is required for additional protection of socket-outlets for general use?",
        "options": json.dumps(["30mA", "100mA", "300mA", "10mA"]),
        "correct_answer": "30mA",
        "explanation": "A 30mA RCD provides additional protection against electric shock for socket-outlets and is required by BS 7671 for all general-use socket-outlets.",
        "regulation_reference": "BS 7671 Regulation 411.3.3 - Additional protection",
        "practical_tip": "30mA = Life Safety! Test RCDs quarterly using the test button and annually with an RCD tester.",
        "epra_class": "Class C"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "easy",
        "question_text": "What certificate must be issued before Kenya Power connects a new electrical installation?",
        "options": json.dumps(["Electrical Installation Completion Certificate", "EPRA License", "Kenya Power Work Order", "Local Authority Building Permit"]),
        "correct_answer": "Electrical Installation Completion Certificate",
        "explanation": "An Electrical Installation Completion Certificate, signed by a licensed electrician, must be submitted to Kenya Power before they will connect the supply.",
        "regulation_reference": "Energy Act 2019, Electrical Installation Regulations",
        "practical_tip": "Never energize an installation without the proper completion certificate. Keep copies for your records and provide one to the client.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "easy",
        "question_text": "What is the correct color identification for line conductor in a NEW single-phase installation?",
        "options": json.dumps(["Brown", "Red", "Black", "Blue"]),
        "correct_answer": "Brown",
        "explanation": "Under BS 7671 harmonized colors: Brown = Line (L), Blue = Neutral (N), Green/Yellow = Earth (E). Red was used in old installations pre-2004.",
        "regulation_reference": "BS 7671 Appendix 7 - Harmonized cable core colours",
        "practical_tip": "Brown = L (Line), Blue = N (Neutral), Green/Yellow = E (Earth). Red means it's an old installation - check carefully!",
        "epra_class": "Class C"
    },
    {
        "category": "Isolation & Switching",
        "difficulty": "medium",
        "question_text": "What is the minimum isolation distance required for a main switch disconnector?",
        "options": json.dumps(["3mm contact gap", "1mm contact gap", "5mm contact gap", "10mm contact gap"]),
        "correct_answer": "3mm contact gap",
        "explanation": "BS 7671 requires a minimum 3mm contact separation for isolation purposes to ensure safe disconnection of all live conductors.",
        "regulation_reference": "BS 7671 Regulation 537.2 - Isolation",
        "practical_tip": "Always verify isolation with an approved voltage tester before touching any conductors. Lock off and label the isolator.",
        "epra_class": "Class C"
    },
    {
        "category": "Protection",
        "difficulty": "hard",
        "question_text": "For a 20A radial circuit wired in 2.5mm² cable, what size MCB should be used for overload protection?",
        "options": json.dumps(["20A Type B", "16A Type B", "32A Type B", "25A Type B"]),
        "correct_answer": "20A Type B",
        "explanation": "The MCB rating must be less than or equal to the cable's current-carrying capacity (Iz). For 2.5mm² cable, the MCB should protect both the cable and the load.",
        "regulation_reference": "BS 7671 Regulation 433.1 - Protection against overload current",
        "practical_tip": "Remember: Ib ≤ In ≤ Iz (Design current ≤ MCB rating ≤ Cable capacity). Always check cable rating after applying correction factors.",
        "epra_class": "Class C"
    }
]

def seed_database():
    """Seed the database with questions"""
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Add questions
        questions_added = 0
        for q_data in questions_data:
            # Check if question already exists
            existing = Question.query.filter_by(question_text=q_data["question_text"]).first()
            if not existing:
                question = Question(**q_data)
                db.session.add(question)
                questions_added += 1
        
        db.session.commit()
        print(f"✓ Database seeded successfully!")
        print(f"✓ {questions_added} new questions added")
        print(f"✓ Total questions in database: {Question.query.count()}")

if __name__ == "__main__":
    seed_database()