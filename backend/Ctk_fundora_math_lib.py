# Math Library 
def percentage_of_offering(origional_price, new_price ):
    Value_for_a = round((new_price/origional_price) * 100, 0)

def udregn_Indkomst(data_var):

    samletTal = data_var['indtaegt_1'].get() + data_var['indtaegt_2'].get()
    #print(f"Samlet indtægt: {samletTal}")

    salary1 = data_var['indtaegt_1'].get()
    pension1 = float(data_var['pension_1'].get()) / 100 if data_var['pension_1'].get() else 0

    salary2 = data_var['indtaegt_2'].get()
    pension2 = float(data_var['pension_2'].get()) / 100 if data_var['pension_2'].get() else 0

    savings = float(data_var['opsparring_1'].get()) + float(data_var['opsparring_2'].get()) 

    ExistLoan1 = float(data_var['gaeld_1'].get()) if data_var['gaeld_1'].get() else 0
    ExistLoan2 = float(data_var['gaeld_2'].get()) if data_var['gaeld_2'].get() else 0

    # Calculate after-tax salaries
    after_tax_salary1, samletSkat1 = beregn_netto_maanedsloen(salary1) 
    after_tax_salary2, samletSkat2 = beregn_netto_maanedsloen(salary2) 

    # Calculate total household income
    total_income = (salary1) + (salary2) # Vi bruger ikke længer pension til gældsfaktor
    max_laan = (total_income * 12 * 4 + savings) - (ExistLoan1 + ExistLoan2)
    loan_total = total_income * 12 * 4
    total_after_tax_income = after_tax_salary1 + after_tax_salary2

    # Format number with correct thousand separators
    data_var["samlet_indtaegt"].set(total_income)
    data_var["max_laan"].set(max_laan)
    data_var["lon_efter_skat1"].set(after_tax_salary1)
    data_var["lon_efter_skat2"].set(after_tax_salary2)
    data_var["samlet_efter_skat"].set(total_after_tax_income)


def beregn_netto_maanedsloen( maanedsloen_brutto, kommuneskat_sats=0.2497, personfradrag_maaned=7536, atp_maaned=99):

    # Skattesatser og grænser (2025)
    am_bidrag_sats = 0.08
    bundskat_sats = 0.1201
    topskat_sats = 0.15 
    topskat_graense_efter_am_aar = 611800

    # Omregn til årsløn
    aarsindkomst = maanedsloen_brutto * 12

    # AM-bidrag
    am_bidrag = aarsindkomst * am_bidrag_sats
    indkomst_efter_am = aarsindkomst - am_bidrag

    # Personfradrag
    personfradrag_aar = personfradrag_maaned * 12
    skattepligtig_indkomst = max(0, indkomst_efter_am - personfradrag_aar)

    # Skatter
    bundskat = skattepligtig_indkomst * bundskat_sats
    kommuneskat = skattepligtig_indkomst * kommuneskat_sats

    # Topskat
    if indkomst_efter_am > topskat_graense_efter_am_aar:
        topskat = (indkomst_efter_am - topskat_graense_efter_am_aar) * topskat_sats
    else:
        topskat = 0

    # Samlet skat (uden AM og ATP)
    samlet_skat = bundskat + kommuneskat + topskat

    # Inkludér AM-bidrag og ATP
    total_skat_med_am_atp = samlet_skat + am_bidrag + (atp_maaned * 12)

    # Netto årsløn og månedsløn
    netto_aarsindkomst = aarsindkomst - total_skat_med_am_atp
    maaneds_netto = netto_aarsindkomst / 12

    # Den faktiske skatteprocent er forskellig efter hvor meget man tjener. 
    # Tjener man meget er procenten 15% af det overskyddende, er man maget over så vil skatten man betaler også være tilsvarende højere. 
    faktisk_skatteprocent = (total_skat_med_am_atp / aarsindkomst) * 100 

    return round(maaneds_netto, 0), round(faktisk_skatteprocent, 0)


