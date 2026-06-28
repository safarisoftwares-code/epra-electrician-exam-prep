from app import app, db
from models import Question
import json

questions = [
    {"category":"safety","difficulty":"medium","question_text":"Minimum IP rating for bathroom zone 1?","options":json.dumps(["IPX4","IPX5","IPX7","IP44"]),"correct_answer":"IPX4","explanation":"Zone 1 needs IPX4. Zone 0 needs IPX7.","regulation_reference":"BS 7671 Section 701","practical_tip":"Check the bathroom zone chart before installing!","epra_class":"Class C"},
    {"category":"safety","difficulty":"hard","question_text":"Max disconnection time for 230V final circuit <=32A on TN system?","options":json.dumps(["0.4s","5s","0.2s","1s"]),"correct_answer":"0.4s","explanation":"0.4 seconds for final circuits <=32A on TN.","regulation_reference":"BS 7671 Table 41.1","practical_tip":"Test RCDs with proper tester, not just the button!","epra_class":"Class C"},
    {"category":"installation","difficulty":"easy","question_text":"Minimum bending radius for PVC cables?","options":json.dumps(["4x dia","6x dia","8x dia","10x dia"]),"correct_answer":"6x dia","explanation":"PVC cables need 6x diameter bend radius.","regulation_reference":"BS 7671 522.8.3","practical_tip":"If tighter than your fist, it's too sharp!","epra_class":"Class C"},
    {"category":"calculations","difficulty":"hard","question_text":"Voltage drop: 2.5mm2 cable, 20A, 30m (mV/A/m=18)?","options":json.dumps(["10.8V","8.6V","12.4V","5.4V"]),"correct_answer":"10.8V","explanation":"Vd=(18x20x30)/1000=10.8V (4.5%)","regulation_reference":"BS 7671 App 4","calculation_steps":json.dumps(["Vd=(mV/A/m x I x L)/1000","=(18x20x30)/1000","=10.8V"]),"practical_tip":"Use the formula for accuracy!","epra_class":"Class C"},
    {"category":"testing","difficulty":"medium","question_text":"Correct initial verification test sequence?","options":json.dumps(["Continuity,IR,Polarity,EFLI,RCD","IR,Cont,RCD,Pol,EFLI","Pol,Cont,EFLI,IR,RCD","RCD,EFLI,Cont,IR,Pol"]),"correct_answer":"Continuity,IR,Polarity,EFLI,RCD","explanation":"CIPELR: First 3 DEAD, last 2 LIVE.","regulation_reference":"BS 7671 Part 6","practical_tip":"CIPELR = Continuity, Insulation, Polarity, Earth Loop, RCD!","epra_class":"Class C"},
    {"category":"kenya_power","difficulty":"easy","question_text":"Standard single-phase voltage from Kenya Power?","options":json.dumps(["240V","230V","220V","250V"]),"correct_answer":"240V","explanation":"Kenya Power: 240V/415V, 50Hz.","regulation_reference":"Kenya Power Standard","practical_tip":"Always measure on site - can be 220-250V!","epra_class":"Class C"},
    {"category":"earthing","difficulty":"hard","question_text":"Max Zs for 32A Type B MCB on TN at 230V?","options":json.dumps(["1.44ohm","1.15ohm","0.72ohm","2.30ohm"]),"correct_answer":"1.44ohm","explanation":"Zs=230/(32x5)=1.44ohm (design:1.15ohm)","regulation_reference":"BS 7671 Table 41.3","practical_tip":">1.15ohm on 32A? Investigate connections!","epra_class":"Class C"},
    {"category":"safety","difficulty":"medium","question_text":"RCD rating for socket-outlet protection?","options":json.dumps(["30mA","100mA","300mA","10mA"]),"correct_answer":"30mA","explanation":"30mA protects people. 100mA for fire, 300mA for equipment.","regulation_reference":"BS 7671 411.3.3","practical_tip":"30mA = Life Safety!","epra_class":"Class C"},
    {"category":"regulations","difficulty":"easy","question_text":"Certificate for new installations in Kenya?","options":json.dumps(["Completion Certificate","EPRA License","KP Form","Local Permit"]),"correct_answer":"Completion Certificate","explanation":"Required before Kenya Power connects supply.","regulation_reference":"Energy Act 2019","practical_tip":"Never energize without this certificate!","epra_class":"Class C"},
    {"category":"safety","difficulty":"easy","question_text":"Line conductor color in NEW installations?","options":json.dumps(["Brown","Red","Black","Blue"]),"correct_answer":"Brown","explanation":"New: Brown=Line, Blue=Neutral, G/Y=Earth.","regulation_reference":"BS 7671","practical_tip":"Red=old installation. Document it!","epra_class":"Class C"}
]

with app.app_context():
    db.create_all()
    Question.query.delete()
    for q in questions:
        db.session.add(Question(**q))
    db.session.commit()
    print(f"Seeded {len(questions)} questions!")

print("Database ready!")
