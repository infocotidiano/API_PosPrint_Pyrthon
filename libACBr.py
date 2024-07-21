import ctypes
import json
import os
import sys
from ctypes import CDLL, POINTER, byref, c_bool, c_char_p, c_int, create_string_buffer, c_ulong

# Obtem a pasta do projeto
diretorio_script = os.path.dirname(os.path.abspath(__file__))

#Constantes de Configuração
#DLL ACBrLibSAT utilizada neste projeto é 64 ST (Single Thread)
PATH_DLL                = os.path.abspath(os.path.join(diretorio_script,r"ACBrLib/x64/ACBrPosPrinter64.dll"))
PATH_ACBRLIB            = os.path.abspath(os.path.join(diretorio_script, "ACBrLib.INI"))
PATH_LOG                = os.path.abspath(os.path.join(diretorio_script, "Log"))

#função para limpar a tela
def limpar_tela():
    if os.name == 'nt':  
        os.system('cls')
    else:
        os.system('clear')

#Validar se json 
def validar_json(json_str):
    try:
        json.loads(json_str)
        return True
    except json.decoder.JSONDecodeError:
        return False

#Cria a pasta log se nao existir
if not os.path.exists(PATH_LOG):
   os.makedirs(PATH_LOG) 

#Verifica se a dll está no path indicado
if not os.path.exists(PATH_DLL):
   print(f"O arquivo '{PATH_DLL}' não existe.")
   sys.exit(1)
    
#função para definir o novo temanho da resposta
def define_bufferResposta(novo_tamanho):
    global tamanho_inicial, esTamanho, sResposta
    tamanho_inicial = novo_tamanho
    esTamanho = ctypes.c_ulong(tamanho_inicial)
    sResposta = ctypes.create_string_buffer(tamanho_inicial)
    return tamanho_inicial, esTamanho, sResposta 

#tratar uma sequencia de bytes     
def TrataRespostaLerValor(AResposta):
    return AResposta.decode('utf-8').strip('\x00 ')

#define o tamanho de retorno do ler valor       
def DefineTamanhoLerValor(ANovoTamanho):
    global RespostaLerValor
    RespostaLerValor = ' ' * ANovoTamanho
    RespostaLerValor = RespostaLerValor.encode("utf-8")
    return RespostaLerValor
    

#Criando o ponteiro pra ser utilizado em MT
ponteiro = c_int()
ponteiro = POINTER(c_int)()

# Carregar a DLL, ajustes os paths para seu ambiente.
acbr_lib = ctypes.CDLL(PATH_DLL)

# Verificação de tipo para Inicializar 
acbr_lib.POS_Inicializar.argtypes = POINTER(POINTER(c_int)), c_char_p, c_char_p
acbr_lib.POS_Inicializar.restype = c_int


resposta = acbr_lib.POS_Inicializar(ponteiro, PATH_ACBRLIB.encode("utf-8"),"".encode("utf-8"))
if resposta != 0:
    print('Erro ao Inicializar ')
    sys.exit(1)

#configurando tipo de resposta retorno 
acbr_lib.POS_ConfigGravarValor(ponteiro,"Principal".encode("utf-8"), "TipoResposta".encode("utf-8"), str(2).encode("utf-8"))

#Configurando o log da Biblioteca
acbr_lib.POS_ConfigGravarValor(ponteiro,"Principal".encode("utf-8"), "LogNivel".encode("utf-8"), str(4).encode("utf-8"))
acbr_lib.POS_ConfigGravarValor(ponteiro,"Principal".encode("utf-8"), "LogPath".encode("utf-8"), PATH_LOG.encode("utf-8"))

#Carrega informação de porta e modelo apenas para exibir nas configurações
def CarregaConfiguracao():
    global LModelo, LPorta
    define_bufferResposta(10)
    DefineTamanhoLerValor(10)
    resultado = acbr_lib.POS_ConfigLerValor(ponteiro,"PosPrinter".encode("utf-8"), "Modelo".encode("utf-8"), RespostaLerValor, ctypes.byref(esTamanho))
    if resultado == 0:
       LModelo = TrataRespostaLerValor(RespostaLerValor);
    else: 
        print('Erro ao lerValor Modelo',resultado)    

    define_bufferResposta(100)
    DefineTamanhoLerValor(100)
    resultado = acbr_lib.POS_ConfigLerValor(ponteiro,"PosPrinter".encode("utf-8"), "Porta".encode("utf-8"), RespostaLerValor, ctypes.byref(esTamanho))
    if resultado == 0:
       LPorta = TrataRespostaLerValor(RespostaLerValor);
    else: 
        print('Erro ao lerValor Porta',resultado)   
    return LModelo, LPorta

#Função para Configuração de porta.
def configPorta():
    limpar_tela()
    LModelo, LPorta = CarregaConfiguracao()
    print(LPorta)
    print('''
    --------------------------------------------------------------------------
    EXEMPLO: ACBrLib para Impressora de Cupom
    ----------------------------- Configuração -------------------------------
    
    Exemplos: Com1, LPT1, USB, raw:i9
    
    '''
    )
    LPorta   = str(input(f'Digite a Porta (Porta Atual = {LPorta}) :'))
    #Gravar as informações no arquivo ACBrLib
    acbr_lib.POS_ConfigGravarValor(ponteiro,"PosPrinter".encode("utf-8"), "Porta".encode("utf-8"), LPorta.encode("utf-8"))
    

#função para configurar modelo
def configModelo():
    limpar_tela()
    LModelo, LPorta = CarregaConfiguracao()
    print(
    '''
    --------------------------------------------------------------------------
    EXEMPLO: ACBrLib para Impressora CUPOM | Configura PORTA
    ----------------------------- Configuração -------------------------------
    '''
    )
    print(
    '''
    Modelos disponíveis :
    0 = ppTexto (Padrão)	4 = ppEscVox		 8 = ppEscPosStar
    1 = ppEscPosEpson		5 = ppEscDiebold	 9 = ppEscZJiang
    2 = ppEscBematec		6 = ppEscEpsonP2	10 = ppEscGPrinter
    3 = ppEscDaruma			7 = ppCustomPos		11 = ppEscDatecs

    '''
    )
    LModelo = str(input(f'Digite o código do Modelo (Modelo Atual = {LModelo}):'))
    acbr_lib.POS_ConfigGravarValor(ponteiro,"PosPrinter".encode("utf-8"), "Modelo".encode("utf-8"), LModelo.encode("utf-8"))
    
