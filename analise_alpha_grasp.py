from matplotlib import pyplot as plt
import numpy as np


def calculate_ci(valores_gaps, nome, benchmarks):

    # benchmarks = [f"Benchmark {i+1}" for i in range(20)]  # Nomes dos benchmarks
    x = np.arange(len(benchmarks))  # Índices dos benchmarks

    # Calcular média e intervalo de confiança global
    media_global = np.mean(valores_gaps)
    desvio_padrao = np.std(valores_gaps, ddof=1)  # Desvio padrão amostral
    n = len(valores_gaps)  # Tamanho da amostra
    z_critico = 1.96  # Para 95% de confiança
    intervalo_conf = z_critico * (desvio_padrao / np.sqrt(n))  # Intervalo de confiança

    # Criar gráfico
    plt.figure(figsize=(12, 6))
    plt.scatter(x, valores_gaps, color='skyblue', alpha=0.8, label='Valores dos Gaps')
    plt.axhline(float(media_global), color='red', linestyle='--', label=f"Média Global = {media_global:.2f}")
    plt.fill_between(
        [-0.5, len(benchmarks)-0.5],
        media_global - intervalo_conf,
        media_global + intervalo_conf,
        color='red', alpha=0.2, label=f"IC 95% [{media_global - intervalo_conf:.2f}, {media_global + intervalo_conf:.2f}]"
    )
    plt.xticks(x, benchmarks, rotation=45, ha='right')  # Benchmarks como rótulos no eixo X
    plt.ylabel('Valor do Gap')
    plt.xlabel('Instâncias')
    plt.title('Intervalo de Confiança - ' + nome)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Mostrar gráfico
    plt.show()

