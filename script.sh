#!/bin/bash

# Lista de instâncias
tasks=(
"A-n32-k5.vrp"  "A-n39-k5.vrp"  "A-n55-k9.vrp"   "A-n80-k10.vrp"  "B-n44-k7.vrp"  "B-n63-k10.vrp"   "M-n121-k7.vrp"   "P-n40-k5.vrp"   "P-n60-k10.vrp"   "X-n115-k10.vrp"
"A-n33-k5.vrp"  "A-n39-k6.vrp"  "A-n60-k9.vrp"   "B-n31-k5.vrp"   "B-n45-k5.vrp"  "B-n64-k9.vrp"    "M-n151-k12.vrp"  "P-n45-k5.vrp"   "P-n60-k15.vrp"   "X-n120-k6.vrp"
"A-n33-k6.vrp"  "A-n44-k6.vrp"  "A-n62-k8.vrp"   "B-n34-k5.vrp"   "B-n45-k6.vrp"  "B-n66-k9.vrp"    "P-n101-k4.vrp"   "P-n50-k10.vrp"  "P-n65-k10.vrp"   "X-n129-k18.vrp"
"A-n34-k5.vrp"  "A-n45-k7.vrp"  "A-n63-k10.vrp"  "B-n35-k5.vrp"   "B-n50-k7.vrp"  "B-n67-k10.vrp"   "P-n16-k8.vrp"    "P-n50-k7.vrp"   "P-n70-k10.vrp"   "X-n134-k13.vrp"
"A-n36-k5.vrp"  "A-n46-k7.vrp"  "A-n63-k9.vrp"   "B-n38-k6.vrp"   "B-n51-k7.vrp"  "B-n68-k9.vrp"    "P-n19-k2.vrp"    "P-n51-k10.vrp"  "P-n76-k4.vrp"    "X-n139-k10.vrp"
"A-n37-k5.vrp"  "A-n48-k7.vrp"  "A-n64-k9.vrp"   "B-n39-k5.vrp"   "B-n52-k7.vrp"  "B-n78-k10.vrp"   "P-n20-k2.vrp"    "P-n55-k10.vrp"  "P-n76-k5.vrp"    "X-n143-k7.vrp"
"A-n37-k6.vrp"  "A-n53-k7.vrp"  "A-n65-k9.vrp"   "B-n41-k6.vrp"   "B-n56-k7.vrp"  "F-n72-k4.vrp"    "P-n21-k2.vrp"    "P-n55-k7.vrp"   "X-n106-k14.vrp"
"A-n38-k5.vrp"  "A-n54-k7.vrp"  "A-n69-k9.vrp"   "B-n43-k6.vrp"   "B-n57-k9.vrp"  "M-n101-k10.vrp"  "P-n22-k2.vrp"    "P-n55-k8.vrp"   "X-n110-k13.vrp"

)

# Lista de valores de alfa
alphas=(0.125 0.25 0.5 0.75 1)

# Itera sobre as instâncias e os valores de alfa, executando o comando em terminais separados
for task in "${tasks[@]}"; do
  for alpha in "${alphas[@]}"; do
    gnome-terminal -- bash -c "python main.py $task GRASP-1000-$alpha; exec bash"
  done
done
