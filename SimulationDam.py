
def simulation(vars, flow=20000, drainAmount = 3000, capacityEnergy = 160, limitsGate = [15000, 25000, 32000, 40000], flowTurbine = 830, limitAlert = 45000):
    changes = 0
    result = []
    resume = {
        'drained': 0,
        'flow': flow,
        'lostEnergy': 0,
        'gates': [0] * len(limitsGate),
        'alert': 0
    }
    for i, var in enumerate(vars):  #var = valor del dia
        if changes != 0:
            aux = changes * drainAmount  #changes va a ser 1,2,3 o 4 depende de las comgates que se abrieron el dia anterior
            resume['flow'] -= aux
            resume['drained'] += aux
            #367mv = 1tb -> 830ms ------------Una turbina genera 367megavatios con 830ms
            resume['lostEnergy'] += ((
                aux/flowTurbine
            ) * capacityEnergy) * 24 #regla de 3
            #ver algo de perdidas
            changes = 0
        resume['flow'] += var
        day = {
            'day': i+1,
            'flow': resume['flow'],
            'gates': [False] * len(limitsGate)
        }
        for i, limit in enumerate(limitsGate):
            if resume['flow'] >= int(limit):
                resume['gates'][i] += 1
                day['gates'][i] = True
                changes += 1
        if resume['flow'] >= limitAlert:
            resume['alert'] += 1
            day['alert'] = True
        result.append(day)
    return {'simulation': result, 'resume': resume}