def udregn_Bolig_Udgift_output(finansiering_vars, udgift_var):  

    gældsfaktor = ((udgift_var['forventet_pris'].get() + finansiering_vars['gaeld_1'].get() + finansiering_vars['gaeld_2'].get())
                   - (finansiering_vars['opsparring_1'].get() + finansiering_vars['opsparring_2'].get())) / (finansiering_vars['samlet_indtaegt'].get()*12)
    
    opsparing = finansiering_vars['opsparring_1'].get() + finansiering_vars['opsparring_2'].get()
    huspris = udgift_var['forventet_pris'].get()

    if 0.2*huspris > opsparing: # BANKLÅN: hvis 20% af boligens totalpris er større end opsparringen skal de bruge banklån
        SavingPercentage = opsparing / huspris
        restbeløbBankloan = SavingPercentage + 0.8 # 0.8 = 80% representing the realkredit part of the loan. 
        TotalRealLån = huspris *.8
        TotalBanklån = huspris - (restbeløbBankloan * huspris)

    elif 0.2*huspris <= opsparing: # Kun behov for real lån. 
        TotalRealLån = huspris - opsparing;
        TotalBanklån = 0; 

    samlede_udgifter = (   udgift_var["bolig_udgift"].get() + udgift_var["forbrug"].get()  + udgift_var["mad_dagligvare"].get()
                         + udgift_var["transport"].get() + udgift_var["forsikringer"].get() + udgift_var["telefon_int_medie"].get()
                         + udgift_var["personlig_pleje_toej"].get() + udgift_var["fritid_fornoejelser"].get() + udgift_var["pasning_fritidsaktiv"].get()
                         + udgift_var["flex_udgift_var1"].get() + udgift_var["flex_udgift_var2"].get() + udgift_var["flex_udgift_var3"].get())

    # Set output values 
    udgift_var["gaeldsfaktor"].set(round(gældsfaktor, 2)) 
    udgift_var["alle_faste_udgifter"].set(round(samlede_udgifter, 2)) 

    udgift_var["banklaan"].set(round(TotalBanklån, 2)) 
    udgift_var["realkreditlaan"].set(round(TotalRealLån, 2)) 
    udgift_var["samlet_laan"].set(round(TotalRealLån+TotalBanklån, 2)) 


