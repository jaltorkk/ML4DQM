from flask import Flask, render_template, request, send_file,redirect,url_for, Response, redirect

app = Flask(__name__,static_folder="static", template_folder="templates")
import sys
import os

@app.route('/', methods=['GET','POST'])



def Menu_func():
    import os
    #capitalLet = os.environ['AWS_PASS']
    #smallLet = os.environ['aws-pass']
    

    #if request.method == 'POST':
    
        #Request form 3.0 hvis:
        #Request form 2.0 hvis:

        #Input_str = str(request.form['GoogleSearch'])
        #Input_str.replace(' ','+')
        
        #return redirect(google_url_1+Input_str+google_url_2,code=302)
    
    return render_template('Frontpage.html')



@app.route('/Quizpage', methods=['GET','POST'])
def Quizpage():

    Soeren_datascience = ["1_3","1_4","1_6","2_1","2_3","2_6","5_2","5_3","5_5","3_2","4_1","4_2"]
    Isabel_datascience = ["1_3","1_4","1_5","2_1","2_6","5_1","5_3","3_3","4_5","4_4",]
    
    Linnea_UX = ["1_2","1_4","1_9","2_1","2_4","2_6","5_1","5_3","3_2","4_3","4_11","4_1"]
    Jens_UX = ["1_2","1_5","1_9","2_2","2_6","2_3","5_1","5_2","3_2","4_1","4_11"]

    Daniel_udvikler = ["1_1","1_6","1_10","2_1","2_2","2_6","5_3","5_6","3_1","4_1","4_2","4_3"]
    Cathrine_udvikler = ["1_2","1_6","1_9","2_3","2_6","5_3","5_6","3_3","4_4","4_7"]

    Niklas_management = ["1_3","1_5","1_9","2_2","2_6","5_1","5_2","5_5","3_5","4_1","4_2"]
    Jeppe_management = ["1_4","1_5","1_9","2_3","2_6","5_5","3_5","4_3","4_8"]
    
    Sebastian_Industry = ["1_4","1_11","1_5","2_6","2_2","2_4","5_1","5_5","3_5","4_3","4_8"]
    Rasmus_Indsutry = ["1_4","1_11","1_5","2_3","2_1","2_4","5_1","5_4","3_4","4_5","4_11"]

    Nicolaj_automation = ["1_1","1_2","1_4","1_10","2_1","2_2","2_6","5_1","5_3","3_1","4_1","4_3"]
    Morten_automation = ["1_10","2_1","2_6","5_1","5_6","3_2","4_2","4_8",]

    Yasmin_graduate = ["1_5","1_9","1_10","2_1","2_6","5_1","5_6","3_2","4_7","4_11","4_10"]
    Philip_management = ["1_1","1_5","1_9","2_3","2_6","5_1","5_2","3_5","4_2","4_6"]

    Peter_automation = ["1_4","1_5","1_10","2_1","2_4","5_1","5_2","5_5","3_5","4_1","4_10",""]




    if request.method == 'POST':

        #--------------Request filled form-----------------#

        q0_1 = request.form["opt1radio"]
        q1_1 = request.form.getlist('question1_1')
        q2_1 = request.form.getlist('question2_1')
        q3_1 = request.form.getlist('question3_1')
        q4_1 = request.form.getlist('question4_1')
        q5_1 = request.form.getlist('question5_1')


        result_list = []
        Peter_score = 0
        Philip_score = 0
        Yasmin_score = 0
        Morten_score = 0
        Nicolaj_score = 0
        Soeren_score = 0
        Isabel_score = 0
        Linnea_score = 0
        Jens_score = 0
        Daniel_score = 0
        Cathrine_score = 0
        Niklas_score = 0
        Jeppe_score = 0
        Sebastian_score = 0
        Rasmus_score = 0
        Final_result = ""

        #-----Loop through & collect list answers----------#        

        for i in q1_1:
            result_list.append(i)
        for s in q2_1:
            result_list.append(s)
        for d in q3_1:
            result_list.append(d)
        for a in q4_1:
            result_list.append(a)
        for c in q5_1:
            result_list.append(c)

        #--------Match score with candidates--------------#

        for a in result_list:
            if a in Soeren_datascience:
                Soeren_score = Soeren_score + 1
        
        for a in result_list:
            if a in Isabel_datascience:
                Isabel_score = Isabel_score + 1
        
        for a in result_list:
            if a in Linnea_UX:
                Linnea_score = Linnea_score + 1
        
        for a in result_list:
            if a in Jens_UX:
                Jens_score = Jens_score + 1

        for a in result_list:
            if a in Daniel_udvikler:
                Daniel_score = Daniel_score + 1
            
        for a in result_list:
            if a in Cathrine_udvikler:
                Cathrine_score = Cathrine_score + 1

        for a in result_list:
            if a in Niklas_management:
                Niklas_score = Niklas_score + 1

        for a in result_list:
            if a in Jeppe_management:
                Jeppe_score = Jeppe_score + 1
        
        for a in result_list:
            if a in Sebastian_Industry:
                Sebastian_score = Sebastian_score + 1
        
        for a in result_list:
            if a in Rasmus_Indsutry:
                Rasmus_score = Rasmus_score + 1

        for a in result_list:
            if a in Nicolaj_automation:
                Nicolaj_score = Nicolaj_score + 1

        for a in result_list:
            if a in Morten_automation:
                Morten_score = Morten_score + 1

        for a in result_list:
            if a in Yasmin_graduate:
                Yasmin_score = Yasmin_score + 1

        for a in result_list:
            if a in Philip_management:
                Philip_score = Philip_score + 1

        for a in result_list:
            if a in Peter_automation:
                Peter_score = Peter_score + 1
        

        ##Add extra point to practice
        if q0_1 == "Software":
            Daniel_score = Daniel_score + 3
            Cathrine_score = Cathrine_score + 3
            Nicolaj_score = Nicolaj_score + 2

        elif q0_1 == "Design":
            Linnea_score = Linnea_score + 3
            Jens_score = Jens_score + 3

        elif q0_1 == "Management":
            Jeppe_score = Jeppe_score + 3
            Niklas_score = Niklas_score + 3
            Yasmin_score = Yasmin_score + 3
            Philip_score = Philip_score + 3
            Peter_score = Peter_score + 3
            
            
        elif q0_1 == "Datascience":
            Soeren_score = Soeren_score + 3
            Isabel_score = Isabel_score +3

        elif q0_1 == "Robotics":
            Sebastian_score = Sebastian_score + 3
            Rasmus_score = Rasmus_score + 3
        

        


        print(Daniel_score,Soeren_score,Jens_score,Cathrine_score,Jeppe_score,Niklas_score,Sebastian_score,Morten_score,Philip_score,Yasmin_score,Peter_score,Rasmus_score,Isabel_score)

        score_list = []

        score_list.append(Linnea_score)
        score_list.append(Jens_score)
        score_list.append(Daniel_score)
        score_list.append(Cathrine_score)
        score_list.append(Niklas_score)
        score_list.append(Jeppe_score)
        score_list.append(Soeren_score)
        score_list.append(Rasmus_score)
        score_list.append(Sebastian_score)
        score_list.append(Isabel_score)
        score_list.append(Nicolaj_score)
        score_list.append(Morten_score)
        score_list.append(Yasmin_score)
        score_list.append(Philip_score)
        score_list.append(Peter_score)


        max = 0

        for i in score_list:
            if i > max:
                max=i        
                winner = score_list.index(max)
                if winner == 0:
                    Final_result = "Linnea"
                    Img_Result = "Linnea.png"
                    disc_result = "Du minder om mig! Jeg hedder Linnea og er UX Designer i IBM Client Innovation Center. Jeg har en bachelor i Information Management og en kandidat i Service Design. Min opgave er at være brugernes ambassadør og designe koncepter og løsninger, der giver værdi for mennesker. Jeg laver fx research, workshopfacilitering, wireframing og brugertesting. Mine hobbies er keramik og andre kreative projekter, samt gåture i naturen med min hund. I mit arbejde værdsætter jeg et godt socialt fællesskab, innovative rammer og at hver dag kan se helt forskellig ud"
                elif winner == 1:
                    Final_result = "Jens"
                    Img_Result = "Jens.png"
                    disc_result = "Jeg hedder Jens og er UX Designer. Jeg har en bachelor i kommunikation og digitale medier og en kandidat i Information Studies. På mit projekt er jeg inde over mange opgaver af forskellig art. Jeg designer løsninger til vores kunders brugere, med udgangspunkt i deres behov, så mine arbejdsopgaver involverer i høj grad user research, prototyping og user testing. Jeg er vild med stort set al sport – både at se og udøve – og så spiser jeg gerne god mad i godt selskab. Jeg værdsætter i høj grad mine kollegaer, og det sammenhold vi har i CIC’et. Folk er altid villige til at hjælpe, og der er et stort socialt engagement i centeret. Derudover kan jeg godt lide projekternes forskellighed og det tætte samarbejde med højtstående profiler såsom partnere, hvor man virkelig kan suge læring til sig."
                elif winner == 2:
                    Final_result = "Daniel"
                    Img_Result = "Daniel.png"
                    disc_result = "Du minder om mig! Jeg hedder Daniel og er Software-udvikler i IBM Client Innovation Center. Jeg er uddannet datamatiker fra KEA og sidder til daglig som udvikler på bl.a. monitoreringsprojekter hos vores kunder. Jeg elsker at udvikle og bruger meget af min fritid på det – udover at løfte tunge vægte i ny og næ. Noget af det, jeg sætter mest pris på i min hverdag er samarbejdet med mine kolleger og vores fællesskab – det er spitzenklasse!"
                elif winner == 3:
                    Final_result = "Cathrine"
                    Img_Result = "Cathrine.png"
                    disc_result = "Du minder om mig! Jeg hedder Cathrine og er Frontend-udvikler i IBM Client Innovation Center. Jeg er har en bachelor i HA(kom.) fra CBS og en kandidat i Software Development fra ITU. Til daglig sidder jeg og udvikler i React, JavaScript, HTML og CSS, hvor vi løbende har demoer af produktet hos kunden. I min fritid nyder jeg at være aktiv og dyrker både løb (blandt andet i CIC’ets løbeklub), crossfit og anden yoga/pilates inspireret træning. Jeg sætter stor pris på at kunne kombinere min tekniske kompetencer med min kommunikationsbaggrund som konsulent i IBM Client Innovation Center."
                elif winner == 4:
                    Final_result = "Niklas"
                    Img_Result = "Niklas.png"
                    disc_result = "Du minder om mig! Jeg hedder Niklas og er Projektleder i IBM Client Innovation Center. Jeg har en kandidat i Information Management fra Aarhus Universitet BSS og arbejder til daglig også som Scrum Master og Agil Coach. Mit arbejde består meget af at netværke og skabe transformationer hos vores forskellige kunder. I min fritid bruger jeg meget til på at game, dyrke fitness og hygge med mine kære. Det jeg sætter mest pris på ved mit arbejder er det unge, ambitiøse kollegaskab, som samtidig har stort fokus på en sjov og stressfri arbejdsplads"
                elif winner == 5:
                    Final_result = "Jeppe"
                    Img_Result = "Jeppe.png"
                    disc_result = "Du minder om mig! Jeg hedder Jeppe og er IT Business konsulent i IBM Client Innovation Center. Jeg er uddannet cand.merc i Digital Transformation fra Aarhus Universitet BSS. Til hverdag er jeg Product Owner, hvor jeg leder et cross-functional team af både udviklere, forretningsfolk og testere i et Scaled Agile Framework setup. Min fornemmeste opgave er at binde forretning og IT sammen, så teamet leverer mest mulig værdi. I min fritid spiller jeg en del tennis. Det fedeste ved mit job er mine fantastiske kolleger – vi hardet utrolig sjovt. I min nuværende rolle får jeg lov til at drive innovationsagendaen, og er samtidig involvereti det digitale strategiarbejde, hvilket jeg synes, er virkelig spændende"
                elif winner == 6:
                    Final_result = "Søren"
                    Img_Result = "Soeren.png"
                    disc_result = "Du minder om mig! Jeg hedder Søren og er Data Scientist i IBM Client Innovation Center. Jeg har en kandidat i kvantitativ økonomi fra Aarhus Universitet og hjælper til daglig vores kunder med at bruge deres data på en smartere måde ved hjælp af de nyeste teknologier indenfor AI og Machine Learning. I min fritid går jeg op i mine venner, mad og golf – gerne samtidig! Det bedste ved mit job er at arbejde sammen med de sejeste mennesker og bidrage med nyskabende løsninger"
                elif winner == 7:
                    Final_result = "Rasmus"
                    Img_Result = "Rasmus.png"
                    disc_result = "Du minder om mig! Jeg hedder Rasmus og er Industry 4.0 konsulent i IBM Client Innovation Center. Jeg haren baggrund som civilingeniør indenfor Operations og Innovations Management – primært fokuseret på procesoptimering og virksomhedsstrategi. Jeg fokuserer på nuværende tidspunkt på at opbygge vores team, lægge strategier og udvikle produkter. Udenfor arbejdet har jeg en stor passion for sport og filmproduktion. Det jeg nyder allermest ved mit arbejde er, at man får muligheden for at arbejde med de ting, man er passioneret omkring, samtidig med at menneskene her er fantastiske"
                elif winner == 8:
                    Final_result = "Sebastian"
                    Img_Result = "Sebastian.png"
                    disc_result = "Du minder om mig! Jeg hedder Sebastian og er Industry 4.0 konsulent i IBM Client Innovation Center. Jeg eruddannet civilingeniør i Manufacturing Technology fra Aalborg Universitet med fokus på Digital Manufacturing og kunstigt intelligente robotter. Jeg er den sporty gamer-type, der kan finde på at bure mig inde en hel weekend og holde LAN-party med gutterne – men som samtig kan gå helt i spåner over ikke at fåtrænet. Jeg bruger meget tid med familie og venner, og gerne aktiviteter der inkluderer fysisk aktivitet såsom padel tennis. Jeg elsker at bruge penge på rejser til svedige destinationer og skiferier – livet handler ikke kun om at arbejde, og det er der plads til her."
                elif winner == 9:
                    Final_result = "Isabel"
                    Img_Result = "Isabel.png"
                    disc_result = "Du minder og mig! Jeg hedder Isabel og er kombineret Data Scientist og projektleder i IBM Client Innovation Center. Jeg er uddannet civilingeniør i Medicin og Teknologi fra DTU og sidder til daglig med meget alsidige opgaver – lige fra opsætning af sensorer til Watson IoT Platform og modellering af data til facilitering af daily standups i projektteamet og samtaler med kunden. I min fritid spiller jeg bl.a. håndbold og sejler, når vejret er godt. Jeg er vild med at hver dag er forskellig i IBM Client Innovation Center, og at man møder mange forskellige kunder og virksomheder. Derudover har jeg mine (unge og sjove) kolleger. Nytænkning og innovation er i fokus på mine projekter, og jeg arbejder med nye, spændende teknologier."
                elif winner == 10:
                    Final_result = "Nicolaj"
                    Img_Result = "Nikolaj.png"
                    disc_result = "Du minder om mig! Jeg hedder Nicolaj og er Automation-udvikler i IBM Client Innovation Center. Jeg har en bachelor i IT Produktudvikling og sidder til daglig og udvikler automatiseringsløsninger for at frigøre vigtige kunderessourcer. I min fritid bruger jeg meget tid på at game og være sammen med mine venner. For mig er det bedste ved mit arbejde, at jeg får mulighed for at udfordre mig selv og benytte nye kunderelevanteteknologier."
                elif winner == 12:
                    Final_result = "Yasmin"
                    Img_Result = "Yasmin.png"
                    disc_result = "Du minder om mig! Jeg hedder Yasmin og er Automation Associate i IBM. Jeg er uddannet cand.merc.IT og sidder til daglig i en koordinerende og faciliterende rolle, hvor jeg fungerer som bindeleddet mellem IT og forretningen – lidt ala en mini projektleder. Jeg arbejder bl.a. med procesafdækning og indhenter viden for forskellige kilder, som analyseres og danner baggrund for beslutninger og igangsættelse af initiativer. I min fritid bruger jeg tid med mine venner og familie – og måske lidt for meget tid på Instagram. En af de ting jeg sætter mest pris på i IBM er feedbackkulturen. Der er stort fokus på personlig såvel som faglig udvikling. Det er MEGA fedt at man har mulighed for det, for det er ikke alle virksomheder der her så stort fokus på det. Desuden er der gode muligheder for at komme på kursus i både Danmark og udlandet - mulighederne er uendelige, og du kan tilegne dig alt den viden du måtte ønske. Du har kollegaer der er superdygtige og er villige til at dele ud af deres kompetencer."
                elif winner == 13:
                    Final_result = "Philip"
                    Img_Result = "Philip.png"
                    disc_result = "Du minder om mig! Jeg hedder Philip og er Cognitive Process Transformation konsulent i IBM, hvor jeg startede i vores Associate-program i 2015. Jeg har en baggrund i Human Ressource Management fra CBS og arbejder til daglig med projektledelse i tæt samarbejde med kunden for at levere IT-løsninger, som understøtter deres business transformation – vi sidder i et stort internationalt team af funktionelle og tekniskeeksperter. I min fritid kan jeg godt lide at sejle, stå på ski og dyrke triatlon. Alt sammen på hobbyplan med henblik på socialt samvær og kunne holde energiniveauet oppe i en travl hverdag"
                elif winner == 14:
                    Final_result = "Peter"
                    Img_Result = "Peter.png"
                    disc_result = "Du minder om mig! Jeg hedder Peter og er IT Business konsulent i IBM. Jeg er uddannet cand.merc.IT i Information Management fra Aarhus Universitet BSS og sidder til dagligt på en automation-projekt som business analyst. Her afdækker jeg forretningens kritiske processer med stakeholders og koordinerer med automatiseringsteamet. I min fritid går jeg meget op i god kaffe, lækker mad og film – gerne Oscar-film og Hitchcock. Det, jeg værdsætter mest ved mit arbejde, er friheden til at nå mine mål, variationen af opgaver og muligheden for at skabe sit eget arbejde med nye projekter og roller."



                else:
                    Final_result = "Wow! du har jo alverdens kompetencer - du har matchet med flere af vores profiler!"



        return render_template("Result.html",result = Final_result, img_Result=Img_Result, Disc_result = disc_result) 

    return render_template('Quizpage.html')




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8001)
