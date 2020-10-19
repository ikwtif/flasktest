from pprint import pprint
import logging

def koordEffectBeperking(delen, beperking, koordeffect):
    koordeffect_beperkt = []
    for johansen in delen:
        laagste = min(johansen * beperking, koordeffect)
        koordeffect_beperkt.append(laagste)
    return koordeffect_beperkt


def koordEffectBeperkt(verbinding_middel):
    beperking_koordeffect = {'nagel': {'rond': 0.15,
                                        'vierkant': 0.25,
                                        'geprofileerd': 0.25,
                                        'andere': 0.50},
                             'schroef': 1,
                             'bout':0.25,
                             'stift':0}

    if verbinding_middel.materiaal == 'nagel':
        kop = verbinding_middel.kop_type
        beperking = beperking_koordeffect[verbinding_middel.materiaal][kop]
    else:
        beperking = beperking_koordeffect[verbinding_middel.materiaal]

    return beperking


def bepalingDiktes(snede_enkel, verbinding_middel, member_kop, member_punt, member_midden=None):
    if verbinding_middel == 'nagel' or verbinding_middel == 'nieten':
        if snede_enkel:
            dikte_1 = member_kop.hechtlengte
            dikte_2 = member_punt.hechtlengte
        else:
            dikte_1 = min(member_kop.hechtlengte, member_punt.hechtlengte)
            dikte_2 = member_midden.hechtlengte
    elif verbinding_middel == 'bouten':
        dikte_1 = member_kop.hechtlengte
        dikte_2 = member_punt.hechtlengte
    else:
        dikte_1 = None
        dikte_2 = None

    return dikte_1, dikte_2


def afschuivingHoH(snede, verbinding_middel, stuiksterkte_1k, stuiksterkte_2k, uittreksterkte,
                   member_kop, member_punt, member_midden=None):
    """
    NBN EN 1995-1-1:2005+AC:2006
    8.2 Sterkte van op afschuiving belaste stiftvormige metalen verbinding_middelen
    8.2.2 Hout-op-hout en plaat-op-houtverbindingen
    ------------------------------------------------------
    PER SNEDE EN PER VERBINDINGSMIDDEL
    ------------------------------------------------------
    """
    logging.info('berekening afschuiving hout op hout')
    # Setup variabelen
    dikte_1, dikte_2 = bepalingDiktes(snede_enkel=snede,
                                      verbinding_middel=verbinding_middel,
                                      member_kop= member_kop,
                                      member_punt= member_punt,
                                      member_midden=member_midden)
    materiaal = verbinding_middel.materiaal
    diameter = verbinding_middel.diameter
    koordeffect = uittreksterkte / 4
    vloeimoment = verbinding_middel.vloeimoment()
    Beta = stuiksterkte_2k / stuiksterkte_1k

    # Bepalen beperking koordeffect
    beperking = koordEffectBeperkt(verbinding_middel)


    if snede == True: #enkelsnedig
        johansen_a = stuiksterkte_1k * dikte_1 * diameter

        johansen_b = stuiksterkte_2k * dikte_2 * diameter

        johansen_c = ((stuiksterkte_1k * dikte_1 * diameter) / (1 + Beta)) * \
                     ((Beta + (2 * Beta**2 * (1+(dikte_2/dikte_1)+(dikte_2/dikte_1)**2)) + Beta**3 * (dikte_2/dikte_1)**2)**(1/2) -
                      Beta * (1 + (dikte_2/dikte_1)))

        johansen_d = 1.05 * ((stuiksterkte_1k * dikte_1 * diameter)/(2 + Beta)) * \
                     (((2 * Beta * (1 + Beta))+((4 * Beta * (2 + Beta) * vloeimoment)/(stuiksterkte_1k*diameter*dikte_1**2)))**(1/2) - Beta)

        johansen_e = 1.05 * ((stuiksterkte_1k * dikte_2 * diameter)/(1 + (2 * Beta))) * \
                     (((2 * (Beta**2) * (1 + Beta))+((4 * Beta * (1 + (2*Beta)) * vloeimoment)/(stuiksterkte_1k*diameter*dikte_2**2)))**(1/2) - Beta)

        johansen_f = 1.15 * ((2 * Beta ) / (1 + Beta)) * (2 * vloeimoment * stuiksterkte_1k * diameter)**(1/2)

        delen = [johansen_c, johansen_d, johansen_e, johansen_f]
        koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)

        sterkte = [johansen_a, johansen_b]
        for i, johansen in enumerate(delen):
            sterkte.append(johansen + koordeffect_beperkt[i])

        Fvrx = sterkte[sterkte.index(min(sterkte))]

    if snede == False: #dubbelsnedig


        johansen_g = stuiksterkte_1k * dikte_1 * diameter

        johansen_h = 0.5 * stuiksterkte_2k * dikte_2 * diameter

        johansen_i = 1.05 * ((stuiksterkte_1k * dikte_1 * diameter)/(2 + Beta)) * \
                     ((((2 * Beta) * (1 + Beta)) + ((4 * Beta * (2 + Beta) * vloeimoment) / (stuiksterkte_1k * dikte_1**2)))**(1/2) - Beta)

        johansen_k = 1.15 * ((2 * Beta)/(1 + Beta))**(1/2) * (2 * vloeimoment * stuiksterkte_1k * diameter)**(1/2)

        delen = [johansen_i, johansen_k]
        koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)

        sterkte = [johansen_g, johansen_h]
        for i, johansen in enumerate(delen):
            sterkte.append(johansen + koordeffect_beperkt[i])

        Fvrx = sterkte[sterkte.index(min(sterkte))]

    saveLocals(locals(), 'AfschuivingHoH')
    return Fvrx