# Fremtidig Økonomi
def udregn_fremtidig_økonomi(finansiering_vars, udgift_vars, fremtid_vars, eksport_vars, mainApp):
    huspris     = udgift_vars['forventet_pris'].get()

    # Realkredit information 
    real_rente      = float (fremtid_vars['realkredit_nominel'].get())        if float(fremtid_vars['realkredit_nominel'].get()) else 0 
    real_periode    = int   (fremtid_vars['realkredit_laaneperiode'].get())    if int  (fremtid_vars['realkredit_laaneperiode'].get()) else 0 
    real_terminer   = int   (fremtid_vars['realkredit_terminer'].get())       if int  (fremtid_vars['realkredit_terminer'].get()) else 0 
    real_bidragssats= float (fremtid_vars['realkredit_bidragssats'].get())    if float(fremtid_vars['realkredit_bidragssats'].get()) else 0 

    # Bank information 
    bank_rente      = float (fremtid_vars['bank_nominel'].get())              if float(fremtid_vars['bank_nominel'].get()) else 0 
    bank_periode    = int   (fremtid_vars['bank_laaneperiode'].get())          if int  (fremtid_vars['bank_laaneperiode'].get()) else 0 
    bank_terminer   = int   (fremtid_vars['bank_terminer'].get())             if int  (fremtid_vars['bank_terminer'].get()) else 0 
    
    opsparing = finansiering_vars['opsparring_1'].get() + finansiering_vars['opsparring_2'].get()

    # BANKLÅN & Realkredit
    if 0.2*huspris > opsparing: 
        
        SavingPercentage = opsparing / huspris
        RemainingPercentageForBankloan = SavingPercentage + 0.8 
        real_loan = huspris *.8 
        bank_loan = huspris - (RemainingPercentageForBankloan * huspris)
        
        # Calculate scenarios
        realkredit_lån_resultat = calculate_loan_scenario(real_loan, real_rente, real_periode, payments_per_year=real_terminer, bidragssats=real_bidragssats)      
        bank_lån_resultat = calculate_loan_scenario(bank_loan, bank_rente, bank_periode, payments_per_year=bank_terminer, bidragssats=0) 
        
        mainApp.fremtid_dicts['realkredit_laaneberegning'] = realkredit_lån_resultat
        mainApp.fremtid_dicts['bank_laaneberegning'] = realkredit_lån_resultat
        #fremtid_vars['realkredit_laaneberegning'] = realkredit_lån_resultat
        # fremtid_vars['bank_laaneberegning']       = bank_lån_resultat

        real_first_payment = realkredit_lån_resultat["Amortization Schedule"][0]
        bank_first_payment = bank_lån_resultat["Amortization Schedule"][0]

        RealTotalCost               = realkredit_lån_resultat['Total Cost']
        RealTotalInterest           = realkredit_lån_resultat["Total Interest"]
        RealMonthlyCost             = realkredit_lån_resultat["Månedelig Cost"]
        RealMonthlyInterest         = realkredit_lån_resultat["Månedelig Interest"]
        RealMonthlyRentefradrag     = realkredit_lån_resultat["Månedelig Rentefradrag"]
        RealMonthlyAfdrag           = realkredit_lån_resultat["Månedelig Afdrag"]

        # udregn fradrag og fradrags procent 
        interest_grand_total = float(f"{realkredit_lån_resultat["Total Interest"]}") + float(f"{bank_lån_resultat["Total Interest"]}")
        Total_rentefradrag, udregnet_fradragsprocent = beregn_rentefradrag_enkelt_person(interest_grand_total)

        BanktotalCost               = bank_lån_resultat["Total Cost"] 
        BanlTotalInterest           = bank_lån_resultat["Total Interest"]
        BankMonthlyCost             = bank_lån_resultat["Månedelig Cost"]
        BankMonthlyInterest         = bank_lån_resultat["Månedelig Interest"]
        BankMonthlyRentefradrag     = bank_lån_resultat["Månedelig Rentefradrag"]
        BankMonthlyAfdrag           = bank_lån_resultat["Månedelig Afdrag"]

        LoanTotalCostCombined       = realkredit_lån_resultat["Total Cost"] + bank_lån_resultat["Total Cost"]
        LoanTotalInterestCombined   = realkredit_lån_resultat["Total Interest"] + bank_lån_resultat["Total Interest"]
 
        LoanMonthlyCombined         = RealMonthlyCost + BankMonthlyCost
        loanMonthlyInterest         = RealMonthlyInterest + BankMonthlyInterest
        LoanMonthlyRentefradrag     = RealMonthlyRentefradrag + BankMonthlyRentefradrag
        LoanMonthlyAfdrag           = RealMonthlyAfdrag + BankMonthlyAfdrag         

    # REALKREDIT ONLY
    elif 0.2*huspris <= opsparing:
        SavingPercentage        = opsparing / huspris
        real_loan               = huspris - opsparing   
        realkredit_lån_resultat       = calculate_loan_scenario(real_loan, real_rente, real_periode, payments_per_year=4, bidragssats=real_bidragssats) #  fradragsprocent=fradragsprocent)
        
        mainApp.fremtid_dicts['realkredit_laaneberegning'] = realkredit_lån_resultat
        #fremtid_vars['realkredit_laaneberegning'] = realkredit_lån_resultat # flyttet ud af vars for bedre db struktur

        interest_grand_total    = float(f"{realkredit_lån_resultat["Total Interest"]}") 
        Total_rentefradrag, udregnet_fradragsprocent = beregn_rentefradrag_enkelt_person(interest_grand_total)

        real_first_payment      = realkredit_lån_resultat["Amortization Schedule"][0]
        RealTotalCost           = realkredit_lån_resultat['Total Cost']
        RealTotalInterest       = realkredit_lån_resultat["Total Interest"]
        RealMonthlyCost         = realkredit_lån_resultat["Månedelig Cost"]
        RealMonthlyInterest     = realkredit_lån_resultat["Månedelig Interest"]
        RealMonthlyRentefradrag = realkredit_lån_resultat["Månedelig Rentefradrag"]
        RealMonthlyAfdrag       = realkredit_lån_resultat["Månedelig Afdrag"]

        LoanMonthlyCombined     = RealMonthlyCost 
        loanMonthlyInterest     = RealMonthlyInterest 
        LoanMonthlyRentefradrag = RealMonthlyRentefradrag 
        LoanMonthlyAfdrag       = RealMonthlyAfdrag # makes no sense because its the total ove rall years. 
    
    #rentefradragProcent = float(udregnet_fradragsprocent)
    rentefradragProcent = udregnet_fradragsprocent

    Output_financial_Monthly_future( finansiering_vars, udgift_vars, fremtid_vars, eksport_vars, 
                                    loanMonthlyInterest, LoanMonthlyAfdrag, LoanMonthlyRentefradrag, rentefradragProcent,)