def box_plot(dados):
    # Criando o boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(dados, tick_labels=['GRASP', 'Algoritmo Genético'], patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='red', linewidth=1.5),
                whiskerprops=dict(color='blue'),
                capprops=dict(color='blue'),
                flierprops=dict(marker='o', color='blue', alpha=0.5))

    # Adicionando título e rótulos
    plt.title('Boxplot de Gaps', fontsize=14)
    plt.ylabel('Gap (%)', fontsize=12)
    plt.xlabel('Algoritmo', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrando o gráfico
    plt.tight_layout()
    plt.show()


alpha_125 = [2.806122448979592, 2.723146747352496, 0.40431266846361186, 1.5424164524421593, 3.254067584480601, 8.968609865470851, 4.004214963119073, 2.73972602739726, 3.2846715328467155, 4.16221985058698, 6.719022687609074, 11.798071469086784, 14.408973252804142, 8.928571428571429, 12.561881188118813, 1.636904761904762, 8.189655172413794, 10.623946037099493 ]

alpha_25 = [4.719387755102041, 6.80786686838124, 10.377358490566039, 5.655526992287918, 9.51188986232791, 16.143497757847534, 7.903055848261328, 5.068493150684931, 10.46228710462287, 9.711846318036287, 11.518324607329843, 20.589903573454336, 21.225194132873167, 17.158385093167702, 25.371287128712872, 5.5059523809523805, 21.695402298850574, 25.96964586846543]

alpha_5 = [25.127551020408163, 22.54160363086233, 19.541778975741238, 21.336760925449873, 19.148936170212767, 22.122571001494766, 23.603793466807165, 32.602739726027394, 26.034063260340634, 25.933831376734258, 25.13089005235602, 45.320476460578554, 46.76445211389129, 38.66459627329192, 43.62623762376238, 10.714285714285714, 46.264367816091955, 34.90725126475548]

alpha_75 = [34.183673469387756, 37.518910741301056, 28.03234501347709, 30.334190231362467, 31.1639549436796, 46.93572496263079, 32.982086406743946, 44.109589041095894, 33.941605839416056, 38.31376734258271, 31.93717277486911, 54.963131026659106, 71.26833477135462, 48.91304347826087, 52.289603960396036, 9.077380952380953, 65.22988505747126, 56.82967959527825]

alpha_1 = [45.66326530612245, 44.175491679273826, 44.07008086253369, 34.832904884318765, 38.92365456821027, 44.09566517189836, 38.77766069546891, 54.657534246575345, 35.523114355231144, 49.6264674493063,  36.82373472949389, 59.44412932501418, 88.35202761000863, 59.62732919254658, 51.0519801980198, 15.178571428571427, 75.14367816091954, 57.67284991568297]

dados = [alpha_125, alpha_25, alpha_5, alpha_75, alpha_1]

def box_plot_alphas(dados):
    # Criando o boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(dados, tick_labels=['0.125', '0.25', '0.5', '0.75', '1.0'], patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='red', linewidth=1.5),
                whiskerprops=dict(color='blue'),
                capprops=dict(color='blue'),
                flierprops=dict(marker='o', color='blue', alpha=0.5))

    # Adicionando título e rótulos
    plt.title('Boxplot - Avaliação Parâmetro ALPHA - GRASP', fontsize=14)
    plt.ylabel('Gap (%)', fontsize=12)
    plt.xlabel('Alpha', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrando o gráfico
    plt.tight_layout()
    plt.show()


nomes = [
         'A-n32-k5', 'A-n33-k5', 'A-n37-k6', 'A-n44-k6', 'A-n60-k9', 'A-n62-k8', 'A-n64-k9', 'A-n65-k9', 'A-n69-k9', 'A-n80-k10',
         'B-n38-k6', 'B-n43-k6', 'B-n51-k7', 'B-n56-k7', 'B-n66-k9', 'B-n68-k9', 'B-n78-k10',
         'F-n72-k4',
         'M-n101-k10', 'M-n121-k7',
         'P-n16-k8', 'P-n19-k2', 'P-n20-k2', 'P-n21-k2', 'P-n22-k8', 'P-n40-k5', 'P-n51-k10', 'P-n101-k4',
         'X-n106-k14', 'X-n110-k13'
]


gap_ga = [

2.1683673469387754, 8.018154311649017, 4.636459430979979, 7.043756670224119, 32.20088626292467, 26.319875776397517, 16.773733047822983, 44.122657580919935, 39.43054357204487, 23.482699943278504,

1.2422360248447204, 1.078167115902965, 4.941860465116279, 5.233380480905233, 23.480243161094226, 31.91823899371069, 24.406224406224407,

28.691983122362867,

19.26829268292683, 48.25918762088975,

0.0, 0.0, 0.4629629629629629, 2.843601895734597, 0.0, 12.663755458515283, 18.488529014844804, 37.15124816446402,

12.222137925802292, 33.62500834947566

]

gap_grasp = [ 2.806122448979592
, 2.5718608169440245
, 7.473841554559043
, 2.9882604055496262
, 6.425406203840472
, 9.782608695652174
, 5.924339757316202
, 14.480408858603067
, 11.993097497842967
, 9.812819058423141
, 2.111801242236025
, 3.7735849056603774
, 9.39922480620155
, 10.891089108910892
, 5.623100303951368
, 4.559748427672956
, 7.0434070434070435
, 5.063291139240507
, 12.195121951219512
, 6.479690522243714
, 0.0
, 2.8301886792452833
, 0.0
, 0.0
, 0.0
, 6.331877729257641
, 19.4331983805668
, 11.45374449339207
, 8.102571883772097
, 18.308730211742702]

dados_finais = [gap_grasp, gap_ga]

# -------------------------------------------------------------------------------------------------------------------- #

box_plot_alphas(dados)
# box_plot(dados_finais)
#
# calculate_ci(gap_grasp, 'GRASP', nomes)
# calculate_ci(gap_ga, 'ALGORITMO GENÉTICO', nomes)


# Parâmetros Algoritmo Genético: Elitismo = 0.15, Mutação = 0.5, População = 500 * numClientes, numGerações = 400
# Parâmetros GRASP: alpha = 0.125 e 1000 iterações

# -------------------------------------------------------------------------------------------------------------------- #

def plot_graphic(rt_3opt, rt_grasp, instancias):

    # Número de instâncias
    n = len(instancias)

    # Posições das instâncias no eixo X
    ind = np.arange(n)

    # Criação do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Criando as barras para as heurísticas
    bar_width = 0.3  # Ajuste a largura para compensar a remoção de uma barra
    ax.set_yscale('log')

    # Ajustar as posições para garantir que as barras fiquem alinhadas e com o mesmo espaçamento
    ax.bar(ind - bar_width / 2, rt_3opt, bar_width, label='GRASP', color='#00008B')
    ax.bar(ind + bar_width / 2, rt_grasp, bar_width, label='ALGORITMO GENÉTICO', color='#A9A9A9')

    # Adicionando rótulos, título e legendas
    ax.set_xlabel('Instâncias')
    ax.set_ylabel('Tempo de Execução (segundos)')
    ax.set_title('Tempo de Execução')
    ax.set_xticks(ind)
    ax.set_xticklabels(instancias, rotation=45, ha='right')
    ax.legend()

    # Exibindo o gráfico
    plt.tight_layout()  # Ajusta o layout para não cortar nada
    plt.show()


rt_grasp = [
   	 12.71853050001664,
     10.440400799998315,
   	 10.111785500019323,
  	 17.448773500014795,
     25.109241900005145,
   	 37.774260600010166,
   	 29.935412200022256,
   	 24.328383999993093,
  	 34.19190879998496,
     52.071103099995526,
	 14.828891700017266,
 	 22.89166799999657,
     21.833320700010518,
   	 36.27300149999792,
     33.95083079999313,
     37.72475259998464,
     44.25948779997998,
   	 633.0470682000159,
     158.84882590000052,
   	 808.1047453999927,
     0.45752989998436533,
     10.535510100016836,
     13.213724000001093,
     17.13320520002162,
     1.005043500015745,
 	 20.625403599988203,
   	 8.216891999996733,
    1901.5891256000032,
   	 58.455171999987215,
   	 74.61517070000991
]

rt_ga = [
    140.09311149999849,
   	150.86247939999885,
   	199.2155638999975,
    282.1814662999968,
   	560.1667337000035 ,
    583.4316666000013 ,
   	641.5851488999979 ,
  	678.6177383999966 ,
  	750.6723706999983 ,
    1217.8639638000022,
    208.2219236000019 ,
   	265.41959560000396 ,
    387.4981053000083 ,
  	463.60355659999186 ,
   	686.2484487000038 ,
    735.2273541999893 ,
    1018.8044108000031,
   	734.6019019000087 ,
    1956.629002799993,
    2669.6177864000056 ,
    43.20759959999123 ,
    45.87569309999526 ,
    50.34523479999916 ,
  	55.14470029999211,
    60.14617659999931,
    220.82874250000168,
    426.73609189999115,
   	1719.7514333 ,
    2390.7562125999975,
    2518.1706990999955,
]


plot_graphic(rt_grasp, rt_ga, nomes)
