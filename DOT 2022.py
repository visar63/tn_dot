# coded by Visar.
import csv
import re
import time

header = [
    'CompanyName', 'City', 'State', 'Zip',
    'Owner_Name',
    'phone',
    'Email', 
    'Website',
    'Certfication',
    'CompanyType',
    'County',
    'Speciality',
    'NAICS_List', 
]

Owner_Name = ''

with open(r"C:\Users\Pc\Desktop\AAA Qcing\TN DOT (Div)_Scripts\Scripts\Report.html", "r", encoding="utf8") as f:
    content1 = f.read()
    # print (content1)

    with open(f"TN DOT.csv", "at", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
    
        count = 0
        # for company in re.findall(r'(formation</span></div>.*?">Company In)', str(content1), re.I|re.S):
        for company in re.findall(
            r'(>Company Information</span></div>.*?(?:<div style="position:absolute;left:38\.|<div style="position:absolute;left:50%))',
            str(content1),
            re.I | re.S,
        ):
            count = count + 1
            phone = re.search(
                r"(>(\(?[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4})</span>)",
                str(company),
                re.I | re.S,
            )
            if phone:
                phone = phone.group(2)
            
            NAICS_List = re.search(
                r'(>NAICS List</span></div>(.*?)(?:<div style="position:absolute;left:38\.|<div style="position:absolute;left:50%))',
                str(company),
                re.I | re.S,
            )
            if NAICS_List:
                NAICS_List = NAICS_List.group(2)
                NAICS_List = re.sub(r"<.*?>", " ", NAICS_List)
                NAICS_List = re.sub(r"\t", " ", NAICS_List)
                NAICS_List = re.sub(r"\n", " ", NAICS_List)
                NAICS_List = re.sub(r"\s{2,}", " ", NAICS_List)
                NAICS_List = NAICS_List.strip()
            
            Speciality = re.search(
                r'Specialty</span></div>(.*?)<div style="position:absolute;left:\d+.\d+px;top:\d+.\d+px" class="cls_\d+"><span class="cls_\d+">NAICS List',
                str(company),
                re.I | re.S,
            )
            if Speciality:
                Speciality = Speciality.group(1)
                Speciality = re.sub(r"<.*?>", " ", Speciality)
                Speciality = re.sub(r"\t", " ", Speciality)
                Speciality = re.sub(r"\n", " ", Speciality)
                Speciality = re.sub(r"\s{2,}", " ", Speciality)
                Speciality = Speciality.strip()
            
            Owner_Name = re.search(r'<div style="position:absolute;left:359.64px;top:\d+\.\d+px" class="cls_\d+"><span class="cls_\d+">(\D+, \D+)</span>',str(company),re.I | re.S)
            if Owner_Name:
                Owner_Name = Owner_Name.group(1)

            Email = re.search(
                r'>\s*([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6})\s*<',
                str(company),
                re.I | re.S,
            )
            if Email:
                Email = Email.group(1)
            
            Website = re.search(r'<A HREF="([^"]*)">', str(company), re.I | re.S)
            if Website:
                Website = Website.group(1)
            
            Certfication = ""
            for cert in re.findall(r'<div style="position:absolute;left:23\d\.\d+px;top:\d+\.\d+px" class="cls_\d+"><span class="cls_\d+">([^<]+)</span>', company, re.I|re.S):
                cert = cert + " "
                Certfication += cert
            Certfication = Certfication.rstrip()

            CompanyType = re.search(r'<div style="position:absolute;left:26\d\.\d+px;top:\d+\.\d+px" class="cls_\d+"><span class="cls_\d+">([^<]+)</span>',str(company),re.I | re.S)
            if CompanyType:
                CompanyType = CompanyType.group(1)
                ptrr = re.search(r'(.*?)\s{3,}(.*)', CompanyType, re.I|re.S)
                if ptrr:
                    Owner_Name = ptrr.group(2)
                    CompanyType = ptrr.group(1)

            County = ""
            for cnty in re.findall(r'<div style="position:absolute;left:16\d\.\d+px;top:\d+\.\d+px" class="cls_\d+"><span class="cls_\d+">([^:]+)</span>', company, re.I|re.S):
                cnty = cnty + "  "
                County += cnty
            County = County.rstrip()

            CompanyName = ""
            for cn in re.findall(r'<div style="position:absolute;left:19\.\d+px;top:\d+\.\d+px" class="cls_\d+"><span class="cls_\d+">([^<]+)</span>', company, re.I|re.S):
                cn = cn + ";  "
                CompanyName += cn
            CompanyName = CompanyName.rstrip()

            City = State = Zip = ""
            CSZ = re.search(r'<div style="position:absolute;left:(?:20|23)\.\d+px;top:\d+\.\d+px" class="cls_\d+"><span class="cls_\d+">([^,]+)(?:, [A-Z]{2})?, ([A-Z]{2}) ([^<]+)</span>', str(company), re.I | re.S)
            CSZ2 = re.search(r'<div style="position:absolute;left:(?:20|23)\.\d+px;top:\d+\.\d+px" class="cls_\d+"><span class="cls_\d+">([^,]+), ([A-Z]{2})(?: ([^<]+))?</span>', str(company), re.I | re.S)
            CSZ3 = re.search(r'<div style="position:absolute;left:\d\d\.\d+px;top:\d+\.\d+px" class="cls_\d+"><span class="cls_\d+">(\d{5})(?:-\d{4})?</span>', str(company), re.I | re.S)
            if CSZ:
                City = CSZ.group(1)
                State = CSZ.group(2)
                Zip = CSZ.group(3)
            elif CSZ2:
                City = CSZ2.group(1)
                State = CSZ2.group(2)
            # elif CSZ3:
            #     Zip = CSZ3.group(1)
                if Zip is "":
                    CSZ3 = re.search(r'<div style="position:absolute;left:\d\d\.\d+px;top:\d+\.\d+px" class="cls_\d+"><span class="cls_\d+">(\d{5})(?:-\d{4})?</span>', str(company), re.I | re.S)
                    if CSZ3:
                        Zip = CSZ3.group(1)
                
                
            

            # Website = re.search(
            #     r'<A HREF="([^"]*)">',
            #     str(company),
            #     re.I | re.S,
            # )
            # if Website:
            #     Website = Website.group(1)



            data = [
                CompanyName,
                City, State, Zip,
                Owner_Name,
                phone,
                Email,
                Website,
                Certfication,
                CompanyType,
                County,
                Speciality,
                NAICS_List,
                
            ]
            writer.writerow(data)
            
            print("----------------------------\n")
            print(Owner_Name)
            print(phone)
            print(Email)
            print("*** Count:  {} ***".format(count))

            Owner_Name = phone = Speciality =  NAICS_List = Email = Website = Certfication = CompanyType = County  = ""