# Låne scenarie (burde være en class )
def calculate_loan_scenario(loan_amount, annual_interest_rate, loan_term_years, payments_per_year, bidragssats):
    """
    Calculates all relevant loan details for a single scenario.
    """
    schedule = generate_amortization_schedule(loan_amount, annual_interest_rate, loan_term_years, payments_per_year, bidragssats)
    total_cost, total_interest, total_afdrag = calculate_total_cost(schedule)
    monthly_cost, monthly_interest, monthly_rentefradrag, monthly_afdrag = calculate_monthly_cost(schedule, payments_per_year)

    return {
        "Total Cost":               total_cost,
        "Total Interest":           total_interest,
        "Rentefradrag":             total_afdrag,
        "Månedelig Cost" :          monthly_cost, 
        "Månedelig Interest" :      monthly_interest, 
        "Månedelig Rentefradrag" :  monthly_rentefradrag, 
        "Månedelig Afdrag" :        monthly_afdrag, 
        "Amortization Schedule":    schedule
    }

def beregn_rentefradrag_enkelt_person(rente_dkk):
    # beregn rentefradraget basseret paa to satser 
    # sæt satser 
    sats_op_til_50000 = 0.331
    sats_over_50000 = 0.251
    rentefradrag = 0 
    fradragsprocent = sats_op_til_50000

    # hvis der ikke betales renter
    if rente_dkk == 0: 
        return round(rentefradrag, 2), round(fradragsprocent, 2)

    # hvis renten er under 50k bruges min. sats. 
    if rente_dkk < 50000: 
        rentefradrag = rente_dkk * sats_op_til_50000

    # Renten er over 50k bruges min. op til 50k og eftg. max sats. 
    else: 
        rentefradrag_min = 50000 * sats_op_til_50000
        beloeb_til_max = rente_dkk - 50000
        rentefradrag_max = beloeb_til_max * sats_over_50000
        rentefradrag = rentefradrag_min + rentefradrag_max
        fradragsprocent = rentefradrag / rente_dkk

    return round(rentefradrag, 2), round(fradragsprocent, 2)

def generate_amortization_schedule(loan_amount, annual_interest_rate, loan_term_years, payments_per_year=12, bidragssats=0):
    """
    Generates an amortization schedule for a loan, considering bidragssats for Realkredit loans.
    """
    remaining_balance = loan_amount
    aaop = annual_interest_rate + bidragssats
    payment = calculate_annuity_payment(loan_amount, aaop, loan_term_years, payments_per_year)
    interest_payment = remaining_balance * (aaop / 100) / payments_per_year # rente
    principal_payment = payment - interest_payment # afdrag

    # print ("Underlig sammensætning her? : %s " %  annual_interest_rate, bidragssats)

    schedule = []
    
    for period in range(1, loan_term_years * payments_per_year + 1):
        interest_payment = remaining_balance * ((annual_interest_rate + bidragssats) / 100) / payments_per_year
        principal_payment = payment - interest_payment
        remaining_balance -= principal_payment
        
        schedule.append({
            "Periode": period,
            "Ydelse": round(payment, 2),
            "Rente": round(interest_payment, 2),
            "Afdrag": round(principal_payment, 2),
            "Restgæld": round(remaining_balance, 2)
        })
    
    return schedule

def calculate_monthly_cost(schedule, payments_per_year): 
    # monthly calculations 
    Monthly_paid = schedule[0]["Ydelse"] / (12/payments_per_year)
    Monthly_interest = schedule[0]["Rente"] / (12/payments_per_year) 
    Monthly_afdrag = schedule[0]["Afdrag"] / (12/payments_per_year) 

    # temp fradrag
    Monthly_fradrag = Monthly_interest * (33.1 / 100) # ''' BUG her skal fikses, det skal laves paa det samlede rente beloeb '''

    return Monthly_paid, Monthly_interest, Monthly_fradrag, Monthly_afdrag, 

def calculate_annuity_payment(loan_amount, annual_interest_rate, loan_term_years, payments_per_year=12):
    """
    Calculates the annuity payment for a given loan, considering bidragssats for Realkredit loans.
    """

    period_interest_rate = (annual_interest_rate / 100) / payments_per_year
    total_payments = loan_term_years * payments_per_year

    if period_interest_rate == 0:
        return loan_amount / total_payments

    annuity_payment = (loan_amount * period_interest_rate) / (1 - (1 + period_interest_rate) ** -total_payments)

    return annuity_payment

