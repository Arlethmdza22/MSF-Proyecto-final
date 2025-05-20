"""
Práctica 3: Sistema cardiovascular

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Perez Chavez Marco Antonio
Número de control: 19212423
Correo institucional: marco.perez193@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control 
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np 
import math as m 
import matplotlib.pyplot as plt 
import control as ctrl

# Parámetros de simulación
x0, t0, tF, dt, w, h = 0, 0, 10, 1E-3, 10, 5
N = round((tF - t0) / dt) + 1
t = np.linspace(t0, tF, N) 
u =  2*np.sin(m.pi/2*t)


# Función del diabetes
def sys_diabetes(CP, CH, RL, RP, L): 
    b0= [CP*RP,1]
    a0= CH*CP*L*RP 
    a1= CH*L + CP*L + CH*CP*RL*RP
    a2= CH*RL + CP*RL + CP*RP
    a3= 1
    num = b0
    den = [a0,a1,a2,a3]
    return ctrl.tf(num, den)

#Funcion de transferencia: Individuo saludable [control]
CP,CH,RL,RP,L= 470E-6, 10E-6, 1E3, 1E3, 10E-3
sysN = sys_diabetes(CP,CH,RL,RP,L)
print('Individuo sano [control]: ')
print(sysN)

#Funcion de transferencia: Individuo enfermo [Caso: Diabetes]
CP,CH,RL,RP,L= 100E-6, 1E-6, 1E3, 1E3, 7E-3
sysE = sys_diabetes(CP,CH,RL,RP,L)
print('Individuo sano [caso]: ')
print(sysE)



# Colores
Morado = [70/255, 53/255, 177/255]
naranja = [1, 128/255, 0]
rojo = [184/255, 0/255, 31/255]
Azul = [7/255, 71/255, 153/255]


def plotsignals(u, sysS, sysE, sysPID, signal):
    fig = plt.figure()
    ts,Vs = ctrl.forced_response(sysS,t,u,x0)
    plt.plot(t,Vs,'-',color = rojo, label = '$Ve(t): Control$')
    ts,Ve = ctrl.forced_response(sysE,t,u,x0)
    plt.plot(t,Ve,'-',color=Morado,label = '$Ve(t): Caso$')
    ts,pid=ctrl.forced_response(sysPID,t,Vs,x0)
    plt.plot(t,pid, ':', linewidth = 3, color = Azul,
             label='$Ve(t): Tratamiento$')
    plt.grid(False)
    plt.xlim(0,10)
    plt.ylim(-2.5,2.5)
    plt.xticks(np.arange(0,11,2))
    plt.yticks(np.arange(-2,2.5,0.5))
    plt.xlabel('$t$ [s]')
    plt.ylabel('$Ve(t)$ [V]')
    plt.legend(bbox_to_anchor = (0.5,-0.3), loc = 'center', ncol=4,
               fontsize=8,frameon=False)
    plt.show()
    fig.set_size_inches(w,h)
    fig.tight_layout()
    namepng='python_'+signal+'.png'
    namepdf='python_'+signal+'.pdf'
    fig.savefig(namepng,dpi=600,bbox_inches='tight')
    fig.savefig(namepdf,dpi=600,bbox_inches='tight')
    
    
def tratamiento (Cr,Re,Rr,Ce,sysE):
    numPID = [Re*Rr*Ce*Cr,Re*Ce+Rr*Cr,1]
    denPID=[Re*Cr,0]
    PID = ctrl.tf(numPID,denPID)
    X = ctrl.series(PID,sysE)
    sysPID = ctrl.feedback (X,1,sign = -1)
    return sysPID
#Sistema de control en lazo cerrado
kP,kI,kD,CP =209.526932, 4712.728165, 1.1380488, 470E-6
Re = 1/(kI*CP)
Rr = kP*Re
Ce = kD/Rr
sysPID = tratamiento(Ce,Re,Rr,CP,sysE)
plotsignals(u,sysN,sysE,sysPID,'Diabetes')