def afschuivingSoH(snede, member_kop, member_punt, verbinding_middel, stuiksterkte, uittreksterkte):
    """
        NBN EN 1995-1-1:2005+AC:2006
        8.2 Sterkte van op afschuiving belaste stiftvormige metalen verbinding_middelen
        8.2.3 staal-op-houtverbindingen
    """
    logging.info('berekening afschuiving staal op hout')
    # stuiksterkte moet van houten element komen
    materiaal = verbinding_middel.materiaal
    koordeffect = uittreksterkte / 4
    diameter = verbinding_middel.diameter
    vloeimoment = verbinding_middel.vloeimoment()
    beperking = koordEffectBeperkt(verbinding_middel)

    if member_kop.soort == 'staal':
        staalplaat_dikte = member_kop.dikte
        hout_dikte = member_punt.dikte
    elif member_punt.soort == 'staal':
        staalplaat_dikte = member_punt.dikte
        hout_dikte = member_kop.dikte

    if staalplaat_dikte <= 0.5 * diameter:
        staalplaat = 'dun'
    elif staalplaat_dikte >= diameter:#en p71
        staalplaat = 'dik'
    else:  # interpoleren
        #IMPLEMENT BOTH
        #staalplaat = 'both'
        print('implement code for interpolation')

    if snede == True and member_kop.soort == 'staal':
        if staalplaat == 'dun':
            #stuiksterkte moet van houten element komen
            johansen_a = 0.4 * stuiksterkte * hout_dikte * diameter
            johansen_b = 1.15 * (2 * vloeimoment * stuiksterkte * diameter)**(0.5)
            delen = [johansen_b]
            koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)
            sterkte = [johansen_a]
            for i, johansen in enumerate(delen):
                sterkte.append(johansen + koordeffect_beperkt[i])
            Fvrx = sterkte[sterkte.index(min(sterkte))]

        if staalplaat == 'dik':
            johansen_c = stuiksterkte * hout_dikte * diameter * \
                         ((2 + (4 * vloeimoment)/(stuiksterkte * diameter * hout_dikte**2))**0.5-1)
            johansen_d = 2.3 * (vloeimoment * stuiksterkte * diameter)**0.5
            johansen_e = stuiksterkte * hout_dikte * diameter
            delen = [johansen_c, johansen_d]
            koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)
            sterkte = [johansen_e]
            for i, johansen in enumerate(delen):
                sterkte.append(johansen + koordeffect_beperkt[i])
            Fvrx = sterkte[sterkte.index(min(sterkte))]
    elif snede == False:
        if member_punt.soort == 'staal':
            johansen_f = stuiksterkte * hout_dikte * diameter
            johansen_g = stuiksterkte * hout_dikte * diameter * \
                         (((2 + (4 * vloeimoment)/(stuiksterkte * diameter * hout_dikte**2))**0.5)-1)
            johansen_h = 2.3 * (vloeimoment * stuiksterkte * diameter)**0.5
            delen = [johansen_g, johansen_h]
            koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)
            sterkte = [johansen_f]
            for i, johansen in enumerate(delen):
                sterkte.append(johansen + koordeffect_beperkt[i])

            Fvrx = sterkte[sterkte.index(min(sterkte))]

        if staalplaat == 'dun' and member_kop.soort == 'staal':
            jh_1 = 0.5 * stuiksterkte * hout_dikte * diameter
            print('stuiksterkte:', stuiksterkte, 'houtdikte:', hout_dikte, 'diameter', diameter)
            jh_2 = 1.15 * (2 * vloeimoment * stuiksterkte * diameter)**0.5
            delen = [jh_2]
            koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)
            sterkte = [jh_1]
            for i, johansen in enumerate(delen):
                sterkte.append(johansen + koordeffect_beperkt[i])
            Fvrx = sterkte[sterkte.index(min(sterkte))]


        if staalplaat == 'dik' and member_kop.soort == 'staal':
            jh_3 = 0.5 * stuiksterkte * hout_dikte * diameter
            jh_4 = 2.3 * (vloeimoment * stuiksterkte * diameter)**0.5
            delen = [jh_4]
            koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)
            sterkte = [jh_3]
            for i, johansen in enumerate(delen):
                sterkte.append(johansen + koordeffect_beperkt[i])

            Fvrx = sterkte[sterkte.index(min(sterkte))]

    saveLocals(locals(), 'AfschuivingSoH')
    #pprint(locals())
    return Fvrx


def saveLocals(output, text):
    with open('{}.txt'.format(text), 'wt') as out:
        pprint(output, stream=out)