def calculate_total_cost(schedule):
    """
    Calculates the total cost of a loan from an amortization schedule.
    """
    total_paid = sum(payment['Ydelse'] for payment in schedule)
    total_interest = sum(payment['Rente'] for payment in schedule)
    total_afdrag = sum(payment['Afdrag'] for payment in schedule)
    return total_paid, total_interest, total_afdrag

def Output_financial_Monthly_future(finansiering_vars, udgift_vars, fremtid_vars, eksport_vars, 
                                    RenteUdgifterPrMd=0, TotalAfdragPrMd=0, TotalRentefradragPrMd=0, RentefradraProcent=33.1):

    total_expenses = (udgift_vars['alle_faste_udgifter'].get() + RenteUdgifterPrMd + TotalAfdragPrMd) #+ TotalRentefradragPrMd
    rådighedsbeløb = (round(finansiering_vars['lon_efter_skat1'].get(), 0)+round(finansiering_vars['lon_efter_skat2'].get(),0) +TotalRentefradragPrMd)-total_expenses
    samletYdelse = (RenteUdgifterPrMd+TotalAfdragPrMd)
    
    fremtid_vars['rente_betaling'].set(round(RenteUdgifterPrMd,0))
    fremtid_vars['rente_afdrag'].set(round(TotalAfdragPrMd,0))
    fremtid_vars['rentefradrag'].set(round(TotalRentefradragPrMd,0))
    fremtid_vars['rentefradrag_procent'].set(RentefradraProcent*100)

    fremtid_vars['samlet_ydelse'].set(round(samletYdelse,0))
    fremtid_vars['fast_udgifter'].set(round(udgift_vars['alle_faste_udgifter'].get(),0))
    fremtid_vars['fast_udgifter_inkl_ydelser'].set(round(total_expenses,0))

    fremtid_vars['raadighedsbeloeb'].set(round(rådighedsbeløb,0))


# Udregn Ackerman forhandling 
class Ackerman_Set_Values():
    def __init__(self, forhandlings_vars):
        # check the int. 
        self.ForventetPris = 0
        try:
            self.ForventetPris = float(forhandlings_vars['forventet_pris'].get())
        except:
            return

        self.forhandlings_vars = forhandlings_vars
        self.agressivitet = forhandlings_vars['aggressivitet'].get()

        # Define negotiation strategies
        self.aggressiveness_strategies = {
            1: [90, 95, 98, 100],   # Conservative
            2: [80, 88, 94, 100],   # Moderate
            3: [65, 85, 95, 100]    # Aggressive (Ackerman)
        }

        # Fallback if invalid aggressiveness level is passed
        self.procent = self.aggressiveness_strategies.get(self.agressivitet, self.aggressiveness_strategies[2])

        self.set_outputvalues()

    def set_outputvalues(self):
        for i in range(4):
            key_procent = f"runde{i+1}_procent"
            key_pris = f"runde{i+1}_pris"

            procent_value = self.procent[i]
            pris_value = round(self.ForventetPris * (procent_value / 100))

            self.forhandlings_vars[key_procent].set(procent_value)
            self.forhandlings_vars[key_pris].set(pris_value)


def beregn_total_budget_pris(data_dict):
    total = 0

    for renovation in data_dict.values():
        if not renovation.get("inkluder_i_budget", True):
            continue  # Skip entire renovation

        opgavegruppe = renovation.get("opgaver", {})
        for opgavenavn, opgavedata in opgavegruppe.items():
            ekskludere = opgavedata.get("ekskludere", False)
            pris_str = opgavedata.get("Pris", "0").strip()

            if not ekskludere:
                try:
                    pris = float(pris_str.replace(".", "").replace(",", "."))
                    total += pris
                except ValueError:
                    print(f"Advarsel: Kunne ikke tolke pris '{pris_str}' i opgave '{opgavenavn}'")

    return round(total)





'''

    # expressions 

    x ^ 3 = xxx 

    x ^ -1 = 1 / x 
    x ^ -n = 1 / x ^ n

    (x^m)^n = x ^ m * n 

    (x^3)^2 = x^3 * x

    (xy)^m = x^m y^m 


    #1.  8, 9
    #2. 4^5 * 2^5 = 4^5
    #3. 5^5*5*5 = 5^7            (5^6)*5 = 78125
    #4. 
    #5 a^b * a^b = (a^2)^b 
    ## A^2*b 
    #6 Same 

    # 8 = 2^3 

'''