"""Seed the database with 160 EPRA exam questions"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Question
import json

# ============================================================
# 160 EPRA EXAM QUESTIONS - SAFARI SOFTWARES © 2026
# 100 Theory + 60 Practical Scenarios
# ============================================================

questions_data = [
    # ========================
    # SAFETY REGULATIONS (15 Theory + 8 Practical = 23)
    # ========================
    
    # Theory Questions
    {
        "category": "Safety Regulations",
        "difficulty": "medium",
        "question_text": "What is the minimum IP rating required for electrical equipment installed in bathroom zone 1?",
        "options": json.dumps(["IPX4", "IPX5", "IPX7", "IP44"]),
        "correct_answer": "IPX4",
        "explanation": "Bathroom zone 1 requires minimum IPX4 protection against splashing water. Zone 0 requires IPX7 for immersion protection.",
        "regulation_reference": "BS 7671 Section 701",
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
        "regulation_reference": "BS 7671 Table 41.1",
        "practical_tip": "Test RCDs with a proper RCD tester at 0°, 90°, and 180° to ensure they trip within the required time.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "medium",
        "question_text": "What RCD rating is required for additional protection of socket-outlets for general use?",
        "options": json.dumps(["30mA", "100mA", "300mA", "10mA"]),
        "correct_answer": "30mA",
        "explanation": "A 30mA RCD provides additional protection against electric shock for socket-outlets and is required by BS 7671.",
        "regulation_reference": "BS 7671 Regulation 411.3.3",
        "practical_tip": "30mA = Life Safety! Test RCDs quarterly using the test button and annually with an RCD tester.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "easy",
        "question_text": "What is the correct color identification for line conductor in a NEW single-phase installation?",
        "options": json.dumps(["Brown", "Red", "Black", "Blue"]),
        "correct_answer": "Brown",
        "explanation": "Under BS 7671 harmonized colors: Brown = Line (L), Blue = Neutral (N), Green/Yellow = Earth (E). Red was used in old installations pre-2004.",
        "regulation_reference": "BS 7671 Appendix 7",
        "practical_tip": "Brown = L (Line), Blue = N (Neutral), Green/Yellow = E (Earth). Red means it's an old installation - check carefully!",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "medium",
        "question_text": "What is the minimum height for socket-outlets in a new domestic kitchen?",
        "options": json.dumps(["450mm above worktop", "150mm above worktop", "300mm above worktop", "600mm above worktop"]),
        "correct_answer": "150mm above worktop",
        "explanation": "Socket-outlets should be mounted at least 150mm above the worktop surface to prevent damage from water and spills.",
        "regulation_reference": "BS 7671 553.1.6",
        "practical_tip": "Measure from the finished worktop level, not the floor. Consider tile splashbacks in your positioning.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "hard",
        "question_text": "What is the maximum earth fault loop impedance for a 32A Type C MCB on a TN system at 230V?",
        "options": json.dumps(["0.72Ω", "1.44Ω", "0.36Ω", "2.88Ω"]),
        "correct_answer": "0.72Ω",
        "explanation": "Type C MCBs require 10x rated current for instantaneous trip. Zs = 230/(32×10) = 0.72Ω. This is half the Type B value.",
        "regulation_reference": "BS 7671 Table 41.3",
        "calculation_steps": "1. Type C multiplier = 10\n2. Zs = 230 / (32 × 10)\n3. Zs = 230 / 320\n4. Zs = 0.72Ω",
        "practical_tip": "Type C MCBs need lower Zs than Type B. Always verify your earthing arrangement can achieve this.",
        "epra_class": "Class B"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "easy",
        "question_text": "Which document must be completed before energizing a new electrical installation in Kenya?",
        "options": json.dumps(["Electrical Installation Completion Certificate", "EPRA License", "Kenya Power Work Order", "Local Authority Permit"]),
        "correct_answer": "Electrical Installation Completion Certificate",
        "explanation": "An Electrical Installation Completion Certificate, signed by a licensed electrician, must be submitted to Kenya Power before connection.",
        "regulation_reference": "Energy Act 2019",
        "practical_tip": "Keep copies of all certificates for your records. Digital photos of completed installations are also recommended.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "medium",
        "question_text": "What is the minimum cross-sectional area of a main protective bonding conductor for a TN-S system with 25mm² line conductor?",
        "options": json.dumps(["10mm²", "16mm²", "6mm²", "25mm²"]),
        "correct_answer": "10mm²",
        "explanation": "For TN-S systems, the main protective bonding conductor must be at least half the size of the main earthing conductor, minimum 6mm² and not exceeding 25mm².",
        "regulation_reference": "BS 7671 Table 54.8",
        "practical_tip": "Always check Table 54.8 for exact sizing. Don't guess - undersized bonding conductors are dangerous.",
        "epra_class": "Class B"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "hard",
        "question_text": "In a bathroom, which zone requires electrical equipment to be IPX7 rated?",
        "options": json.dumps(["Zone 0", "Zone 1", "Zone 2", "Outside zones"]),
        "correct_answer": "Zone 0",
        "explanation": "Zone 0 is the interior of the bath or shower tray where equipment can be immersed in water. IPX7 is required for immersion protection.",
        "regulation_reference": "BS 7671 Section 701.512.2",
        "practical_tip": "Zone 0 = inside bath/shower tray. Only SELV equipment at 12V or less is permitted in Zone 0.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "easy",
        "question_text": "What is the maximum permitted voltage for SELV (Separated Extra Low Voltage) circuits?",
        "options": json.dumps(["50V AC", "120V AC", "230V AC", "12V AC"]),
        "correct_answer": "50V AC",
        "explanation": "SELV circuits must not exceed 50V AC or 120V DC to ensure safety against electric shock.",
        "regulation_reference": "BS 7671 Part 4, Chapter 41",
        "practical_tip": "SELV is commonly used in bathroom lighting, garden lighting, and construction site temporary supplies.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "medium",
        "question_text": "How often should RCDs be tested using the integral test button?",
        "options": json.dumps(["Quarterly", "Monthly", "Annually", "Weekly"]),
        "correct_answer": "Quarterly",
        "explanation": "BS 7671 recommends testing RCDs quarterly using the integral test button to ensure mechanical operation.",
        "regulation_reference": "BS 7671 Regulation 643.10",
        "practical_tip": "Set calendar reminders for quarterly RCD testing. Record results in a logbook for compliance.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "hard",
        "question_text": "What is the maximum disconnection time for a 400V distribution circuit on a TN system?",
        "options": json.dumps(["5 seconds", "0.4 seconds", "1 second", "0.2 seconds"]),
        "correct_answer": "5 seconds",
        "explanation": "Distribution circuits on TN systems have a maximum disconnection time of 5 seconds, unlike final circuits which require 0.4 seconds.",
        "regulation_reference": "BS 7671 Table 41.1",
        "practical_tip": "Remember: Final circuits ≤32A = 0.4s, Distribution circuits = 5s.",
        "epra_class": "Class B"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "medium",
        "question_text": "What is the minimum insulation resistance for a new 230V domestic circuit?",
        "options": json.dumps(["1 MΩ", "0.5 MΩ", "2 MΩ", "5 MΩ"]),
        "correct_answer": "1 MΩ",
        "explanation": "The minimum insulation resistance for circuits up to 500V is 1 MΩ according to BS 7671 Table 61.",
        "regulation_reference": "BS 7671 Table 61",
        "practical_tip": "Always test at 500V DC for 230V circuits. If reading is below 1 MΩ, investigate each circuit section.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "easy",
        "question_text": "Which type of fire extinguisher is suitable for electrical fires?",
        "options": json.dumps(["CO2", "Water", "Foam", "Wet chemical"]),
        "correct_answer": "CO2",
        "explanation": "CO2 extinguishers are suitable for electrical fires as they don't conduct electricity and leave no residue.",
        "regulation_reference": "Fire Safety Regulations",
        "practical_tip": "Never use water on electrical fires! CO2 or dry powder extinguishers are the correct choice.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "hard",
        "question_text": "What is the maximum Zs for a 6A Type B MCB on a 230V TN system?",
        "options": json.dumps(["7.67Ω", "4.60Ω", "3.83Ω", "15.33Ω"]),
        "correct_answer": "7.67Ω",
        "explanation": "Zs = 230/(6×5) = 230/30 = 7.67Ω. Lower current MCBs allow higher Zs values.",
        "regulation_reference": "BS 7671 Table 41.3",
        "calculation_steps": "1. Type B multiplier = 5\n2. Zs = 230 / (6 × 5)\n3. Zs = 230 / 30\n4. Zs = 7.67Ω",
        "practical_tip": "Lighting circuits with 6A MCBs are more forgiving on Zs values than power circuits.",
        "epra_class": "Class C"
    },
    
    # Practical Scenario Questions
    {
        "category": "Safety Regulations",
        "difficulty": "medium",
        "question_text": "PRACTICAL: You are installing a socket-outlet in a bathroom. The homeowner wants it next to the washbasin. What is the minimum distance from the edge of the washbasin?",
        "options": json.dumps(["300mm", "150mm", "600mm", "100mm"]),
        "correct_answer": "300mm",
        "explanation": "Socket-outlets must be at least 300mm from the edge of a washbasin or draining board to prevent water ingress.",
        "regulation_reference": "BS 7671 701.512.3",
        "practical_tip": "Measure from the edge of the basin, not the center. Consider splash zones when positioning.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "hard",
        "question_text": "PRACTICAL: During an inspection, you find a bathroom light fitting 200mm from the shower head. The fitting is IPX4 rated. Is this compliant?",
        "options": json.dumps(["No, needs IPX5 and must be 600mm away", "Yes, IPX4 is adequate", "No, needs IPX7", "Yes, but only with RCD protection"]),
        "correct_answer": "No, needs IPX5 and must be 600mm away",
        "explanation": "Within 600mm of a shower head is Zone 1 which requires IPX5 minimum, and the fitting should be outside the spray zone.",
        "regulation_reference": "BS 7671 Section 701, Fig 701.1",
        "practical_tip": "Always refer to bathroom zone diagrams. Zone 1 extends 600mm from shower head and 2.25m high.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "medium",
        "question_text": "PRACTICAL: A kitchen ring circuit keeps tripping the 32A MCB when the kettle and toaster are used together. What is the most likely cause?",
        "options": json.dumps(["Overload - both appliances exceed 32A combined", "Earth fault", "Short circuit", "Loose connection"]),
        "correct_answer": "Overload - both appliances exceed 32A combined",
        "explanation": "A kettle (13A) + toaster (10A) = 23A which is within limits. But if other appliances are also running, total can exceed 32A causing overload trip.",
        "regulation_reference": "BS 7671 433.1",
        "practical_tip": "Calculate total load before adding appliances. Consider splitting high-load appliances across different circuits.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "easy",
        "question_text": "PRACTICAL: You notice a client's consumer unit is made of wood. What action should you take?",
        "options": json.dumps(["Recommend immediate replacement with non-combustible unit", "Leave it - it's still functional", "Paint it with fire-resistant paint", "Install smoke detector nearby"]),
        "correct_answer": "Recommend immediate replacement with non-combustible unit",
        "explanation": "Wooden consumer units are a fire risk and do not comply with current regulations requiring non-combustible enclosures.",
        "regulation_reference": "BS 7671 421.1.201",
        "practical_tip": "Document this as a C2 (potentially dangerous) observation in your EICR and strongly advise replacement.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "hard",
        "question_text": "PRACTICAL: A client has a TT system with an earth electrode reading 200Ω. What RCD rating would make this installation safe?",
        "options": json.dumps(["100mA RCD at the origin", "30mA RCD on all circuits", "300mA RCD", "No RCD needed"]),
        "correct_answer": "30mA RCD on all circuits",
        "explanation": "For a TT system with high Ra, 30mA RCDs provide protection. Ra × IΔn ≤ 50V, so 200Ω × 0.03A = 6V which is well below 50V.",
        "regulation_reference": "BS 7671 411.5.3",
        "calculation_steps": "1. Required: Ra × IΔn ≤ 50V\n2. With Ra = 200Ω: 200 × 0.03 = 6V\n3. 6V < 50V = Safe\n4. 30mA RCDs required on all circuits",
        "practical_tip": "On TT systems, always install 30mA RCD protection on all final circuits due to typically high earth electrode resistance.",
        "epra_class": "Class B"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "medium",
        "question_text": "PRACTICAL: While working on a lighting circuit, you receive a minor electric shock. The circuit was supposedly isolated. What went wrong?",
        "options": json.dumps(["Shared neutral with another circuit", "Circuit not properly isolated", "Capacitive discharge", "Induced voltage from parallel cable"]),
        "correct_answer": "Shared neutral with another circuit",
        "explanation": "A borrowed or shared neutral can remain live even when the circuit MCB is off because current flows through the other circuit.",
        "regulation_reference": "BS 7671 314.4",
        "practical_tip": "Always test for voltage after isolation. Shared neutrals are dangerous and should be corrected when found.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "medium",
        "question_text": "PRACTICAL: An outdoor socket with IP66 rating has been installed but water still enters. What is the likely cause?",
        "options": json.dumps(["Cable entry not sealed - gland not tightened", "IP66 insufficient for outdoor use", "Wrong voltage rating", "Socket mounted upside down"]),
        "correct_answer": "Cable entry not sealed - gland not tightened",
        "explanation": "IP66 rating is adequate for outdoor use but cable entries must be properly sealed with compression glands to maintain the IP rating.",
        "regulation_reference": "BS 7671 522.8.1",
        "practical_tip": "Always use appropriate cable glands for outdoor installations. Silicone sealant can provide additional protection at entry points.",
        "epra_class": "Class C"
    },
    {
        "category": "Safety Regulations",
        "difficulty": "hard",
        "question_text": "PRACTICAL: You measure 0.8Ω Zs on a 32A Type B MCB circuit. The maximum permitted is 1.44Ω. Is this acceptable?",
        "options": json.dumps(["Yes - 0.8Ω is below maximum permitted", "No - must be exactly 1.44Ω", "No - too low means short circuit", "Yes but only with RCD"]),
        "correct_answer": "Yes - 0.8Ω is below maximum permitted",
        "explanation": "Zs must be LESS than the maximum permitted value. 0.8Ω < 1.44Ω so this installation is safe and compliant.",
        "regulation_reference": "BS 7671 Table 41.3",
        "practical_tip": "Lower Zs is always better. The maximum value is the upper limit - anything below it is acceptable and safer.",
        "epra_class": "Class C"
    },

    # ========================
    # CABLE CALCULATIONS (12 Theory + 8 Practical = 20)
    # ========================
    
    # Theory Questions
    {
        "category": "Cable Calculations",
        "difficulty": "hard",
        "question_text": "Calculate the voltage drop for a 2.5mm² copper cable carrying 20A over 30m. (mV/A/m = 18). Is this acceptable for a lighting circuit?",
        "options": json.dumps(["10.8V (4.7%) - Not acceptable for lighting", "8.6V (3.7%) - Acceptable", "5.4V (2.3%) - Acceptable", "12.4V (5.4%) - Not acceptable"]),
        "correct_answer": "10.8V (4.7%) - Not acceptable for lighting",
        "explanation": "Vd = (18 × 20 × 30) / 1000 = 10.8V. As percentage: (10.8/230) × 100 = 4.7%. Lighting circuits have 3% maximum voltage drop.",
        "regulation_reference": "BS 7671 Appendix 4",
        "calculation_steps": "1. Vd = (mV/A/m × I × L) / 1000\n2. Vd = (18 × 20 × 30) / 1000\n3. Vd = 10.8V\n4. % = (10.8/230) × 100 = 4.7%\n5. Compare to 3% limit → Exceeds",
        "practical_tip": "For lighting circuits, aim for 3% or less. For power circuits, 5% is acceptable. Always calculate before installing.",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "medium",
        "question_text": "What is the current-carrying capacity of 2.5mm² PVC twin and earth cable clipped direct?",
        "options": json.dumps(["27A", "20A", "32A", "24A"]),
        "correct_answer": "27A",
        "explanation": "According to BS 7671 Table 4D5, 2.5mm² PVC twin and earth cable clipped direct has a rating of 27A (reference method C).",
        "regulation_reference": "BS 7671 Table 4D5",
        "practical_tip": "Remember: Clipped direct (Method C) gives highest rating. In conduit (Method B) or insulation (Method 101), rating decreases significantly.",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "hard",
        "question_text": "A 10kW shower at 240V needs a cable run of 25m. What is the minimum cable size if mV/A/m for 10mm² is 4.4?",
        "options": json.dumps(["10mm²", "6mm²", "16mm²", "4mm²"]),
        "correct_answer": "10mm²",
        "explanation": "Current = 10000/240 = 41.7A. Vd = (4.4 × 41.7 × 25)/1000 = 4.59V. Percentage = (4.59/240)×100 = 1.9%. Within 5% limit.",
        "regulation_reference": "BS 7671 Appendix 4",
        "calculation_steps": "1. Ib = 10000/240 = 41.7A\n2. Vd = (4.4 × 41.7 × 25)/1000 = 4.59V\n3. % = (4.59/240)×100 = 1.9%\n4. 1.9% < 5% limit ✓\n5. 10mm² cable is adequate",
        "practical_tip": "For showers, always allow for future upgrade. Consider using 16mm² to allow for larger shower installation later.",
        "epra_class": "Class B"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "easy",
        "question_text": "What does mV/A/m represent in cable calculations?",
        "options": json.dumps(["Millivolt drop per amp per meter", "Maximum voltage per amp per meter", "Minimum volt per application per meter", "Millivolt ampere per meter"]),
        "correct_answer": "Millivolt drop per amp per meter",
        "explanation": "mV/A/m is the voltage drop in millivolts for a cable carrying 1 amp over 1 meter. It's used in voltage drop calculations.",
        "regulation_reference": "BS 7671 Appendix 4",
        "practical_tip": "The mV/A/m value changes with cable size - larger cables have smaller values (less voltage drop).",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "medium",
        "question_text": "What is the maximum permitted voltage drop for a lighting circuit as a percentage of supply voltage?",
        "options": json.dumps(["3%", "5%", "4%", "2%"]),
        "correct_answer": "3%",
        "explanation": "BS 7671 specifies maximum voltage drop of 3% for lighting circuits and 5% for other circuits from the origin of the installation.",
        "regulation_reference": "BS 7671 525.1",
        "practical_tip": "Lighting circuits are more sensitive to voltage drop because light output decreases noticeably with lower voltage.",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "hard",
        "question_text": "Calculate the design current for a 3-phase 15kW motor at 415V with power factor 0.85.",
        "options": json.dumps(["24.6A", "36.1A", "20.9A", "42.4A"]),
        "correct_answer": "24.6A",
        "explanation": "For 3-phase: I = P/(√3 × V × pf) = 15000/(1.732 × 415 × 0.85) = 15000/610.6 = 24.6A",
        "regulation_reference": "BS 7671 Appendix 4",
        "calculation_steps": "1. I = P / (√3 × V × pf)\n2. I = 15000 / (1.732 × 415 × 0.85)\n3. I = 15000 / 610.6\n4. I = 24.6A",
        "practical_tip": "For motors, always add 25% for starting current when sizing cables and protection devices.",
        "epra_class": "Class B"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "medium",
        "question_text": "What correction factor would you apply for a cable installed in an ambient temperature of 35°C?",
        "options": json.dumps(["0.94 for PVC", "1.06 for PVC", "0.87 for PVC", "1.0 for PVC"]),
        "correct_answer": "0.94 for PVC",
        "explanation": "For PVC cables at 35°C, the correction factor is 0.94 according to BS 7671 Table 4B1. The standard reference temperature is 30°C.",
        "regulation_reference": "BS 7671 Table 4B1",
        "practical_tip": "In hot environments like boiler rooms or roof spaces, always apply temperature correction factors.",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "hard",
        "question_text": "A 6mm² cable has a voltage drop of 7.3 mV/A/m. What voltage drop would result from a 40A load over 50m?",
        "options": json.dumps(["14.6V", "7.3V", "29.2V", "3.65V"]),
        "correct_answer": "14.6V",
        "explanation": "Vd = (7.3 × 40 × 50)/1000 = 14.6V. Percentage = (14.6/230)×100 = 6.3% - exceeds 5% limit for power circuits.",
        "regulation_reference": "BS 7671 Appendix 4",
        "calculation_steps": "1. Vd = (mV/A/m × I × L) / 1000\n2. Vd = (7.3 × 40 × 50) / 1000\n3. Vd = 14.6V\n4. % = (14.6/230) × 100 = 6.3%\n5. Exceeds 5% limit - use larger cable",
        "practical_tip": "If voltage drop exceeds 5%, go up one cable size and recalculate.",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "easy",
        "question_text": "What is the standard reference method for cables clipped directly to a wall?",
        "options": json.dumps(["Method C", "Method A", "Method B", "Method 101"]),
        "correct_answer": "Method C",
        "explanation": "Method C is the reference method for cables clipped direct to a surface or on cable trays, providing the highest current-carrying capacity.",
        "regulation_reference": "BS 7671 Table 4A2",
        "practical_tip": "Method C gives the highest current ratings. Any other installation method will require derating factors.",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "medium",
        "question_text": "What is the minimum cable size for a 32A radial circuit using PVC cable clipped direct?",
        "options": json.dumps(["4mm²", "2.5mm²", "6mm²", "10mm²"]),
        "correct_answer": "4mm²",
        "explanation": "4mm² PVC cable clipped direct (Method C) has a current rating of 37A, which is above the 32A circuit requirement. 2.5mm² (27A) would be too small.",
        "regulation_reference": "BS 7671 Table 4D5",
        "practical_tip": "For 32A radial circuits, use minimum 4mm² cable. 2.5mm² is only suitable for 20A radials or ring circuits.",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "hard",
        "question_text": "Calculate the total voltage drop from origin to a distribution board 40m away using 16mm² cable carrying 60A (mV/A/m = 2.8), then 20m to load using 2.5mm² carrying 20A (mV/A/m = 18).",
        "options": json.dumps(["13.92V total (6.1%)", "6.72V total (2.9%)", "20.64V total (9.0%)", "10.32V total (4.5%)"]),
        "correct_answer": "13.92V total (6.1%)",
        "explanation": "Distribution: (2.8×60×40)/1000 = 6.72V. Final: (18×20×20)/1000 = 7.2V. Total = 13.92V. % = (13.92/230)×100 = 6.1%",
        "regulation_reference": "BS 7671 Appendix 4, 525.1",
        "calculation_steps": "1. Dist: Vd1 = (2.8 × 60 × 40) / 1000 = 6.72V\n2. Final: Vd2 = (18 × 20 × 20) / 1000 = 7.2V\n3. Total Vd = 6.72 + 7.2 = 13.92V\n4. % = (13.92/230) × 100 = 6.1%",
        "practical_tip": "Always sum voltage drops from origin to the furthest point. Sub-main and final circuit drops are cumulative.",
        "epra_class": "Class B"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "easy",
        "question_text": "What does the abbreviation 'Iz' represent in cable calculations?",
        "options": json.dumps(["Current-carrying capacity of the cable", "Design current", "Short circuit current", "Protective device rating"]),
        "correct_answer": "Current-carrying capacity of the cable",
        "explanation": "Iz is the current-carrying capacity of a cable under defined installation conditions, taking into account all correction factors.",
        "regulation_reference": "BS 7671 Part 2 Definitions",
        "practical_tip": "Remember: Ib ≤ In ≤ Iz (Design current ≤ MCB rating ≤ Cable capacity after correction factors).",
        "epra_class": "Class C"
    },


    # ========================
    # CABLE CALCULATIONS - Practical Scenarios (8)
    # ========================
    
    {
        "category": "Cable Calculations",
        "difficulty": "hard",
        "question_text": "PRACTICAL: You are installing a 7.2kW cooker on a 30m cable run. The cable is in conduit (Method B). What minimum cable size is needed? (Use 6mm² mV/A/m=7.3, 10mm² mV/A/m=4.4)",
        "options": json.dumps(["10mm² - voltage drop 4.62V (2.0%)", "6mm² - voltage drop 7.67V (3.3%)", "16mm² - voltage drop 2.9V (1.3%)", "4mm² - voltage drop 12V (5.2%)"]),
        "correct_answer": "10mm² - voltage drop 4.62V (2.0%)",
        "explanation": "Current = 7200/240 = 30A. For 6mm²: Vd = (7.3×30×30)/1000 = 6.57V (2.9%). For 10mm²: Vd = (4.4×30×30)/1000 = 3.96V (1.7%). 10mm² is appropriate for Method B.",
        "regulation_reference": "BS 7671 Table 4D2A, Appendix 4",
        "calculation_steps": "1. Ib = 7200/240 = 30A\n2. 6mm² Vd = (7.3×30×30)/1000 = 6.57V\n3. 10mm² Vd = (4.4×30×30)/1000 = 3.96V\n4. Method B derating: check Table 4D2A\n5. 10mm² selected",
        "practical_tip": "Cookers with ovens and hobs can draw high currents. Consider diversity in calculations.",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "medium",
        "question_text": "PRACTICAL: A garden shed 40m from the house needs a 16A supply. Using SWA cable buried underground, what size cable would you install?",
        "options": json.dumps(["2.5mm² SWA (check volt drop)", "1.5mm² SWA", "4mm² SWA", "6mm² SWA"]),
        "correct_answer": "2.5mm² SWA (check volt drop)",
        "explanation": "2.5mm² SWA buried has rating of ~29A (Method D). 16A load is within capacity. Check voltage drop: (18×16×40)/1000 = 11.52V (5.0%) - borderline, consider 4mm².",
        "regulation_reference": "BS 7671 Table 4D4A",
        "practical_tip": "For long garden runs, voltage drop often determines cable size more than current rating. Always calculate both.",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "hard",
        "question_text": "PRACTICAL: A 3-phase distribution circuit supplies a workshop 80m away. The load is 40A per phase. What minimum cable size using SWA on tray? (mV/A/m: 10mm²=4.4, 16mm²=2.8, 25mm²=1.75)",
        "options": json.dumps(["16mm² - voltage drop 8.96V (2.2%)", "10mm² - voltage drop 14.08V (3.4%)", "25mm² - voltage drop 5.6V (1.4%)", "6mm² - voltage drop 23.4V (5.6%)"]),
        "correct_answer": "16mm² - voltage drop 8.96V (2.2%)",
        "explanation": "Vd = (2.8×40×80)/1000 = 8.96V. Percentage = (8.96/400)×100 = 2.2%. Well within 5% limit for distribution.",
        "regulation_reference": "BS 7671 Appendix 4",
        "calculation_steps": "1. Try 10mm²: (4.4×40×80)/1000 = 14.08V = 3.4%\n2. Try 16mm²: (2.8×40×80)/1000 = 8.96V = 2.2%\n3. 16mm² meets criteria\n4. Check current rating for installation method",
        "practical_tip": "For 3-phase circuits, use 400V for voltage drop percentage calculation, not 230V.",
        "epra_class": "Class B"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "medium",
        "question_text": "PRACTICAL: You have 4 cables bunched together in conduit. How does this affect the current-carrying capacity?",
        "options": json.dumps(["Apply grouping factor of 0.8 (reduces capacity by 20%)", "No effect - conduit protects cables", "Capacity increases due to mutual heating", "Apply factor of 1.2"]),
        "correct_answer": "Apply grouping factor of 0.8 (reduces capacity by 20%)",
        "explanation": "When cables are grouped, mutual heating reduces heat dissipation. BS 7671 Table 4C1 gives a grouping factor of 0.8 for 4 circuits.",
        "regulation_reference": "BS 7671 Table 4C1",
        "practical_tip": "Grouping factors significantly reduce cable capacity. When possible, space cables apart or use larger conduit.",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "hard",
        "question_text": "PRACTICAL: A 12kW 3-phase motor at 415V, pf 0.85, efficiency 90%, starting current 6x full load. What cable size for Method C installation 25m run?",
        "options": json.dumps(["4mm² - check volt drop for starting", "6mm²", "2.5mm²", "10mm²"]),
        "correct_answer": "4mm² - check volt drop for starting",
        "explanation": "FL current = 12000/(1.732×415×0.85×0.9) = 21.9A. Starting = 131.4A briefly. 4mm² rated 37A Method C. Voltage drop at starting must be checked.",
        "regulation_reference": "BS 7671 433.1, Appendix 4",
        "calculation_steps": "1. Ifl = P/(√3×V×pf×eff)\n2. Ifl = 12000/(1.732×415×0.85×0.9) = 21.9A\n3. Istart = 21.9 × 6 = 131.4A\n4. Cable must handle starting current momentarily",
        "practical_tip": "Motor starting currents are 6-8 times full load current. MCBs must be Type C or D to avoid nuisance tripping.",
        "epra_class": "Class B"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "medium",
        "question_text": "PRACTICAL: You discover a 2.5mm² cable supplying a 32A socket radial. The cable is in thermal insulation (Method 101). Is this safe?",
        "options": json.dumps(["No - cable rated only 13.5A in insulation", "Yes - 2.5mm² handles 32A", "Yes if RCD protected", "Only if cable is derated by 50%"]),
        "correct_answer": "No - cable rated only 13.5A in insulation",
        "explanation": "2.5mm² in thermal insulation (Method 101) has a rating of only 13.5A. This cable is severely undersized and dangerous.",
        "regulation_reference": "BS 7671 Table 4D5",
        "practical_tip": "Cables in insulation can have their capacity reduced by over 50%. Always consider installation method.",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "easy",
        "question_text": "PRACTICAL: What is the voltage drop for a 1.5mm² lighting circuit carrying 6A over 20m? (mV/A/m = 29)",
        "options": json.dumps(["3.48V (1.5%)", "1.74V (0.8%)", "6.96V (3.0%)", "0.87V (0.4%)"]),
        "correct_answer": "3.48V (1.5%)",
        "explanation": "Vd = (29 × 6 × 20) / 1000 = 3.48V. Percentage = (3.48/230)×100 = 1.5%. Well within 3% limit for lighting.",
        "regulation_reference": "BS 7671 Appendix 4",
        "calculation_steps": "1. Vd = (29 × 6 × 20) / 1000\n2. Vd = 3480/1000\n3. Vd = 3.48V\n4. % = (3.48/230) × 100 = 1.5%",
        "practical_tip": "1.5mm² is standard for domestic lighting. Voltage drop rarely an issue on short runs.",
        "epra_class": "Class C"
    },
    {
        "category": "Cable Calculations",
        "difficulty": "hard",
        "question_text": "PRACTICAL: A sub-main cable feeds a consumer unit 50m away. The maximum demand is 80A single phase. Cable is 25mm² with mV/A/m = 1.75. What is the voltage drop and is a 16mm² (mV/A/m=2.8) adequate?",
        "options": json.dumps(["25mm²: 7V (3.0%), 16mm²: 11.2V (4.9%). Use 25mm²", "Both are fine", "16mm² is better", "Need 35mm²"]),
        "correct_answer": "25mm²: 7V (3.0%), 16mm²: 11.2V (4.9%). Use 25mm²",
        "explanation": "For 25mm²: Vd = (1.75×80×50)/1000 = 7V (3.0%). For 16mm²: Vd = (2.8×80×50)/1000 = 11.2V (4.9%). 16mm² is borderline, 25mm² is safer.",
        "regulation_reference": "BS 7671 525.1",
        "calculation_steps": "1. 25mm²: (1.75×80×50)/1000 = 7V = 3.0%\n2. 16mm²: (2.8×80×50)/1000 = 11.2V = 4.9%\n3. Both under 5% for distribution\n4. 25mm² recommended for future proofing",
        "practical_tip": "For sub-mains, always oversize slightly for future load increases. The cost difference is minimal compared to rewiring later.",
        "epra_class": "Class B"
    },

    # ========================
    # EARTHING & BONDING (10 Theory + 6 Practical = 16)
    # ========================
    
    # Theory Questions
    {
        "category": "Earthing & Bonding",
        "difficulty": "hard",
        "question_text": "What is the maximum earth fault loop impedance (Zs) for a 32A Type B MCB on a TN system at 230V?",
        "options": json.dumps(["1.44Ω", "1.15Ω", "0.72Ω", "2.30Ω"]),
        "correct_answer": "1.44Ω",
        "explanation": "Using the formula: Zs = Uo/(In×5) for Type B MCBs. Zs = 230/(32×5) = 1.44Ω. This ensures the MCB trips within 0.4 seconds.",
        "regulation_reference": "BS 7671 Table 41.3",
        "calculation_steps": "1. Type B multiplier = 5\n2. Zs = 230 / (32 × 5)\n3. Zs = 230 / 160\n4. Zs = 1.44Ω",
        "practical_tip": "Always measure Zs at the furthest point of the circuit. If Zs > 1.15Ω, investigate the earthing arrangement.",
        "epra_class": "Class C"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "medium",
        "question_text": "What is the purpose of main protective bonding conductors?",
        "options": json.dumps(["To connect extraneous conductive parts to the main earthing terminal", "To carry fault current to earth", "To protect against overload", "To provide a neutral connection"]),
        "correct_answer": "To connect extraneous conductive parts to the main earthing terminal",
        "explanation": "Main protective bonding connects incoming metal services (water, gas, oil) to the main earthing terminal to prevent dangerous potential differences.",
        "regulation_reference": "BS 7671 544.1",
        "practical_tip": "Bonding must be within 600mm of service entry point before any branch pipework. Use approved bonding clamps.",
        "epra_class": "Class C"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "easy",
        "question_text": "What color is the earth conductor in a NEW installation?",
        "options": json.dumps(["Green/Yellow", "Green", "Yellow", "Black"]),
        "correct_answer": "Green/Yellow",
        "explanation": "The harmonized color for earth/CPC conductors is green/yellow stripe. This applies to all new installations.",
        "regulation_reference": "BS 7671 Appendix 7",
        "practical_tip": "Never use green/yellow conductors for any purpose other than earthing. It's dangerous and non-compliant.",
        "epra_class": "Class C"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "hard",
        "question_text": "What is the maximum resistance of an earth electrode for a TT system?",
        "options": json.dumps(["200Ω (with 30mA RCD)", "100Ω", "500Ω", "50Ω"]),
        "correct_answer": "200Ω (with 30mA RCD)",
        "explanation": "For TT systems: Ra × IΔn ≤ 50V. With 30mA RCD: Ra = 50/0.03 = 1667Ω. Practical maximum is 200Ω to allow for soil condition changes.",
        "regulation_reference": "BS 7671 411.5.3",
        "calculation_steps": "1. Ra × IΔn ≤ 50V\n2. With IΔn = 0.03A: Ra ≤ 50/0.03\n3. Ra ≤ 1667Ω theoretically\n4. Practically: Ra ≤ 200Ω recommended",
        "practical_tip": "Install multiple earth rods if needed to achieve acceptable resistance. Space rods at least their length apart.",
        "epra_class": "Class B"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "medium",
        "question_text": "What is supplementary bonding?",
        "options": json.dumps(["Additional bonding between simultaneously accessible conductive parts", "Bonding at the origin of the installation", "Bonding to the earth electrode", "Bonding of the neutral conductor"]),
        "correct_answer": "Additional bonding between simultaneously accessible conductive parts",
        "explanation": "Supplementary bonding connects together all simultaneously accessible exposed and extraneous conductive parts to reduce touch voltage below 50V.",
        "regulation_reference": "BS 7671 415.2",
        "practical_tip": "Required in locations containing a bath or shower. Use 4mm² minimum copper conductor.",
        "epra_class": "Class C"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "hard",
        "question_text": "Calculate the minimum size of a main protective bonding conductor for a TN-S system with 25mm² line conductor.",
        "options": json.dumps(["10mm²", "16mm²", "6mm²", "25mm²"]),
        "correct_answer": "10mm²",
        "explanation": "For TN-S: bonding conductor ≥ half the main earthing conductor. Earthing conductor from Table 54.7 for 25mm² line is 16mm². Half of 16mm² = 8mm², minimum 10mm².",
        "regulation_reference": "BS 7671 544.1, Table 54.8",
        "practical_tip": "Never use less than 6mm² for main bonding. 10mm² is standard for most domestic installations.",
        "epra_class": "Class B"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "medium",
        "question_text": "What is the difference between earthing and bonding?",
        "options": json.dumps(["Earthing connects to earth, bonding connects conductive parts together", "They are the same thing", "Bonding is for TT systems only", "Earthing is for TN systems only"]),
        "correct_answer": "Earthing connects to earth, bonding connects conductive parts together",
        "explanation": "Earthing provides a path to earth for fault currents. Bonding connects conductive parts together to maintain equal potential and prevent dangerous voltage differences.",
        "regulation_reference": "BS 7671 Part 2 Definitions",
        "practical_tip": "Earthing = connection to earth. Bonding = connection between parts. Both essential for safety.",
        "epra_class": "Class C"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "easy",
        "question_text": "What is the minimum cross-sectional area of a circuit protective conductor (CPC) for a 2.5mm² line conductor?",
        "options": json.dumps(["1.5mm²", "2.5mm²", "1.0mm²", "4.0mm²"]),
        "correct_answer": "1.5mm²",
        "explanation": "For line conductors up to 16mm², the CPC must be the same size as the line conductor if not calculated separately. However, standard twin and earth cable includes a 1.5mm² CPC with 2.5mm² line.",
        "regulation_reference": "BS 7671 Table 54.7",
        "practical_tip": "Standard 2.5mm² twin & earth cable has a 1.5mm² CPC. For separate CPC, calculate using the adiabatic equation.",
        "epra_class": "Class C"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "hard",
        "question_text": "Using the adiabatic equation S = √(I²t)/k, calculate minimum CPC size for a fault current of 1600A, disconnection time 0.1s, k=115 for copper.",
        "options": json.dumps(["4.4mm² (select 6mm²)", "2.2mm² (select 2.5mm²)", "6.6mm² (select 10mm²)", "1.1mm² (select 1.5mm²)"]),
        "correct_answer": "4.4mm² (select 6mm²)",
        "explanation": "S = √(1600² × 0.1)/115 = √(256000)/115 = 506/115 = 4.4mm². Round up to next standard size: 6mm².",
        "regulation_reference": "BS 7671 543.1.3",
        "calculation_steps": "1. S = √(I² × t) / k\n2. S = √(1600² × 0.1) / 115\n3. S = √(2,560,000 × 0.1) / 115\n4. S = √256,000 / 115\n5. S = 506 / 115 = 4.4mm² → 6mm²",
        "practical_tip": "The adiabatic equation often allows smaller CPCs than the rule-of-thumb method. Always calculate for economy.",
        "epra_class": "Class B"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "medium",
        "question_text": "Which earthing system uses the supply cable sheath as the earth path?",
        "options": json.dumps(["TN-S", "TN-C-S (PME)", "TT", "IT"]),
        "correct_answer": "TN-S",
        "explanation": "TN-S (Terra Neutral - Separate) uses a separate earth conductor throughout the system, often the metallic sheath of the supply cable.",
        "regulation_reference": "BS 7671 312.1",
        "practical_tip": "TN-S is common in older installations with lead-sheathed cables. Modern installations often use TN-C-S (PME).",
        "epra_class": "Class C"
    },
    
    # Practical Scenario Questions
    {
        "category": "Earthing & Bonding",
        "difficulty": "hard",
        "question_text": "PRACTICAL: You measure Zs at a socket outlet and get 1.8Ω on a 32A Type B MCB circuit (max 1.44Ω). What action should you take?",
        "options": json.dumps(["Investigate earthing - Zs too high, circuit unsafe", "Record it as acceptable", "Install an RCD", "Change to Type C MCB"]),
        "correct_answer": "Investigate earthing - Zs too high, circuit unsafe",
        "explanation": "1.8Ω exceeds the maximum 1.44Ω for a 32A Type B MCB. The circuit will not disconnect within the required 0.4s. This is a C2 (potentially dangerous) observation.",
        "regulation_reference": "BS 7671 Table 41.3",
        "practical_tip": "Check all connections in the earth path: MET, earthing conductor, bonding connections. High Zs often caused by loose connections.",
        "epra_class": "Class C"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "medium",
        "question_text": "PRACTICAL: During an EICR, you find no main protective bonding to the incoming gas pipe. The pipe enters the building 2m from the consumer unit. What code?",
        "options": json.dumps(["C2 - Potentially dangerous, bonding required", "C3 - Improvement recommended", "C1 - Danger present", "No code needed"]),
        "correct_answer": "C2 - Potentially dangerous, bonding required",
        "explanation": "Missing main protective bonding is a C2 observation as it could lead to dangerous potential differences under fault conditions.",
        "regulation_reference": "BS 7671 544.1, Electrical Safety First Best Practice Guide",
        "practical_tip": "Always check main bonding as part of any inspection. Use the correct bonding clamp designed for the pipe material.",
        "epra_class": "Class C"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "hard",
        "question_text": "PRACTICAL: A TT installation has an earth electrode resistance of 150Ω. You plan to install a 30mA RCD as main switch. Is this acceptable?",
        "options": json.dumps(["Yes - 150Ω × 0.03A = 4.5V (< 50V limit)", "No - resistance too high", "Yes but only with 100mA RCD", "No - need multiple electrodes"]),
        "correct_answer": "Yes - 150Ω × 0.03A = 4.5V (< 50V limit)",
        "explanation": "Ra × IΔn = 150 × 0.03 = 4.5V which is well below the 50V maximum touch voltage. The installation is safe with 30mA RCD protection.",
        "regulation_reference": "BS 7671 411.5.3",
        "calculation_steps": "1. Touch voltage = Ra × IΔn\n2. = 150 × 0.03\n3. = 4.5V\n4. Compare to 50V limit\n5. 4.5V << 50V = Safe",
        "practical_tip": "TT systems rely on RCDs for earth fault protection. Always ensure the RCD is functioning correctly.",
        "epra_class": "Class B"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "medium",
        "question_text": "PRACTICAL: You need to bond a structural steel column that's 3m from the main earthing terminal. What minimum size bonding conductor?",
        "options": json.dumps(["10mm² copper", "6mm² copper", "16mm² copper", "4mm² copper"]),
        "correct_answer": "10mm² copper",
        "explanation": "Main protective bonding conductors must be minimum 6mm² but not less than half the main earthing conductor. Standard practice is 10mm².",
        "regulation_reference": "BS 7671 544.1.1",
        "practical_tip": "Use bonding clamps designed for structural steel. Paint must be removed to ensure good electrical contact.",
        "epra_class": "Class C"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "easy",
        "question_text": "PRACTICAL: You are replacing a consumer unit. What connection is required for the main earthing terminal?",
        "options": json.dumps(["Connect main earthing conductor, bonding conductors, and CPCs", "Connect only the earth electrode", "Connect only bonding conductors", "No connections needed"]),
        "correct_answer": "Connect main earthing conductor, bonding conductors, and CPCs",
        "explanation": "The main earthing terminal (MET) must connect the main earthing conductor, main protective bonding conductors, and all circuit CPCs.",
        "regulation_reference": "BS 7671 542.4",
        "practical_tip": "Use a proper earth bar in the consumer unit. Ensure all connections are tight and properly torqued.",
        "epra_class": "Class C"
    },
    {
        "category": "Earthing & Bonding",
        "difficulty": "hard",
        "question_text": "PRACTICAL: RCD test at 0° gives 28ms, at 180° gives 35ms. Maximum allowed is 40ms at IΔn. Is this RCD acceptable?",
        "options": json.dumps(["Yes - both readings below 40ms limit", "No - inconsistent readings", "Yes but only at 0°", "No - should be exactly the same"]),
        "correct_answer": "Yes - both readings below 40ms limit",
        "explanation": "Both readings are below the 40ms maximum for 30mA RCDs. Slight variation between 0° and 180° is normal due to the RCD's internal electronics.",
        "regulation_reference": "BS 7671 643.8",
        "practical_tip": "Test RCDs at 0°, 90°, and 180°. All readings should be <40ms at IΔn and <300ms at 0.5 IΔn.",
        "epra_class": "Class C"
    },


    # ========================
    # INSPECTION & TESTING (12 Theory + 8 Practical = 20)
    # ========================
    
    # Theory Questions
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
        "explanation": "The correct testing sequence is CIPELR: Continuity (dead), Insulation Resistance (dead), Polarity (dead), Earth Fault Loop Impedance (live), RCD (live).",
        "regulation_reference": "BS 7671 Part 6",
        "practical_tip": "Remember CIPELR - first 3 are dead tests, last 2 are live tests. Never mix dead and live testing.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "easy",
        "question_text": "What test voltage is used for insulation resistance testing of a 230V circuit?",
        "options": json.dumps(["500V DC", "250V DC", "1000V DC", "230V AC"]),
        "correct_answer": "500V DC",
        "explanation": "For circuits up to 500V, the test voltage for insulation resistance is 500V DC as specified in BS 7671 Table 61.",
        "regulation_reference": "BS 7671 643.3, Table 61",
        "practical_tip": "Ensure all sensitive electronic equipment is disconnected before IR testing to prevent damage.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "hard",
        "question_text": "What is the minimum acceptable insulation resistance for a new 230V domestic circuit?",
        "options": json.dumps(["1 MΩ", "0.5 MΩ", "2 MΩ", "5 MΩ"]),
        "correct_answer": "1 MΩ",
        "explanation": "The minimum insulation resistance for circuits up to 500V is 1 MΩ. Values below this indicate potential insulation breakdown.",
        "regulation_reference": "BS 7671 Table 61",
        "practical_tip": "If IR reading is low, test each section individually to locate the problem. Damp or aging insulation are common causes.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "medium",
        "question_text": "What instrument is used to measure earth fault loop impedance?",
        "options": json.dumps(["Earth fault loop impedance tester", "Multimeter", "Insulation resistance tester", "RCD tester"]),
        "correct_answer": "Earth fault loop impedance tester",
        "explanation": "An earth fault loop impedance tester injects a current and measures the impedance of the entire earth fault loop path.",
        "regulation_reference": "BS 7671 643.7",
        "practical_tip": "Modern loop testers use a no-trip function that prevents RCD tripping during testing.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "hard",
        "question_text": "What is the maximum RCD trip time at rated residual current (IΔn) for a 30mA RCD?",
        "options": json.dumps(["40ms", "300ms", "200ms", "100ms"]),
        "correct_answer": "40ms",
        "explanation": "RCDs must trip within 40ms at IΔn to provide additional protection against electric shock (BS 7671 643.8).",
        "regulation_reference": "BS 7671 643.8",
        "practical_tip": "Test at 0°, 90°, 180° to verify consistent operation. Record the highest reading.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "medium",
        "question_text": "What is the purpose of a polarity test?",
        "options": json.dumps(["To verify that line and neutral are correctly connected", "To measure voltage", "To check earth continuity", "To test RCD operation"]),
        "correct_answer": "To verify that line and neutral are correctly connected",
        "explanation": "Polarity testing ensures that switches and protective devices are connected in the line conductor only, and that socket-outlets are wired correctly.",
        "regulation_reference": "BS 7671 643.6",
        "practical_tip": "Reversed polarity can be fatal - equipment may appear off but still be live. Always test polarity.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "easy",
        "question_text": "What does an RCD ramp test measure?",
        "options": json.dumps(["The actual current at which the RCD trips", "The trip time", "The earth loop impedance", "The insulation resistance"]),
        "correct_answer": "The actual current at which the RCD trips",
        "explanation": "A ramp test gradually increases the test current until the RCD trips, measuring the actual tripping current. It should trip between 15-30mA for a 30mA RCD.",
        "regulation_reference": "BS 7671 643.8",
        "practical_tip": "RCD should trip at 50-100% of rated IΔn. A 30mA RCD should trip between 15-30mA.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "hard",
        "question_text": "What test confirms that all exposed conductive parts are connected to the main earthing terminal?",
        "options": json.dumps(["Continuity of protective conductors test", "Insulation resistance test", "Polarity test", "Functional test"]),
        "correct_answer": "Continuity of protective conductors test",
        "explanation": "This test verifies that all CPCs and bonding conductors are electrically continuous and properly connected to the MET.",
        "regulation_reference": "BS 7671 643.4",
        "practical_tip": "Use a low-resistance ohmmeter with a test current of at least 200mA for accurate continuity testing.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "medium",
        "question_text": "What is a prospective fault current (PFC) test?",
        "options": json.dumps(["Measures the maximum current that could flow under short circuit conditions", "Tests RCD operation", "Measures insulation resistance", "Tests circuit continuity"]),
        "correct_answer": "Measures the maximum current that could flow under short circuit conditions",
        "explanation": "PFC testing determines the maximum prospective short circuit current (PSCC) and earth fault current to ensure protective devices can safely interrupt them.",
        "regulation_reference": "BS 7671 643.7",
        "practical_tip": "Record the higher of PSCC and PEFC as the PFC. Verify that all protective devices have adequate breaking capacity.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "hard",
        "question_text": "When performing an RCD test at 0.5 IΔn, what is the maximum acceptable trip time?",
        "options": json.dumps(["300ms", "40ms", "200ms", "500ms"]),
        "correct_answer": "300ms",
        "explanation": "At half rated current (0.5 IΔn), the RCD should NOT trip within 300ms. This ensures it won't nuisance trip on normal leakage currents.",
        "regulation_reference": "BS 7671 643.8",
        "practical_tip": "At 0.5 IΔn the RCD should NOT trip. At IΔn (×1) it must trip within 40ms. At ×5 it must trip within 40ms.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "easy",
        "question_text": "What does an EICR stand for?",
        "options": json.dumps(["Electrical Installation Condition Report", "Electrical Inspection Certificate Report", "Energy Installation Check Record", "Electrical Installation Compliance Register"]),
        "correct_answer": "Electrical Installation Condition Report",
        "explanation": "An EICR is a formal document that assesses the condition of an existing electrical installation against current safety standards.",
        "regulation_reference": "BS 7671 Part 6",
        "practical_tip": "EICRs should be carried out every 5-10 years for domestic, 5 years for commercial, and 3 years for industrial installations.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "medium",
        "question_text": "Which test uses a test current of 200mA minimum?",
        "options": json.dumps(["Continuity of protective conductors", "Insulation resistance", "Polarity", "Earth loop impedance"]),
        "correct_answer": "Continuity of protective conductors",
        "explanation": "BS 7671 requires a test current of at least 200mA for continuity testing to ensure reliable measurement of low resistance connections.",
        "regulation_reference": "BS 7671 643.4",
        "practical_tip": "A standard multimeter may not provide enough current. Use a dedicated low-resistance ohmmeter.",
        "epra_class": "Class C"
    },
    
    # Practical Scenario Questions
    {
        "category": "Inspection & Testing",
        "difficulty": "hard",
        "question_text": "PRACTICAL: During an EICR, you find a socket with L-N reversed. The client refuses to allow you to fix it. What EICR code do you assign?",
        "options": json.dumps(["C1 - Danger present, immediate action required", "C2 - Potentially dangerous", "C3 - Improvement recommended", "FI - Further investigation"]),
        "correct_answer": "C1 - Danger present, immediate action required",
        "explanation": "Reversed polarity means the switch only disconnects neutral, leaving the appliance live even when switched off. This is immediately dangerous.",
        "regulation_reference": "Electrical Safety First Best Practice Guide",
        "practical_tip": "C1 requires immediate action. If client refuses, you must report it and note the refusal on the EICR.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "medium",
        "question_text": "PRACTICAL: You measure insulation resistance of a lighting circuit at 0.8 MΩ. The minimum is 1 MΩ. What should you do?",
        "options": json.dumps(["Investigate further - test each section individually", "Pass it - close enough", "Replace all cables", "Increase test voltage to 1000V"]),
        "correct_answer": "Investigate further - test each section individually",
        "explanation": "0.8 MΩ is below the 1 MΩ minimum. The circuit fails IR test. Systematically test each section to locate the low insulation.",
        "regulation_reference": "BS 7671 Table 61",
        "practical_tip": "Disconnect loads and test wiring only. Damp in fittings, trapped cables, or degraded insulation are common causes.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "hard",
        "question_text": "PRACTICAL: RCD trip time at IΔn = 45ms (max 40ms). At 5× IΔn = 38ms. Is this RCD acceptable?",
        "options": json.dumps(["No - fails at IΔn (exceeds 40ms)", "Yes - 5× test passes", "Yes - within tolerance", "Retest once more"]),
        "correct_answer": "No - fails at IΔn (exceeds 40ms)",
        "explanation": "The RCD must trip within 40ms at IΔn. 45ms exceeds this limit. Even though the 5× test passes, the RCD fails and must be replaced.",
        "regulation_reference": "BS 7671 643.8",
        "practical_tip": "A slow RCD could indicate mechanical wear or contamination. Replace the RCD and retest.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "medium",
        "question_text": "PRACTICAL: You are testing a ring final circuit. The r1 reading is 0.4Ω. What should r2 (CPC) approximately measure?",
        "options": json.dumps(["0.67Ω (1.67 × r1 for 2.5/1.5mm² cable)", "0.4Ω (same as r1)", "0.2Ω (half of r1)", "1.0Ω"]),
        "correct_answer": "0.67Ω (1.67 × r1 for 2.5/1.5mm² cable)",
        "explanation": "For 2.5mm² line and 1.5mm² CPC, the ratio is 1.67. So r2 should be approximately r1 × 1.67 = 0.4 × 1.67 = 0.67Ω.",
        "regulation_reference": "BS 7671 Guidance Note 3",
        "calculation_steps": "1. Ratio = Line CSA / CPC CSA = 2.5/1.5 = 1.67\n2. Expected r2 = r1 × 1.67\n3. r2 = 0.4 × 1.67 = 0.67Ω",
        "practical_tip": "r1 and r2 measurements help verify ring continuity. Large deviations indicate a broken ring or loose connections.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "hard",
        "question_text": "PRACTICAL: During initial verification, you measure Zs = 1.2Ω on a 32A Type B MCB (max 1.44Ω). The circuit has a 30mA RCD. Is this acceptable?",
        "options": json.dumps(["Yes - 1.2Ω < 1.44Ω maximum, RCD provides additional protection", "No - Zs too close to maximum", "Yes but only with 100mA RCD", "No - RCD doesn't compensate for high Zs"]),
        "correct_answer": "Yes - 1.2Ω < 1.44Ω maximum, RCD provides additional protection",
        "explanation": "1.2Ω is below the 1.44Ω maximum for a 32A Type B MCB. The RCD provides additional earth fault protection. This is fully compliant.",
        "regulation_reference": "BS 7671 Table 41.3, 411.3.3",
        "practical_tip": "Zs within limits + RCD = fully compliant. The RCD is additional protection, not a substitute for meeting Zs requirements.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "medium",
        "question_text": "PRACTICAL: When testing a ring final circuit, you get r1=0.32Ω, rn=0.32Ω, r2=0.54Ω. Is the ring continuous?",
        "options": json.dumps(["Yes - r1≈rn and r2 is correct ratio", "No - r1 and rn should differ", "No - r2 should be smaller", "Cannot determine"]),
        "correct_answer": "Yes - r1≈rn and r2 is correct ratio",
        "explanation": "r1 and rn should be equal (same length, same CSA). r2/r1 ratio = 0.54/0.32 = 1.69 ≈ 1.67 (theoretical). Ring is continuous and correct.",
        "regulation_reference": "BS 7671 Guidance Note 3",
        "calculation_steps": "1. r1 = rn = 0.32Ω ✓\n2. Ratio r2/r1 = 0.54/0.32 = 1.69\n3. Expected ratio = 2.5/1.5 = 1.67\n4. 1.69 ≈ 1.67 ✓",
        "practical_tip": "Step 1: Ring continuity test verifies no breaks. Step 2: Cross-connect test verifies correct connections.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "easy",
        "question_text": "PRACTICAL: You perform an RCD test and the RCD trips but takes 50ms at IΔn. The client wants to know if this is safe. What do you tell them?",
        "options": json.dumps(["No - the RCD is too slow and needs replacing", "Yes - 50ms is acceptable", "It's borderline but acceptable", "Test again in 6 months"]),
        "correct_answer": "No - the RCD is too slow and needs replacing",
        "explanation": "50ms exceeds the 40ms maximum for RCDs at rated current. The RCD cannot guarantee shock protection within the required time. Replacement is necessary.",
        "regulation_reference": "BS 7671 643.8",
        "practical_tip": "Explain to the client that a slow RCD is a safety risk. Quote for replacement and explain the protection it provides.",
        "epra_class": "Class C"
    },
    {
        "category": "Inspection & Testing",
        "difficulty": "hard",
        "question_text": "PRACTICAL: Ze measured at origin is 0.35Ω (TN-C-S system, max 0.35Ω). Is this acceptable and what does it indicate?",
        "options": json.dumps(["Borderline - exactly at maximum, monitor for changes", "Acceptable - below maximum", "Fail - must be below 0.35Ω", "Retest with different instrument"]),
        "correct_answer": "Borderline - exactly at maximum, monitor for changes",
        "explanation": "0.35Ω is the maximum declared by the DNO for TN-C-S. While technically at the limit, any increase in soil conditions or connections could make it non-compliant.",
        "regulation_reference": "BS 7671 Table 41.1",
        "practical_tip": "Record the value and check all connections at the MET. A high Ze will affect all downstream Zs readings.",
        "epra_class": "Class B"
    },

    # ========================
    # INSTALLATION PRACTICES (12 Theory + 8 Practical = 20)
    # ========================
    
    # Theory Questions
    {
        "category": "Installation Practices",
        "difficulty": "easy",
        "question_text": "What is the minimum bending radius for PVC insulated and sheathed cables during installation?",
        "options": json.dumps(["6 times cable diameter", "4 times cable diameter", "8 times cable diameter", "10 times cable diameter"]),
        "correct_answer": "6 times cable diameter",
        "explanation": "PVC cables require a minimum bending radius of 6 times the overall cable diameter to prevent damage to the insulation and sheath.",
        "regulation_reference": "BS 7671 522.8.3",
        "practical_tip": "If the bend is tighter than your fist, it's probably too sharp for most domestic cables.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "medium",
        "question_text": "What is the minimum depth for buried cables in a garden?",
        "options": json.dumps(["450mm", "300mm", "600mm", "150mm"]),
        "correct_answer": "450mm",
        "explanation": "Cables buried in ground must be at least 450mm deep to protect against damage from gardening activities and surface loads.",
        "regulation_reference": "BS 7671 522.8.10",
        "practical_tip": "Use warning tape above the cable at 150mm below surface. This alerts anyone digging that a cable is below.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "hard",
        "question_text": "What is the minimum IP rating for a socket-outlet installed outdoors with no additional protection from weather?",
        "options": json.dumps(["IP66", "IP44", "IPX4", "IP20"]),
        "correct_answer": "IP66",
        "explanation": "Outdoor socket-outlets without additional weather protection must be rated IP66 for protection against heavy rain and water jets.",
        "regulation_reference": "BS 7671 522.8.1",
        "practical_tip": "Even IP66 sockets should be mounted with cable entries at the bottom to prevent water ingress along cables.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "easy",
        "question_text": "In which zones of a bathroom are socket-outlets permitted?",
        "options": json.dumps(["Outside zones 0, 1, and 2 (minimum 3m from zone 2)", "Zone 2 only", "Zone 1 and 2", "Nowhere in a bathroom"]),
        "correct_answer": "Outside zones 0, 1, and 2 (minimum 3m from zone 2)",
        "explanation": "Socket-outlets are only permitted outside bathroom zones, at least 3m from the boundary of zone 2.",
        "regulation_reference": "BS 7671 701.512.3",
        "practical_tip": "In practice, most domestic bathrooms are too small for socket-outlets. Use shaver sockets complying with BS 3535.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "medium",
        "question_text": "What is the recommended maximum number of socket-outlets on a 32A ring final circuit?",
        "options": json.dumps(["Unlimited within 100m² floor area", "10 sockets", "6 sockets", "12 sockets"]),
        "correct_answer": "Unlimited within 100m² floor area",
        "explanation": "BS 7671 does not limit the number of socket-outlets on a ring final circuit, but the circuit should serve no more than 100m² of floor area.",
        "regulation_reference": "BS 7671 Appendix 15",
        "practical_tip": "For kitchens, consider a separate ring circuit due to high appliance density. For large houses, use multiple ring circuits.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "hard",
        "question_text": "What is the minimum cross-sectional area for a main earthing conductor in a TN-S system with 25mm² tails?",
        "options": json.dumps(["16mm²", "10mm²", "6mm²", "25mm²"]),
        "correct_answer": "16mm²",
        "explanation": "For TN-S with 25mm² line conductor, Table 54.7 requires minimum 16mm² main earthing conductor. This is independent of the bonding conductor size.",
        "regulation_reference": "BS 7671 Table 54.7",
        "practical_tip": "Main earthing conductor connects the MET to the earth electrode or supply earth terminal. Not to be confused with bonding conductors.",
        "epra_class": "Class B"
    },
    {
        "category": "Installation Practices",
        "difficulty": "medium",
        "question_text": "Where should a consumer unit NOT be installed?",
        "options": json.dumps(["Under a staircase (escape route)", "In a garage", "In a utility room", "Under the stairs with fire protection"]),
        "correct_answer": "Under a staircase (escape route)",
        "explanation": "Consumer units should not be installed on escape routes, including under stairs, unless they are in a fire-resistant enclosure.",
        "regulation_reference": "BS 7671 421.1.201",
        "practical_tip": "If the consumer unit must be under stairs, install a metal enclosure and ensure adequate fire protection of the surrounding area.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "easy",
        "question_text": "What is the minimum height for a consumer unit?",
        "options": json.dumps(["No specified minimum - accessible for operation", "1400mm", "1200mm", "1500mm"]),
        "correct_answer": "No specified minimum - accessible for operation",
        "explanation": "BS 7671 does not specify a minimum height for consumer units. They should be installed at a height that allows easy access for operation and maintenance.",
        "regulation_reference": "BS 7671 132.12",
        "practical_tip": "Part M of Building Regulations recommends switches at 1350-1450mm. Apply common sense for accessibility.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "hard",
        "question_text": "What is the minimum separation distance between low voltage (230V) and extra-low voltage (12V) cables running in the same trunking?",
        "options": json.dumps(["Must be separated by a physical barrier or use cables rated for highest voltage present", "50mm", "100mm", "No separation needed"]),
        "correct_answer": "Must be separated by a physical barrier or use cables rated for highest voltage present",
        "explanation": "BS 7671 requires segregation between different voltage bands unless all cables are insulated for the highest voltage present.",
        "regulation_reference": "BS 7671 528.1",
        "practical_tip": "Use separate trunking compartments or ensure all cables in the trunking are rated for 230V operation.",
        "epra_class": "Class B"
    },
    {
        "category": "Installation Practices",
        "difficulty": "medium",
        "question_text": "What type of cable is most suitable for underground installation?",
        "options": json.dumps(["SWA (Steel Wire Armoured)", "PVC twin and earth", "PVC singles in conduit", "Flexible cable"]),
        "correct_answer": "SWA (Steel Wire Armoured)",
        "explanation": "Steel Wire Armoured cable provides mechanical protection against ground pressure, digging, and rodent damage for underground installations.",
        "regulation_reference": "BS 7671 522.8.10",
        "practical_tip": "Always use the correct SWA glands and ensure the armour is earthed at the supply end.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "easy",
        "question_text": "What is the standard height for light switches in new domestic installations?",
        "options": json.dumps(["1350mm to centre", "1200mm to centre", "1500mm to centre", "1000mm to centre"]),
        "correct_answer": "1350mm to centre",
        "explanation": "Part M of Building Regulations recommends light switches at 1350mm to centre for accessibility by wheelchair users.",
        "regulation_reference": "Building Regulations Part M",
        "practical_tip": "Be consistent with heights throughout the installation. Mark positions with a spirit level before cutting boxes.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "hard",
        "question_text": "What is the maximum permitted length for a flexible cord supplying a pendant light fitting?",
        "options": json.dumps(["No specified maximum in BS 7671, but typically 1.5m", "3m", "1m", "2m"]),
        "correct_answer": "No specified maximum in BS 7671, but typically 1.5m",
        "explanation": "BS 7671 does not specify a maximum length for pendant flex, but practical considerations and manufacturer instructions typically limit to 1.5m.",
        "regulation_reference": "BS 7671 559.6",
        "practical_tip": "Longer pendants put strain on ceiling fixings. For high ceilings, consider chain suspension with cable support.",
        "epra_class": "Class C"
    },
    
    # Practical Scenario Questions
    {
        "category": "Installation Practices",
        "difficulty": "hard",
        "question_text": "PRACTICAL: You are installing a new circuit in a building with thermal insulation in the loft. The cable will be covered by 100mm of insulation. What derating factor applies?",
        "options": json.dumps(["Cable in thermal insulation >100mm - rating may be halved (derating ~0.5)", "No derating needed", "Derate by 0.7", "Use high-temperature cable"]),
        "correct_answer": "Cable in thermal insulation >100mm - rating may be halved (derating ~0.5)",
        "explanation": "Cables covered by >100mm thermal insulation have significantly reduced heat dissipation. Current rating can be reduced by 50% or more (Method 101/103).",
        "regulation_reference": "BS 7671 Table 4D5, Method 101",
        "practical_tip": "Either clip cables above insulation or significantly increase cable size. A 2.5mm² cable rated 27A clipped direct may only handle 13.5A in deep insulation.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "medium",
        "question_text": "PRACTICAL: You need to install a cable through a wall from an external socket to internal consumer unit. What protection is required?",
        "options": json.dumps(["RCD protection (30mA) and appropriate IP rating for external penetration", "No special protection needed", "MCB only", "Double insulation"]),
        "correct_answer": "RCD protection (30mA) and appropriate IP rating for external penetration",
        "explanation": "External sockets require 30mA RCD protection. The wall penetration must be sealed to maintain weatherproofing and prevent water ingress.",
        "regulation_reference": "BS 7671 411.3.3, 522.8",
        "practical_tip": "Drill the hole at a slight downward angle to prevent water tracking inwards. Use silicone sealant around the cable entry.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "hard",
        "question_text": "PRACTICAL: A client wants recessed downlights in a ceiling with 300mm loft insulation above. What must you consider?",
        "options": json.dumps(["Use fire-rated fittings, maintain clearance around lights, check insulation compatibility", "Install any downlights - insulation will protect", "Only use LED lamps", "Remove all insulation"]),
        "correct_answer": "Use fire-rated fittings, maintain clearance around lights, check insulation compatibility",
        "explanation": "Downlights generate heat. Insulation must not cover them. Use fire-rated fittings to maintain ceiling fire integrity. Maintain manufacturer's clearance distances.",
        "regulation_reference": "BS 7671 559.6, Building Regulations Part B",
        "practical_tip": "Use insulation guards or hoods over downlights to maintain clearance. Some LED fittings are rated for insulation contact.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "medium",
        "question_text": "PRACTICAL: When installing a new consumer unit, you notice the existing main earth conductor is 6mm² on a 25mm² tail TN-S system. What should you do?",
        "options": json.dumps(["Upgrade to 16mm² - 6mm² is undersized for TN-S with 25mm² tails", "Leave it - it's working", "Add a supplementary earth", "Change to TT system"]),
        "correct_answer": "Upgrade to 16mm² - 6mm² is undersized for TN-S with 25mm² tails",
        "explanation": "Table 54.7 requires 16mm² minimum main earthing conductor for 25mm² tails on TN-S. 6mm² is non-compliant and potentially dangerous.",
        "regulation_reference": "BS 7671 Table 54.7",
        "practical_tip": "Always check earthing conductor size when upgrading consumer units. It's a common non-compliance in older installations.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "easy",
        "question_text": "PRACTICAL: A kitchen fitter asks you to install a socket inside a kitchen cabinet for a microwave. Is this permitted?",
        "options": json.dumps(["Yes, but socket must be accessible and not exposed to heat/steam", "No, sockets not allowed in cabinets", "Only with IP44 rating", "Yes, any socket is fine"]),
        "correct_answer": "Yes, but socket must be accessible and not exposed to heat/steam",
        "explanation": "Socket-outlets in cabinets are permitted provided they are accessible for operation and testing, and not exposed to excessive heat or moisture.",
        "regulation_reference": "BS 7671 132.12",
        "practical_tip": "Consider using a switched fused connection unit above the worktop controlling a flex outlet in the cabinet. This is often more practical.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "hard",
        "question_text": "PRACTICAL: You are running cables in a stud wall with metal capping. The capping is earthed. What is the purpose of the metal capping?",
        "options": json.dumps(["Mechanical protection only - not intended as an earth path", "Supplementary earthing", "Electromagnetic shielding", "Earth fault path"]),
        "correct_answer": "Mechanical protection only - not intended as an earth path",
        "explanation": "Metal capping provides mechanical protection against penetration by nails and screws. It must be earthed to prevent it becoming live if a cable is damaged.",
        "regulation_reference": "BS 7671 522.6.6",
        "practical_tip": "Capping alone may not prevent nail penetration. For better protection, use steel conduit or specify safe zones clearly.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "medium",
        "question_text": "PRACTICAL: You notice the existing wiring in a house has black and red colored cables. The installation dates from 1995. What does this indicate?",
        "options": json.dumps(["Pre-harmonization colors - red=line, black=neutral. Installation may need rewiring", "Faulty wiring - colors wrong", "Commercial installation colors", "Alien wiring system"]),
        "correct_answer": "Pre-harmonization colors - red=line, black=neutral. Installation may need rewiring",
        "explanation": "Red/black colors were used before harmonization in 2004. The installation is 30+ years old and may have degraded insulation. An EICR is strongly recommended.",
        "regulation_reference": "BS 7671 Appendix 7",
        "practical_tip": "Old colors = old installation. Check for rubber insulation, no RCD protection, and other age-related issues.",
        "epra_class": "Class C"
    },
    {
        "category": "Installation Practices",
        "difficulty": "hard",
        "question_text": "PRACTICAL: A client wants 3-phase supply installed for a workshop. The DNO has provided a 100A TN-C-S supply. What size meter tails are required?",
        "options": json.dumps(["25mm² for 100A supply", "16mm²", "35mm²", "10mm²"]),
        "correct_answer": "25mm² for 100A supply",
        "explanation": "For a 100A supply, 25mm² copper tails are standard. Check Table 4D1A for installation method. 25mm² in free air handles approximately 114A.",
        "regulation_reference": "BS 7671 Table 4D1A",
        "practical_tip": "Keep meter tails as short as possible. If longer than 3m, install a switch-fuse at the meter position.",
        "epra_class": "Class B"
    },


    # ========================
    # KENYA POWER STANDARDS (10 Theory + 6 Practical = 16)
    # ========================
    
    # Theory Questions
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
        "category": "Kenya Power Standards",
        "difficulty": "medium",
        "question_text": "What is the standard frequency of electricity supply in Kenya?",
        "options": json.dumps(["50Hz", "60Hz", "50/60Hz", "100Hz"]),
        "correct_answer": "50Hz",
        "explanation": "Kenya Power operates at a standard frequency of 50Hz for all electricity supply across the country.",
        "regulation_reference": "Kenya Power Distribution Code",
        "practical_tip": "All electrical equipment installed in Kenya must be compatible with 50Hz operation. Check nameplate ratings before installation.",
        "epra_class": "Class C"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "hard",
        "question_text": "What is the maximum voltage variation allowed by Kenya Power at the point of supply?",
        "options": json.dumps(["±6% of nominal voltage (240V ± 14.4V)", "±10%", "±5%", "±2%"]),
        "correct_answer": "±6% of nominal voltage (240V ± 14.4V)",
        "explanation": "Kenya Power allows voltage variation of ±6% at the point of supply. This means voltage can range from 225.6V to 254.4V for single-phase.",
        "regulation_reference": "Kenya Power Distribution Code, Schedule 2",
        "practical_tip": "If voltage is consistently outside this range, report to Kenya Power. It may indicate transformer or distribution issues.",
        "epra_class": "Class B"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "easy",
        "question_text": "Who is responsible for the supply cable up to the meter in a domestic installation?",
        "options": json.dumps(["Kenya Power (the DNO)", "The homeowner", "The electrician", "The building contractor"]),
        "correct_answer": "Kenya Power (the DNO)",
        "explanation": "Kenya Power is responsible for the distribution network and supply cable up to and including the meter. The consumer is responsible after the meter.",
        "regulation_reference": "Energy Act 2019, Kenya Power Connection Policy",
        "practical_tip": "The meter tails from the meter to the consumer unit are the responsibility of the consumer.",
        "epra_class": "Class C"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "medium",
        "question_text": "What document must an electrician hold to legally perform electrical installation work in Kenya?",
        "options": json.dumps(["EPRA Electrician License (Class C, B, or A)", "Kenya Power Work Permit", "Local Authority Business Permit", "University Degree"]),
        "correct_answer": "EPRA Electrician License (Class C, B, or A)",
        "explanation": "All electricians in Kenya must be licensed by EPRA. Class C is for domestic, Class B for commercial, and Class A for high voltage installations.",
        "regulation_reference": "Energy Act 2019, EPRA Licensing Regulations",
        "practical_tip": "Always display your EPRA license number on certificates. Working without a license is illegal and can result in prosecution.",
        "epra_class": "Class C"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "hard",
        "question_text": "What is the standard three-phase voltage supplied by Kenya Power?",
        "options": json.dumps(["415V", "400V", "440V", "380V"]),
        "correct_answer": "415V",
        "explanation": "Kenya Power supplies 415V three-phase at 50Hz. This gives 240V single-phase (415/√3 = 240V).",
        "regulation_reference": "Kenya Power Distribution Code",
        "calculation_steps": "1. VL = 415V (line-to-line)\n2. Vph = VL/√3\n3. Vph = 415/1.732\n4. Vph = 239.6V ≈ 240V",
        "practical_tip": "Always verify phase rotation when connecting three-phase equipment. Incorrect rotation can damage motors.",
        "epra_class": "Class B"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "medium",
        "question_text": "What type of earthing system does Kenya Power primarily use for domestic supplies?",
        "options": json.dumps(["TN-C-S (PME - Protective Multiple Earthing)", "TT", "TN-S", "IT"]),
        "correct_answer": "TN-C-S (PME - Protective Multiple Earthing)",
        "explanation": "Kenya Power predominantly uses TN-C-S (PME) for domestic supplies, where the neutral and earth are combined in the supply cable and separated at the consumer unit.",
        "regulation_reference": "Kenya Power Engineering Standard",
        "practical_tip": "TN-C-S systems require special considerations. Never connect the earth to neutral downstream of the consumer unit.",
        "epra_class": "Class C"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "easy",
        "question_text": "What is the maximum demand for a standard single-phase domestic supply in Kenya?",
        "options": json.dumps(["60A", "100A", "30A", "80A"]),
        "correct_answer": "60A",
        "explanation": "Standard domestic single-phase supplies in Kenya are typically rated at 60A, with 100A available for larger installations.",
        "regulation_reference": "Kenya Power Connection Policy",
        "practical_tip": "If the calculated maximum demand exceeds 60A, consider requesting a 100A supply or three-phase connection.",
        "epra_class": "Class C"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "hard",
        "question_text": "What is the minimum clearance height for overhead power lines crossing a road in Kenya?",
        "options": json.dumps(["6.1 meters", "5.5 meters", "4.5 meters", "7.5 meters"]),
        "correct_answer": "6.1 meters",
        "explanation": "Kenya Power specifies minimum clearance of 6.1m for low voltage lines crossing roads to allow safe passage of vehicles.",
        "regulation_reference": "Kenya Power Overhead Line Construction Standards",
        "practical_tip": "Never work near overhead lines without proper safety clearance. Contact Kenya Power for shrouding or isolation before working near lines.",
        "epra_class": "Class B"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "medium",
        "question_text": "When must an installation be inspected and tested before connection by Kenya Power?",
        "options": json.dumps(["All new installations and major alterations", "Only commercial installations", "Only when requested", "Never - electrician's certificate is sufficient"]),
        "correct_answer": "All new installations and major alterations",
        "explanation": "Kenya Power requires all new installations and major alterations to be inspected and tested by a licensed electrician, with a completion certificate issued before connection.",
        "regulation_reference": "Energy Act 2019, Electrical Installation Regulations",
        "practical_tip": "Schedule the Kenya Power inspection after you've completed your own testing. Have all documentation ready for the inspector.",
        "epra_class": "Class C"
    },
    
    # Practical Scenario Questions
    {
        "category": "Kenya Power Standards",
        "difficulty": "hard",
        "question_text": "PRACTICAL: A client's voltage measured at 218V consistently. Kenya Power's nominal is 240V ±6% (225.6V-254.4V). What should you do?",
        "options": json.dumps(["Report to Kenya Power - voltage below minimum permitted", "Install a voltage stabilizer", "Nothing - it's close enough", "Change the transformer tap setting"]),
        "correct_answer": "Report to Kenya Power - voltage below minimum permitted",
        "explanation": "218V is below the minimum 225.6V (-6% of 240V). This can cause equipment malfunction. Kenya Power must investigate their distribution network.",
        "regulation_reference": "Kenya Power Distribution Code",
        "practical_tip": "Document voltage readings at different times of day. This helps Kenya Power identify if it's a peak demand or continuous issue.",
        "epra_class": "Class C"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "medium",
        "question_text": "PRACTICAL: A client in rural Kenya has a TT earthing system with no RCD. The earth rod resistance is 80Ω. Is this safe?",
        "options": json.dumps(["No - TT systems must have RCD protection. 80Ω × 0.03A = 2.4V (safe with RCD)", "Yes - 80Ω is low enough", "Yes if earth rod is deep enough", "No - earth rod must be <1Ω"]),
        "correct_answer": "No - TT systems must have RCD protection. 80Ω × 0.03A = 2.4V (safe with RCD)",
        "explanation": "TT systems rely on RCDs for earth fault protection. Without RCD, a fault could leave exposed metalwork at dangerous voltages. Install a 30mA RCD.",
        "regulation_reference": "BS 7671 411.5.3",
        "practical_tip": "In rural areas, TT systems are common. Always install RCD protection and test earth electrode resistance.",
        "epra_class": "Class C"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "easy",
        "question_text": "PRACTICAL: A client's premises is 200m from the nearest Kenya Power transformer. What must be considered for the supply?",
        "options": json.dumps(["Voltage drop over long distance may require larger cables", "No special consideration needed", "The client must pay for a new transformer", "Only underground cable can be used"]),
        "correct_answer": "Voltage drop over long distance may require larger cables",
        "explanation": "Long supply distances cause significant voltage drop. The supply cable must be sized to maintain voltage within ±6% at full load.",
        "regulation_reference": "Kenya Power Connection Policy, BS 7671 525",
        "practical_tip": "Kenya Power may require the customer to pay for upgraded cables or a dedicated transformer for very long runs.",
        "epra_class": "Class C"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "hard",
        "question_text": "PRACTICAL: You are installing a 3-phase distribution board for a small factory. How do you verify phase rotation is correct?",
        "options": json.dumps(["Use a phase rotation meter - L1, L2, L3 should be clockwise", "Connect a motor and see which way it turns", "Any connection order is fine", "Check with a voltmeter"]),
        "correct_answer": "Use a phase rotation meter - L1, L2, L3 should be clockwise",
        "explanation": "Phase rotation must be verified with a rotation meter. Incorrect rotation can cause motors to run backwards, potentially damaging equipment.",
        "regulation_reference": "BS 7671 643.7",
        "practical_tip": "Standard UK/Kenyan rotation is L1-L2-L3 clockwise. Label phases clearly at the distribution board for future reference.",
        "epra_class": "Class B"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "medium",
        "question_text": "PRACTICAL: A client has a 240V single-phase supply but wants to install a 3-phase borehole pump. What options do they have?",
        "options": json.dumps(["Apply to Kenya Power for 3-phase supply upgrade or use a phase converter", "Cannot install 3-phase equipment", "Connect across two phases", "Use a generator"]),
        "correct_answer": "Apply to Kenya Power for 3-phase supply upgrade or use a phase converter",
        "explanation": "If 3-phase supply is available nearby, Kenya Power can upgrade the connection. Alternatively, a single-phase to 3-phase converter can be used for smaller motors.",
        "regulation_reference": "Kenya Power Connection Policy",
        "practical_tip": "Phase converters are cost-effective for single motors. For multiple 3-phase loads, a proper 3-phase supply is recommended.",
        "epra_class": "Class C"
    },
    {
        "category": "Kenya Power Standards",
        "difficulty": "hard",
        "question_text": "PRACTICAL: A commercial kitchen has a 3-phase supply. You measure: L1=238V, L2=242V, L3=235V. Is this acceptable?",
        "options": json.dumps(["Yes - all within ±6% of 240V and reasonably balanced", "No - voltages should be identical", "No - L3 too low", "Yes but only for domestic"]),
        "correct_answer": "Yes - all within ±6% of 240V and reasonably balanced",
        "explanation": "All readings are within the 225.6V-254.4V range. Small phase-to-phase variations are normal due to unbalanced loading on the network.",
        "regulation_reference": "Kenya Power Distribution Code",
        "practical_tip": "Significant voltage imbalance (>10% difference between phases) should be reported to Kenya Power for investigation.",
        "epra_class": "Class B"
    },

    # ========================
    # PROTECTION DEVICES (10 Theory + 6 Practical = 16)
    # ========================
    
    # Theory Questions
    {
        "category": "Protection Devices",
        "difficulty": "medium",
        "question_text": "What is the primary function of a Miniature Circuit Breaker (MCB)?",
        "options": json.dumps(["Overcurrent protection (overload and short circuit)", "Earth fault protection only", "Voltage regulation", "Power factor correction"]),
        "correct_answer": "Overcurrent protection (overload and short circuit)",
        "explanation": "MCBs provide protection against both overload currents (thermal trip) and short circuit currents (magnetic trip) in electrical circuits.",
        "regulation_reference": "BS 7671 433.1",
        "practical_tip": "Type B MCBs are standard for domestic. Type C for inductive loads (motors). Type D for high inrush currents (transformers, welding).",
        "epra_class": "Class C"
    },
    {
        "category": "Protection Devices",
        "difficulty": "hard",
        "question_text": "What is the difference between a Type B and Type C MCB?",
        "options": json.dumps(["Type C has higher magnetic trip threshold (5-10× In vs 3-5× In for Type B)", "Type B is for DC circuits", "Type C has better overload protection", "No difference - just different manufacturers"]),
        "correct_answer": "Type C has higher magnetic trip threshold (5-10× In vs 3-5× In for Type B)",
        "explanation": "Type B MCBs trip magnetically at 3-5 times rated current. Type C trip at 5-10 times, making them suitable for loads with higher inrush currents like motors.",
        "regulation_reference": "BS 7671 Table 41.3",
        "practical_tip": "Use Type C for motors, fluorescent lighting banks, and large transformers. Use Type B for general domestic socket and lighting circuits.",
        "epra_class": "Class C"
    },
    {
        "category": "Protection Devices",
        "difficulty": "easy",
        "question_text": "What does an RCD (Residual Current Device) protect against?",
        "options": json.dumps(["Earth leakage current and electric shock", "Overload current", "Short circuits", "Voltage surges"]),
        "correct_answer": "Earth leakage current and electric shock",
        "explanation": "RCDs detect imbalance between line and neutral currents (earth leakage) and disconnect within 40ms to protect against electric shock.",
        "regulation_reference": "BS 7671 411.3.3",
        "practical_tip": "RCDs do NOT protect against overload or short circuit. Always use MCB or RCBO for complete protection.",
        "epra_class": "Class C"
    },
    {
        "category": "Protection Devices",
        "difficulty": "medium",
        "question_text": "What is an RCBO?",
        "options": json.dumps(["Combined RCD and MCB in one device", "Remote Controlled Breaker Operated", "Residual Current Breaker Only", "Rotary Circuit Breaker Overload"]),
        "correct_answer": "Combined RCD and MCB in one device",
        "explanation": "An RCBO (Residual Current Breaker with Overcurrent protection) combines earth leakage, overload, and short circuit protection in a single device.",
        "regulation_reference": "BS 7671 Part 2 Definitions",
        "practical_tip": "RCBOs provide individual circuit protection. If one trips, only that circuit is affected, unlike split-load RCD boards.",
        "epra_class": "Class C"
    },
    {
        "category": "Protection Devices",
        "difficulty": "hard",
        "question_text": "What is the maximum Zs for a 20A Type D MCB on a 230V TN system?",
        "options": json.dumps(["0.58Ω", "1.15Ω", "0.38Ω", "2.30Ω"]),
        "correct_answer": "0.58Ω",
        "explanation": "Type D MCBs trip at 10-20× In. Using 20×: Zs = 230/(20×20) = 230/400 = 0.575Ω. Type D requires very low Zs values.",
        "regulation_reference": "BS 7671 Table 41.3",
        "calculation_steps": "1. Type D multiplier = 20\n2. Zs = 230 / (20 × 20)\n3. Zs = 230 / 400\n4. Zs = 0.575Ω ≈ 0.58Ω",
        "practical_tip": "Type D MCBs require excellent earthing. Often used for welding equipment and large transformers with very high inrush currents.",
        "epra_class": "Class B"
    },
    {
        "category": "Protection Devices",
        "difficulty": "medium",
        "question_text": "What is the purpose of a surge protection device (SPD)?",
        "options": json.dumps(["Protect against transient overvoltages (lightning, switching surges)", "Overload protection", "Earth fault protection", "Power factor correction"]),
        "correct_answer": "Protect against transient overvoltages (lightning, switching surges)",
        "explanation": "SPDs protect electrical equipment from voltage spikes caused by lightning strikes or switching operations on the power network.",
        "regulation_reference": "BS 7671 Section 443",
        "practical_tip": "SPDs are required where consequences of overvoltage could cause serious injury, loss of life, or significant financial loss.",
        "epra_class": "Class C"
    },
    {
        "category": "Protection Devices",
        "difficulty": "easy",
        "question_text": "What does the 'In' rating on an MCB represent?",
        "options": json.dumps(["Nominal rated current", "Instantaneous trip current", "Earth fault current", "Maximum breaking capacity"]),
        "correct_answer": "Nominal rated current",
        "explanation": "In is the nominal rated current that the MCB can carry continuously without tripping under specified conditions.",
        "regulation_reference": "BS 7671 Part 2 Definitions",
        "practical_tip": "Select MCB so that Ib ≤ In ≤ Iz (Design current ≤ MCB rating ≤ Cable capacity).",
        "epra_class": "Class C"
    },
    {
        "category": "Protection Devices",
        "difficulty": "hard",
        "question_text": "What is the minimum breaking capacity required for a domestic consumer unit MCB?",
        "options": json.dumps(["6kA (6000A) typically sufficient for domestic", "3kA", "10kA", "16kA"]),
        "correct_answer": "6kA (6000A) typically sufficient for domestic",
        "explanation": "BS 7671 requires MCBs to have adequate breaking capacity for the prospective fault current. 6kA is standard for domestic installations in Kenya.",
        "regulation_reference": "BS 7671 434.5.1",
        "practical_tip": "For installations close to distribution transformers (high PFC), 10kA or higher breaking capacity may be required.",
        "epra_class": "Class C"
    },
    {
        "category": "Protection Devices",
        "difficulty": "medium",
        "question_text": "What is discrimination (selectivity) in protective devices?",
        "options": json.dumps(["Ensuring only the nearest upstream device trips during a fault", "All devices trip simultaneously", "RCD and MCB tripping together", "Fast tripping of all devices"]),
        "correct_answer": "Ensuring only the nearest upstream device trips during a fault",
        "explanation": "Discrimination ensures that under fault conditions, only the protective device closest to the fault operates, minimizing disruption to other circuits.",
        "regulation_reference": "BS 7671 536",
        "practical_tip": "Good discrimination means a faulty appliance only trips its plug fuse, not the whole consumer unit RCD.",
        "epra_class": "Class C"
    },
    {
        "category": "Protection Devices",
        "difficulty": "hard",
        "question_text": "An RCD rated at 30mA trips at 18mA during a ramp test. Is this RCD functioning correctly?",
        "options": json.dumps(["Yes - should trip between 15-30mA (50-100% of IΔn)", "No - should trip at exactly 30mA", "No - tripped too early at 18mA", "Yes but only at 0° test angle"]),
        "correct_answer": "Yes - should trip between 15-30mA (50-100% of IΔn)",
        "explanation": "BS 7671 requires RCDs to trip between 50-100% of rated IΔn. For a 30mA RCD, this is 15-30mA. 18mA is within the acceptable range.",
        "regulation_reference": "BS 7671 643.8",
        "practical_tip": "An RCD tripping below 15mA may be overly sensitive and prone to nuisance tripping. Above 30mA indicates a faulty RCD.",
        "epra_class": "Class C"
    },
    
    # Practical Scenario Questions
    {
        "category": "Protection Devices",
        "difficulty": "hard",
        "question_text": "PRACTICAL: A 7.5kW 3-phase motor (11A FLC) trips the 16A Type C MCB on startup. The MCB is correctly sized. What is the likely cause?",
        "options": json.dumps(["Motor starting current 6-8× FLC (66-88A) - needs Type D MCB or soft starter", "Faulty motor", "MCB too small - use 32A", "Wrong voltage"]),
        "correct_answer": "Motor starting current 6-8× FLC (66-88A) - needs Type D MCB or soft starter",
        "explanation": "Motor starting current can be 6-8 times FLC (66-88A). Type C trips at 5-10× In (80-160A). The starting current falls within the tripping range causing nuisance trips.",
        "regulation_reference": "BS 7671 433.1",
        "calculation_steps": "1. FLC = 11A\n2. Starting current = 11 × 7 = 77A (average)\n3. Type C trip range: 5×16=80A to 10×16=160A\n4. 77A is very close to 80A threshold\n5. Use Type D or soft starter",
        "practical_tip": "For motors with high starting currents, use Type D MCB (10-20× In) or install a soft starter/VSD to reduce inrush.",
        "epra_class": "Class B"
    },
    {
        "category": "Protection Devices",
        "difficulty": "medium",
        "question_text": "PRACTICAL: A split-load consumer unit has one RCD protecting 6 circuits. The RCD trips when the kettle is used. What's the most efficient solution?",
        "options": json.dumps(["Install RCBOs on individual circuits for better discrimination", "Replace the RCD with higher rating", "Split circuits across more RCDs", "Remove the RCD"]),
        "correct_answer": "Install RCBOs on individual circuits for better discrimination",
        "explanation": "Cumulative earth leakage from multiple circuits can cause RCD nuisance tripping. RCBOs provide individual circuit protection without affecting other circuits.",
        "regulation_reference": "BS 7671 531.3",
        "practical_tip": "Modern consumer units with all RCBOs are recommended for new installations. They eliminate the 'whole house in darkness' problem.",
        "epra_class": "Class C"
    },
    {
        "category": "Protection Devices",
        "difficulty": "hard",
        "question_text": "PRACTICAL: PFC measured at consumer unit is 8.2kA. The installed MCBs are rated 6kA breaking capacity. What action must you take?",
        "options": json.dumps(["Replace with 10kA MCBs - 6kA is inadequate for 8.2kA PFC", "Install an RCD", "No action needed - it's close enough", "Reduce the main fuse rating"]),
        "correct_answer": "Replace with 10kA MCBs - 6kA is inadequate for 8.2kA PFC",
        "explanation": "MCB breaking capacity must exceed the maximum prospective fault current. 6kA < 8.2kA means the MCBs could fail explosively under fault conditions.",
        "regulation_reference": "BS 7671 434.5.1",
        "practical_tip": "This is a C2 (potentially dangerous) observation. The MCBs could fail to safely interrupt a fault, causing fire or explosion risk.",
        "epra_class": "Class B"
    },
    {
        "category": "Protection Devices",
        "difficulty": "medium",
        "question_text": "PRACTICAL: A 30mA RCD trips immediately when a specific circuit is energized, even with all appliances unplugged. What is the most likely fault?",
        "options": json.dumps(["Neutral-to-earth fault on the circuit wiring", "Overloaded circuit", "Faulty RCD", "Wrong MCB type"]),
        "correct_answer": "Neutral-to-earth fault on the circuit wiring",
        "explanation": "A neutral-to-earth fault causes current to bypass the RCD's sensing coil, creating an imbalance that trips the RCD. This occurs even without load.",
        "regulation_reference": "BS 7671 531.3",
        "practical_tip": "Test with insulation resistance tester between neutral and earth. A reading below 1MΩ indicates a fault. Check junction boxes and accessories.",
        "epra_class": "Class C"
    },
    {
        "category": "Protection Devices",
        "difficulty": "easy",
        "question_text": "PRACTICAL: A customer complains that their 63A RCD trips during heavy rain. The RCD protects external circuits. What is the likely cause?",
        "options": json.dumps(["Water ingress in external fittings causing earth leakage", "RCD is faulty", "Overload from external circuits", "Lightning strike"]),
        "correct_answer": "Water ingress in external fittings causing earth leakage",
        "explanation": "Water in external sockets, junction boxes, or light fittings creates leakage paths to earth, tripping the RCD. Check all external accessories for water damage.",
        "regulation_reference": "BS 7671 522.8",
        "practical_tip": "Ensure all external electrical accessories have adequate IP ratings and cable entries are sealed with appropriate glands or sealant.",
        "epra_class": "Class C"
    },
    {
        "category": "Protection Devices",
        "difficulty": "hard",
        "question_text": "PRACTICAL: You need to protect a 32A ring final circuit. The calculated Zs is 0.9Ω. Which combination provides fastest disconnection?",
        "options": json.dumps(["32A Type B MCB - Zs max 1.44Ω, 0.9Ω is well within limits", "32A Type C MCB - Zs max 0.72Ω, 0.9Ω exceeds limits", "20A Type B MCB", "32A Type D MCB"]),
        "correct_answer": "32A Type B MCB - Zs max 1.44Ω, 0.9Ω is well within limits",
        "explanation": "Type B max Zs = 1.44Ω > 0.9Ω ✓. Type C max Zs = 0.72Ω < 0.9Ω ✗. Type B is appropriate and provides required disconnection time.",
        "regulation_reference": "BS 7671 Table 41.3",
        "practical_tip": "Always check Zs against the MCB type. A Type C MCB needs half the Zs of Type B for the same current rating.",
        "epra_class": "Class C"
    },

    # ========================
    # REGULATIONS & COMPLIANCE (10 Theory + 5 Practical = 15)
    # ========================
    
    # Theory Questions
    {
        "category": "Regulations & Compliance",
        "difficulty": "easy",
        "question_text": "Which British Standard covers electrical installations in the UK and Kenya?",
        "options": json.dumps(["BS 7671 (IET Wiring Regulations)", "BS 5839", "BS 5266", "BS 9999"]),
        "correct_answer": "BS 7671 (IET Wiring Regulations)",
        "explanation": "BS 7671 is the national standard for electrical installation in the UK and is widely adopted in Kenya as the basis for electrical regulations.",
        "regulation_reference": "BS 7671:2018+A2:2022",
        "practical_tip": "Always use the latest edition. BS 7671 is updated every 3 years. Kenya may adopt amendments at different times.",
        "epra_class": "Class C"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "medium",
        "question_text": "What is the maximum interval between periodic inspection and testing for a domestic installation?",
        "options": json.dumps(["10 years (or change of occupancy)", "5 years", "3 years", "1 year"]),
        "correct_answer": "10 years (or change of occupancy)",
        "explanation": "BS 7671 recommends EICRs every 10 years for domestic owner-occupied properties, or on change of occupancy for rented properties.",
        "regulation_reference": "BS 7671 Table 3.2",
        "practical_tip": "Rented properties require EICRs every 5 years or at each change of tenancy. Commercial: 5 years. Industrial: 3 years.",
        "epra_class": "Class C"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "hard",
        "question_text": "What is the purpose of an Electrical Installation Certificate (EIC)?",
        "options": json.dumps(["To certify a new installation complies with BS 7671 and is safe for use", "To register with Kenya Power", "To apply for an EPRA license", "To bill the customer"]),
        "correct_answer": "To certify a new installation complies with BS 7671 and is safe for use",
        "explanation": "An EIC is a legal declaration that a new installation, addition, or alteration has been designed, constructed, and tested in accordance with BS 7671.",
        "regulation_reference": "BS 7671 Part 6, 644.1",
        "practical_tip": "Keep EIC copies for at least 3 years. Provide the original to the person ordering the work. It may be required for insurance or house sales.",
        "epra_class": "Class C"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "easy",
        "question_text": "What is the minimum IP rating for a luminaire in bathroom zone 2?",
        "options": json.dumps(["IPX4", "IPX5", "IPX7", "IP44"]),
        "correct_answer": "IPX4",
        "explanation": "Zone 2 (0.6m from bath/shower edge) requires IPX4 minimum. This protects against splashing water from any direction.",
        "regulation_reference": "BS 7671 701.512.2",
        "practical_tip": "Zone 2 extends 0.6m horizontally from Zone 1 and to 2.25m height. Use enclosed fittings rated for bathroom use.",
        "epra_class": "Class C"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "medium",
        "question_text": "What must be included on an Electrical Installation Certificate?",
        "options": json.dumps(["Schedule of inspections, test results, installer details, and declaration", "Only the customer's name", "Just the test results", "The quotation and invoice"]),
        "correct_answer": "Schedule of inspections, test results, installer details, and declaration",
        "explanation": "An EIC must include: details of the installation, schedule of inspections, schedule of test results, and a signed declaration by the responsible person.",
        "regulation_reference": "BS 7671 644.1, Appendix 6",
        "practical_tip": "Use model forms from BS 7671 Appendix 6. Ensure all sections are completed - incomplete certificates are not valid.",
        "epra_class": "Class C"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "hard",
        "question_text": "What is the definition of a competent person under BS 7671?",
        "options": json.dumps(["Person with sufficient technical knowledge, experience, and skill to carry out the work safely", "Anyone with an EPRA license", "A university graduate", "Someone who has passed an exam"]),
        "correct_answer": "Person with sufficient technical knowledge, experience, and skill to carry out the work safely",
        "explanation": "BS 7671 defines a competent person as having adequate knowledge, experience, and understanding to perform electrical work safely and correctly.",
        "regulation_reference": "BS 7671 Part 2 Definitions",
        "practical_tip": "Competence includes: understanding BS 7671, practical installation skills, testing ability, and experience with the type of installation being worked on.",
        "epra_class": "Class C"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "easy",
        "question_text": "How often should portable appliances be PAT tested in a commercial environment?",
        "options": json.dumps(["Based on risk assessment - typically 1-4 years depending on equipment type", "Every month", "Every 6 months", "Never if they look OK"]),
        "correct_answer": "Based on risk assessment - typically 1-4 years depending on equipment type",
        "explanation": "PAT testing frequency depends on equipment type, usage, and environment. Hand-held tools may need annual testing, while stationary IT equipment may go 4 years.",
        "regulation_reference": "Code of Practice for In-Service Inspection and Testing of Electrical Equipment",
        "practical_tip": "Create a PAT testing schedule based on risk assessment. High-risk equipment (construction site tools) needs more frequent testing than low-risk (office computers).",
        "epra_class": "Class C"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "medium",
        "question_text": "What is Part P of the Building Regulations?",
        "options": json.dumps(["UK regulation requiring electrical work in dwellings to be safe - Kenya has similar local regulations", "Part of BS 7671 about protection", "Regulation about power factor", "Standard for portable appliances"]),
        "correct_answer": "UK regulation requiring electrical work in dwellings to be safe - Kenya has similar local regulations",
        "explanation": "Part P requires that electrical installations in dwellings are designed and installed safely. Kenya has similar requirements through EPRA and local authority building control.",
        "regulation_reference": "Building Regulations Part P (UK), Energy Act 2019 (Kenya)",
        "practical_tip": "In Kenya, major electrical work requires approval from EPRA and must be carried out by a licensed electrician with appropriate certification.",
        "epra_class": "Class C"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "hard",
        "question_text": "What classification code would you give to the absence of RCD protection on socket-outlets in a domestic EICR?",
        "options": json.dumps(["C3 - Improvement recommended (if installation predates RCD requirement)", "C1 - Danger present", "C2 - Potentially dangerous", "No code - not required"]),
        "correct_answer": "C3 - Improvement recommended (if installation predates RCD requirement)",
        "explanation": "If the installation predates the RCD requirement and was compliant at time of installation, missing RCD is C3. For new installations, it would be C2.",
        "regulation_reference": "Electrical Safety First Best Practice Guide, BS 7671 411.3.3",
        "practical_tip": "Always recommend RCD installation even if coded C3. It provides additional protection that could save lives.",
        "epra_class": "Class B"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "medium",
        "question_text": "What is the maximum period between issuing an EIC and notifying the relevant authority?",
        "options": json.dumps(["30 days in Kenya (check local requirements)", "7 days", "Immediately", "90 days"]),
        "correct_answer": "30 days in Kenya (check local requirements)",
        "explanation": "EPRA requires notification of electrical work within 30 days. The licensed electrician must submit certificates to both the client and EPRA.",
        "regulation_reference": "Energy Act 2019, EPRA Regulations",
        "practical_tip": "Submit paperwork promptly after completion. Late notification can result in penalties or invalidate insurance.",
        "epra_class": "Class C"
    },
    
    # Practical Scenario Questions
    {
        "category": "Regulations & Compliance",
        "difficulty": "hard",
        "question_text": "PRACTICAL: During an EICR, you discover the installation has no RCD protection on socket-outlets. The installation is from 2005. What code and action?",
        "options": json.dumps(["C2 - RCDs were required by 2005 (BS 7671:2001)", "C3 - improvement recommended", "C1 - immediately dangerous", "No code needed - too old"]),
        "correct_answer": "C2 - RCDs were required by 2005 (BS 7671:2001)",
        "explanation": "RCD protection for socket-outlets was introduced in BS 7671:2001. A 2005 installation should have had RCDs. Their absence is potentially dangerous (C2).",
        "regulation_reference": "BS 7671 411.3.3, Electrical Safety First Best Practice Guide",
        "practical_tip": "Know the timeline of regulation changes: RCDs for sockets became mandatory in 2001, consumer units must be non-combustible since 2015.",
        "epra_class": "Class B"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "medium",
        "question_text": "PRACTICAL: A client's landlord refuses to carry out recommended electrical repairs identified in your EICR. What should you do?",
        "options": json.dumps(["Document the refusal on the EICR and advise the tenant/client in writing", "Do nothing - it's the landlord's choice", "Report to the police", "Disconnect the supply"]),
        "correct_answer": "Document the refusal on the EICR and advise the tenant/client in writing",
        "explanation": "You cannot force repairs, but must document all dangerous conditions and recommendations. Inform the person ordering the report (and tenants if applicable) in writing.",
        "regulation_reference": "BS 7671 634.2, Professional Ethics",
        "practical_tip": "Keep copies of all correspondence. If C1 hazards exist, you have a professional duty to warn of immediate danger.",
        "epra_class": "Class C"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "easy",
        "question_text": "PRACTICAL: A new homeowner asks what electrical certificate they should have received from the builder. What do you tell them?",
        "options": json.dumps(["Electrical Installation Certificate (EIC) signed by a licensed electrician", "Just the Kenya Power bill", "A handwritten note from the builder", "No certificate is needed for new builds"]),
        "correct_answer": "Electrical Installation Certificate (EIC) signed by a licensed electrician",
        "explanation": "All new installations must have an EIC. This is a legal document proving the installation was designed, installed, and tested to BS 7671.",
        "regulation_reference": "BS 7671 644.1, Energy Act 2019",
        "practical_tip": "Without an EIC, the installation may not be insurable and could be difficult to sell. Always insist on proper documentation.",
        "epra_class": "Class C"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "hard",
        "question_text": "PRACTICAL: You are asked to install electrical wiring in a new building. The architect's plans show socket-outlets at 300mm above floor level. Is this compliant?",
        "options": json.dumps(["No - Part M requires 450mm minimum for new dwellings", "Yes - any height is acceptable", "Yes for commercial buildings only", "No - must be 600mm minimum"]),
        "correct_answer": "No - Part M requires 450mm minimum for new dwellings",
        "explanation": "Building Regulations Part M (accessibility) requires socket-outlets at minimum 450mm above finished floor level in new dwellings to ensure accessibility for all users.",
        "regulation_reference": "Building Regulations Part M (UK), Kenyan Building Code",
        "practical_tip": "Part M heights: sockets 450-1200mm, switches 1350-1450mm, consumer unit 1350-1450mm (or accessible). These apply to new builds, not rewires.",
        "epra_class": "Class C"
    },
    {
        "category": "Regulations & Compliance",
        "difficulty": "medium",
        "question_text": "PRACTICAL: A client wants you to install a socket-outlet in their bathroom for a hair dryer. Is this permitted?",
        "options": json.dumps(["No - socket-outlets are prohibited in rooms containing a bath or shower (except shaver sockets to BS 3535)", "Yes, with RCD protection", "Yes, if it's IP66 rated", "Yes, outside zone 2"]),
        "correct_answer": "No - socket-outlets are prohibited in rooms containing a bath or shower (except shaver sockets to BS 3535)",
        "explanation": "BS 7671 701.512.3 prohibits socket-outlets in rooms containing a bath or shower. Only shaver supply units complying with BS 3535 are permitted.",
        "regulation_reference": "BS 7671 701.512.3",
        "practical_tip": "This is absolute - even outside zones, standard socket-outlets are not allowed in bathrooms. The risk of extension leads into wet areas is too great.",
        "epra_class": "Class C"
    },

    # ========================
    # ISOLATION & SWITCHING (5 Theory + 3 Practical = 8)
    # ========================
    
    # Theory Questions
    {
        "category": "Isolation & Switching",
        "difficulty": "medium",
        "question_text": "What is the minimum isolation distance required for a main switch disconnector?",
        "options": json.dumps(["3mm contact gap", "1mm contact gap", "5mm contact gap", "10mm contact gap"]),
        "correct_answer": "3mm contact gap",
        "explanation": "BS 7671 requires a minimum 3mm contact separation for isolation purposes to ensure safe disconnection of all live conductors.",
        "regulation_reference": "BS 7671 537.2",
        "practical_tip": "Always verify isolation with an approved voltage tester before touching any conductors. Lock off and label the isolator.",
        "epra_class": "Class C"
    },
    {
        "category": "Isolation & Switching",
        "difficulty": "easy",
        "question_text": "What is the difference between isolation and switching?",
        "options": json.dumps(["Isolation disconnects for safety; switching is for functional control", "They are the same thing", "Isolation is for DC only", "Switching is for safety; isolation is for control"]),
        "correct_answer": "Isolation disconnects for safety; switching is for functional control",
        "explanation": "Isolation is the disconnection of a circuit for safety during maintenance. Switching is the normal on/off operation for functional control.",
        "regulation_reference": "BS 7671 537",
        "practical_tip": "An isolator must have a visible or clearly indicated break. A standard light switch provides functional switching, not safe isolation.",
        "epra_class": "Class C"
    },
    {
        "category": "Isolation & Switching",
        "difficulty": "hard",
        "question_text": "What is the purpose of a main linked switch in a consumer unit?",
        "options": json.dumps(["To isolate the entire installation with a single device", "To protect against overload", "To provide RCD protection", "To switch individual circuits"]),
        "correct_answer": "To isolate the entire installation with a single device",
        "explanation": "A main linked switch disconnects all live conductors (line and neutral for single-phase) simultaneously, providing safe isolation of the entire installation.",
        "regulation_reference": "BS 7671 537.1",
        "practical_tip": "The main switch should be easily accessible. In an emergency, anyone should be able to quickly turn off the entire installation.",
        "epra_class": "Class C"
    },
    {
        "category": "Isolation & Switching",
        "difficulty": "medium",
        "question_text": "Where should a firefighter's switch be installed for an illuminated sign?",
        "options": json.dumps(["At a height of 2.75m above ground on the external wall", "Inside the building near the sign", "At the main consumer unit", "Any accessible location"]),
        "correct_answer": "At a height of 2.75m above ground on the external wall",
        "explanation": "Firefighter's switches for external illuminated signs must be mounted externally at 2.75m above ground level for easy access by firefighters.",
        "regulation_reference": "BS 7671 537.6",
        "practical_tip": "The switch should be red in color and clearly labeled. It must isolate all live conductors to the sign.",
        "epra_class": "Class C"
    },
    {
        "category": "Isolation & Switching",
        "difficulty": "hard",
        "question_text": "What is emergency switching and when is it required?",
        "options": json.dumps(["Switching to remove danger in an emergency - required for motors, machines, and certain equipment", "Normal on/off switching", "Switching for maintenance", "Automatic switching by timers"]),
        "correct_answer": "Switching to remove danger in an emergency - required for motors, machines, and certain equipment",
        "explanation": "Emergency switching must quickly disconnect power to remove unexpected danger. Required for motor-driven equipment, heating appliances, and other machinery.",
        "regulation_reference": "BS 7671 537.4",
        "practical_tip": "Emergency stop buttons must be red with a yellow background, mushroom-headed, and latch when pressed. They must be easily accessible and clearly identified.",
        "epra_class": "Class B"
    },
    
    # Practical Scenario Questions
    {
        "category": "Isolation & Switching",
        "difficulty": "hard",
        "question_text": "PRACTICAL: You need to safely isolate a circuit for maintenance. You switch off the MCB. Is this sufficient for safe isolation?",
        "options": json.dumps(["No - must lock off, label, and verify with approved voltage tester. MCB alone is not safe isolation", "Yes - MCB provides adequate isolation", "Yes if it's a double-pole MCB", "Only if RCD is also off"]),
        "correct_answer": "No - must lock off, label, and verify with approved voltage tester. MCB alone is not safe isolation",
        "explanation": "Safe isolation requires: 1) Identify point of isolation, 2) Switch off, 3) Secure (lock off), 4) Label, 5) Prove tester, 6) Test for dead, 7) Prove tester again.",
        "regulation_reference": "BS 7671 537.2, HSE Safe Isolation Procedure",
        "practical_tip": "Use an approved voltage indicator (not a multimeter) for proving dead. Always test the tester before and after checking the circuit.",
        "epra_class": "Class C"
    },
    {
        "category": "Isolation & Switching",
        "difficulty": "medium",
        "question_text": "PRACTICAL: A client's consumer unit main switch only breaks the line conductor, not neutral (single-pole). The installation is TN-C-S. Is this acceptable?",
        "options": json.dumps(["No - main switch must isolate all live conductors (line AND neutral) for TN systems", "Yes - single pole is fine", "Yes for domestic only", "Only if RCD protected"]),
        "correct_answer": "No - main switch must isolate all live conductors (line AND neutral) for TN systems",
        "explanation": "BS 7671 requires the main switch to disconnect all live conductors. For single-phase, this means both line and neutral. A single-pole switch is non-compliant.",
        "regulation_reference": "BS 7671 537.1.3",
        "practical_tip": "Always install a double-pole main switch. This ensures complete isolation even if the supply polarity is reversed.",
        "epra_class": "Class C"
    },
    {
        "category": "Isolation & Switching",
        "difficulty": "easy",
        "question_text": "PRACTICAL: A workshop has a 3-phase distribution board. How do you verify complete isolation before working on it?",
        "options": json.dumps(["Test all three phases and neutral to earth with approved voltage tester after locking off main switch", "Just turn off the main switch", "Check one phase only", "Remove the fuses"]),
        "correct_answer": "Test all three phases and neutral to earth with approved voltage tester after locking off main switch",
        "explanation": "All conductors must be tested for dead: L1-E, L2-E, L3-E, L1-N, L2-N, L3-N, N-E. Use an approved voltage indicator and prove it before and after testing.",
        "regulation_reference": "BS 7671 537.2, HSE Guidance Note GS38",
        "practical_tip": "On 3-phase boards, be aware that some circuits may be fed from different sources. Always test every conductor before touching.",
        "epra_class": "Class C"
    },

    # ========================
    # TOOLS & EQUIPMENT (4 Theory + 2 Practical = 6)
    # ========================
    
    # Theory Questions
    {
        "category": "Tools & Equipment",
        "difficulty": "easy",
        "question_text": "What instrument is used to measure insulation resistance?",
        "options": json.dumps(["Insulation resistance tester (megohmmeter)", "Multimeter", "Clamp meter", "Earth loop tester"]),
        "correct_answer": "Insulation resistance tester (megohmmeter)",
        "explanation": "An insulation resistance tester applies a DC voltage (typically 500V for 230V circuits) and measures the resistance in megohms (MΩ).",
        "regulation_reference": "BS 7671 643.3",
        "practical_tip": "Never use a standard multimeter for IR testing. It doesn't apply the required test voltage and gives inaccurate readings.",
        "epra_class": "Class C"
    },
    {
        "category": "Tools & Equipment",
        "difficulty": "medium",
        "question_text": "What is the purpose of a proving unit?",
        "options": json.dumps(["To verify that a voltage tester is working correctly before and after testing for dead", "To test RCDs", "To measure earth resistance", "To calibrate multimeters"]),
        "correct_answer": "To verify that a voltage tester is working correctly before and after testing for dead",
        "explanation": "A proving unit provides a known voltage to confirm the voltage tester is functioning correctly. This is essential for safe isolation procedures.",
        "regulation_reference": "BS 7671 643.1, HSE GS38",
        "practical_tip": "Always prove your tester before and after testing for dead. A faulty tester could show 'dead' when the circuit is actually live - potentially fatal.",
        "epra_class": "Class C"
    },
    {
        "category": "Tools & Equipment",
        "difficulty": "hard",
        "question_text": "What is the minimum test current required for a low-resistance ohmmeter used for continuity testing?",
        "options": json.dumps(["200mA", "50mA", "500mA", "10mA"]),
        "correct_answer": "200mA",
        "explanation": "BS 7671 requires a test current of at least 200mA for continuity testing of protective conductors to ensure reliable measurement of low resistances.",
        "regulation_reference": "BS 7671 643.4",
        "practical_tip": "A standard multimeter typically provides only 1mA test current, which is insufficient for reliable continuity testing. Use a dedicated low-resistance ohmmeter.",
        "epra_class": "Class C"
    },
    {
        "category": "Tools & Equipment",
        "difficulty": "easy",
        "question_text": "What tool is used to confirm correct phase rotation on a 3-phase supply?",
        "options": json.dumps(["Phase rotation meter", "Voltmeter", "Ammeter", "Insulation tester"]),
        "correct_answer": "Phase rotation meter",
        "explanation": "A phase rotation meter indicates whether phases are connected in the correct sequence (L1-L2-L3 clockwise). Incorrect rotation can cause motors to run backwards.",
        "regulation_reference": "BS 7671 643.7",
        "practical_tip": "Always check phase rotation when connecting 3-phase equipment. Label phases clearly for future reference.",
        "epra_class": "Class C"
    },
    
    # Practical Scenario Questions
    {
        "category": "Tools & Equipment",
        "difficulty": "hard",
        "question_text": "PRACTICAL: Your insulation resistance tester's battery is low. You need to test a circuit urgently. Can you use your multimeter instead?",
        "options": json.dumps(["No - multimeter cannot provide the required 500V DC test voltage for insulation testing", "Yes - multimeter resistance range works fine", "Yes for low voltage circuits", "Only if it's a digital multimeter"]),
        "correct_answer": "No - multimeter cannot provide the required 500V DC test voltage for insulation testing",
        "explanation": "Insulation testing requires a specific test voltage (500V DC for 230V circuits). A multimeter operates at low voltage and cannot detect insulation breakdown that only occurs at higher voltages.",
        "regulation_reference": "BS 7671 643.3, Table 61",
        "practical_tip": "Using a multimeter for IR testing gives dangerously misleading results. Always use a properly functioning insulation resistance tester with adequate battery power.",
        "epra_class": "Class C"
    },
    {
        "category": "Tools & Equipment",
        "difficulty": "medium",
        "question_text": "PRACTICAL: You are testing a ring final circuit. You measure r1=0.40Ω, rn=0.41Ω, r2=0.66Ω. The expected r2 is 0.67Ω (r1 × 1.67). Is the ring OK?",
        "options": json.dumps(["Yes - r1≈rn and r2 is within 2% of expected value", "No - r1 and rn differ slightly", "No - r2 should be exactly 0.67Ω", "Retest with different instrument"]),
        "correct_answer": "Yes - r1≈rn and r2 is within 2% of expected value",
        "explanation": "r1 and rn should be approximately equal (within 0.05Ω is acceptable). r2/r1 ratio = 0.66/0.40 = 1.65, close to theoretical 1.67. Ring is continuous and correctly wired.",
        "regulation_reference": "BS 7671 Guidance Note 3",
        "calculation_steps": "1. r1 ≈ rn (0.40 ≈ 0.41) ✓\n2. Expected r2 = 0.40 × 1.67 = 0.668Ω\n3. Actual r2 = 0.66Ω\n4. Difference = 0.008Ω (1.2%)\n5. Within acceptable tolerance ✓",
        "practical_tip": "Small variations in r1/rn are normal due to terminal resistance. Variations >0.05Ω suggest poor connections. Large r2 variations suggest wrong CPC size or broken ring.",
        "epra_class": "Class C"
    },
]

# ============================================================
# DATABASE SEEDING FUNCTION
# ============================================================

def seed_database():
    """Seed the database with all 160 EPRA exam questions"""
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Count existing questions
        existing_count = Question.query.count()
        print(f"Existing questions in database: {existing_count}")
        
        # Add questions
        questions_added = 0
        questions_skipped = 0
        
        for q_data in questions_data:
            # Check if question already exists (by question text)
            existing = Question.query.filter_by(question_text=q_data["question_text"]).first()
            if not existing:
                question = Question(**q_data)
                db.session.add(question)
                questions_added += 1
            else:
                questions_skipped += 1
        
        db.session.commit()
        
        total_questions = Question.query.count()
        print(f"\n✓ Database seeding complete!")
        print(f"✓ {questions_added} new questions added")
        print(f"✓ {questions_skipped} duplicate questions skipped")
        print(f"✓ Total questions in database: {total_questions}")
        
        # Show breakdown by category
        from sqlalchemy import func
        categories = db.session.query(Question.category, func.count(Question.id)).group_by(Question.category).all()
        print("\n📊 Questions by Category:")
        for category, count in categories:
            print(f"   {category}: {count}")
        
        # Count theory vs practical
        theory_count = Question.query.filter(~Question.question_text.like('PRACTICAL:%')).count()
        practical_count = Question.query.filter(Question.question_text.like('PRACTICAL:%')).count()
        print(f"\n📝 Theory Questions: {theory_count}")
        print(f"🔧 Practical Scenarios: {practical_count}")

if __name__ == "__main__":
    seed_database()

