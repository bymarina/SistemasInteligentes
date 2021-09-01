import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as control

#Variáveis Entrada
temperature = control.Antecedent(np.arange(0, 11, 0.5), 'Temperatura')
lotation = control.Antecedent(np.arange(0, 11, 1), 'Lotação')

#Variáveis Saída
power = control.Consequent(np.arange(0, 5, 1), 'Potência')

temperature['Frio'] = fuzzy.trapmf(temperature.universe, [0,0,2,5])
temperature['Apropriado'] = fuzzy.trimf(temperature.universe, [4,5,6])
temperature['Quente'] = fuzzy.trapmf(temperature.universe, [5,8,10.5,10.5])

power['Baixa'] = fuzzy.trapmf(power.universe, [0,0,1,2])
power['Média'] = fuzzy.trimf(power.universe, [1,2,3])
power['Alta'] = fuzzy.trapmf(power.universe, [2,3,4,4])

lotation.automf(names=['Baixa', 'Média', 'Alta'])

temperature.view()
lotation.view()
power.view()

#Regras
rule1 = control.Rule(temperature['Frio'] & lotation['Baixa'], power['Baixa'])
rule2 = control.Rule(temperature['Frio'] & lotation['Média'], power['Baixa'])
rule3 = control.Rule(temperature['Frio'] & lotation['Alta'], power['Média'])

rule4 = control.Rule(temperature['Apropriado'] & lotation['Baixa'], power['Baixa'])
rule5 = control.Rule(temperature['Apropriado'] & lotation['Média'], power['Baixa'])
rule6 = control.Rule(temperature['Apropriado'] & lotation['Alta'], power['Média'])

rule7 = control.Rule(temperature['Quente'] & lotation['Baixa'], power['Média'])
rule8 = control.Rule(temperature['Quente'] & lotation['Média'], power['Alta'])
rule9 = control.Rule(temperature['Quente'] & lotation['Alta'], power['Alta'])

power_control = control.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
power_simulator = control.ControlSystemSimulation (power_control)

#Testando valores
power_simulator.input['Temperatura'] = 6 
power_simulator.input['Lotação'] = 8

power_simulator.compute()
print(power_simulator.output['Potência'])

temperature.view(sim=power_simulator)
lotation.view(sim=power_simulator)
power.view(sim=power_simulator)