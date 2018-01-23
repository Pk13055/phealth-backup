Step 1:
add data in role table
    {
        role: Clinic, rolecode: HP,
        role: Hospital, rolecode: HP,
        role: DiagnosticCentre, rolecode: HP,
        role: Healthseeker, rolecode: HS,
        role: SalesAgents, rolecode: SALES,
        role: Resellers, rolecode: SALES,
        role: admin, rolecode: admin
    }

usertype: pass the roles where role code is HP

Onsubmit check the unique of email & mobile 
create a otp save in session & send it to the email & mobile 
Show step2.0
On submit Otp verify with the session 
Show step 2.1 
On submit the password & confirm match
Insert in users table
redirect to step 3
fetch the details & set the sessions as the user loged in
step 3
show the name,mobile,email, ask upload image(Optional)
On submit save 
Step 4
On submit update the location lat and long only not needed city country, state

Plugins to be added for multi image upload


Add columns to table of healthproviders
establishedyear,
beds

Step 5:
On click add branch repeat step 4
Step 6:
add data in speciality_type table
    {
        speciality_type_name: DiagnosticCentre,
        speciality_type_name: Hospital,
        speciality_type_name: Clinic,
    }
add data in speciality table
    {
        speciality: Anaesthesiology & Emergency Medicine,
        speciality: Ayurvedic,
        speciality: Cardio Thorasic Surgery,
        speciality: Cochlar Implant Surgery,
        speciality: Cardiology,
        speciality: Anaesthesiology & Emergency Medicine
    }
show Specialities Available select * from speciality and display

On submit save it in healthproviders_speciality

Setp 7:
add data in facilities_services table
    {
      facilities_services: Pharmacy 24 Hours,facilities_id: 1,
      facilities_services: Ambulance,facilities_id: 1,
      facilities_services: Day Time,facilities_id: 1,
    }
add data in facilities table
    {
      facilitity: Out Patient,
      facilitity: In Patient,
      facilitity: Casuality / Emergency,
    }
on submit insert in availablefacilities
Same way insert dummy data in test, category, subcategory


Step8:
Enter the discounts
Show the selected speciality here in select speciality


Step 9:
On submit Insert in healthchecks table
Add columns to table of healthchecks
Sharetoad


step10:

Fill some dummy data in plans and group plans
