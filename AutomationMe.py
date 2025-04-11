#Automação de encaminhamento de orçamentos
from datetime import datetime
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from DistanceCalculator import DistanceCalculator
from selenium.webdriver.common.keys import Keys

#constantes para teste
email="contato@bandamoderatto.com.br"
senha="raulseixas423123"
site = "https://app3.meeventos.com.br/bandamoderatto"
meu_local = "São Miguel do Iguaçu"
v_km_rodado = 7

class AutomationMe:

    def __init__(self, email, senha, site):
        self.email = email
        self.senha = senha
    #abre o site para automação
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        service = None

        try:
            service = Service(ChromeDriverManager().install())
        except:
            print("Você está sem conexão com internet")
            exit()


        self.nav = webdriver.Chrome(options=options, service=service)
        self.nav.get(site)
        self.nav.maximize_window()
        time.sleep(3)




    #efetua o login com e-mail e senha e cliacando para o login
    def login(self):
        self.nav.find_element('xpath', '//*[@id="email"]').send_keys(email)
        self.nav.find_element('xpath', '//*[@id="password"]').send_keys(senha)
        self.nav.find_element('xpath', '//*[@id="login"]').click()


    def novo_orcamento(self, tipo_evento, data, cliente, telefone, email, local, servicos):

        self.nav.find_element('xpath', '//*[@id="element2"]/div[1]/button').click()
        time.sleep(1)
        #novo orçamento
        self.nav.find_element('xpath', '//*[@id="element2"]/div[1]/ul/li[1]/a').click()
        time.sleep(1)

        if data != "":
            # inserir data
            self.nav.find_element('xpath','//*[@id="eventoverifica"]').click()
            self.nav.find_element('xpath', '//*[@id="eventoverifica"]').send_keys(data)
            self.nav.find_element('xpath','// *[ @ id = "formmodelo1"] / div / div[1] / h4').click()

            time.sleep(1)

            #verifica disponibilidade
            if self.nav.find_element('xpath', '//*[@id="retornoeventos"]/div[1]/div/div').get_dom_attribute('class') != "alert alert-success mb-0":
                self.nav.close()
                return "Data indisponível"

        else:
            self.nav.find_element('xpath', '// *[ @ id = "datanaodefinidack"]').click()


        # inserir local
        self.nav.find_element('xpath', '//*[@id="s2id_select-basicwhats"]/a/span[2]/b').click()
        self.nav.find_element('xpath', '//*[@id="select2-drop"]/ul/li[2]/div').click()
        self.nav.find_element('xpath', '//*[@id="localdoevento"]').send_keys(local)

        time.sleep(1)


        #selecionar e-mail e telefone e insere

        if email == "":
            self.nav.find_element('xpath','//*[@id="formmodelo1"]/div/div[2]/div/div[7]/div/div/div[1]').click()
        else:
            self.nav.find_element('xpath', '//*[@id="emailinicial"]').send_keys(email)
            time.sleep(1)
            try:
                select_element = self.nav.find_element('xpath', '// *[ @ id = "cadastrocliente"] / div / div / select')
                select = Select(select_element)
                select.select_by_visible_text("Não")
            except:
                pass


        time.sleep(1)

        if telefone != "":
            self.nav.find_element('xpath', '// *[ @ id = "envio-whatsapp"]').click()
            self.nav.find_element('xpath', '// *[ @ id = "telefone2"]').clear()
            self.nav.find_element('xpath','// *[ @ id = "telefone2"]').send_keys(telefone)

        time.sleep(2)

        #inserir nome cliente
        self.nav.find_element('xpath', '//*[@id="nomeinicial"]').clear()
        self.nav.find_element('xpath', '//*[@id="nomeinicial"]').clear()
        time.sleep(2)
        self.nav.find_element('xpath', '//*[@id="nomeinicial"]').send_keys(cliente)

        #selecionar tipo orçamento @@@@@@@@@@@@@@@
        self.nav.find_element('class name','col-sm-8').click()
        self.nav.find_element('xpath', '//*[@id="select2-drop"]/ul/li[2]/div').click()

        #continuar
        self.nav.find_element('xpath', '//*[@id="continuar"]').click()

        #nova janela

        #mudar Modelo de Orçamento
        self.nav.find_element('xpath','// *[ @ id = "modelopdf"] / option[2]').click()

       #mudar tipo de Evento
        select_element = self.nav.find_element('xpath', '//*[@id="tipodoevento"]')
        select = Select(select_element)
        select.select_by_visible_text(tipo_evento)

        #adicionar serviços
        self.nav.find_element('xpath','// *[ @ id = "produto"]').click()


        for servico in servicos:
            time.sleep(2)
            self.nav.find_element('xpath', '//*[@id="jq-datatables-example_filter"]/label/input').send_keys(servico)
            time.sleep(2)
            self.nav.find_element('xpath', '// *[ @ id = "jq-datatables-example"] / tbody / tr[1] / td[1] / button').click()
            self.nav.find_element('xpath', '//*[@id="jq-datatables-example_filter"]/label/input').clear()


        if meu_local not in local:
            #calculo custo logística
            dis = DistanceCalculator()
            distancia_total  = int(2 * dis.get_distance(meu_local, local))
            dis.destroy()
            #inserir valor de logistica
            if distancia_total > 150:
                #abre um serviço avulso
                self.nav.find_element('xpath','// *[ @ id = "avulso"]').click()
                time.sleep(1)
                #insere nome do serviço avulso
                self.nav.find_element('xpath','/ html / body / div[7] / div / div / div[2] / div / form / input').send_keys(f"Despesas de Logística {distancia_total} KM")
                self.nav.find_element('xpath', '/ html / body / div[7] / div / div / div[3] / button[2]').click()
                time.sleep(2)
                #inserir valor de logística
                valor_logistica = v_km_rodado * distancia_total
                t = len(servicos) + 1
                self.nav.find_element('xpath', f'/html/body/div[2]/div[4]/div[2]/div[2]/div/div[2]/div[1]/div[{t}]/div/div[2]/input').send_keys(valor_logistica*100)
                #click aleatório para carregar valor de logística
                self.nav.find_element('xpath', '// *[ @ id = "produto"]').click()

        time.sleep(1)

        #botão para enviar os dados do orçamento
        self.nav.find_element('xpath', '// *[ @ id = "enviardados"]').click()
        time.sleep(3)
        #botão encerrar o orçamento

        self.nav.find_element('xpath', '//*[@id="continuar"]').click()
        #retorna link com a proposta
        time.sleep(3)
        link = self.nav.find_element('xpath', '//*[@id="linkproposta"]').get_attribute("value")
        #fecha o navegador
        self.nav.close()

        return link


    def verifica_disponibilidade(self, data):

        self.nav.find_element('xpath', '//*[@id="element2"]/div[1]/button').click()
        time.sleep(1)
        # novo orçamento
        self.nav.find_element('xpath', '//*[@id="element2"]/div[1]/ul/li[1]/a').click()
        time.sleep(1)

        if AutomationMe._is_valid_date(data):
            # inserir data
            self.nav.find_element('xpath', '//*[@id="eventoverifica"]').click()
            self.nav.find_element('xpath', '//*[@id="eventoverifica"]').send_keys(data)
            self.nav.find_element('xpath', '// *[ @ id = "formmodelo1"] / div / div[1] / h4').click()

            time.sleep(1)

            # verifica disponibilidade
            if self.nav.find_element('xpath', '//*[@id="retornoeventos"]/div[1]/div/div').get_dom_attribute('class') != "alert alert-success mb-0":
                self.nav.close()
                return "Data indisponível"
            else:
                self.nav.close()
                return "Data disponível"

        else: return "Data Inválida"

    def efetuarReserva(self, data, nome, telefone):
        date = data

        #valida data se esta no formato correto ou se a data não é passada
        if AutomationMe._is_valid_date(date):
            self.nav.find_element('xpath', '//*[@id="main-menu-inner"]/ul/li[11]').click()
            time.sleep(1)
            self.nav.find_element('xpath', '//*[@id="main-menu-inner"]/ul/li[11]/ul/li[2]/a').click()
            #busca orçamento pelo numero de telefone
            self.nav.find_element('xpath', '// *[ @ id = "buscanalista"]').send_keys(telefone)
            time.sleep(3)

            #tenta acessar orçamentos com o telefone, caso contrário não há orçamentos.
            try:
                #carrega lista de orçamentos com o mesmo telefone
                orcamentos = self.nav.find_elements('tag name', 'tr')

                d = None
                #acessa cada orçamento
                for i  in range(len(orcamentos) - 1):
                    elemento = self.nav.find_element('xpath',f'//*[@id="carregalista"]/div[1]/div/table/tbody/tr[{i+1}]/td[4]')
                    dt = elemento.text[:10]
                    n = self.nav.find_element('xpath',f'//*[@id="carregalista"]/div[1]/div/table/tbody/tr[{i + 1}]/td[3]').text.splitlines()[0]
                    #verifica se o orçamento possui o mesmo nome e data, ou se a data está como indefinida
                    if (n == nome and (dt == data or dt == 'Data Não D')):

                        #clica no orçamento para abrir nova página
                        self.nav.find_element('xpath',f'// *[ @ id = "carregalista"] / div[1] / div / table / tbody / tr[{i+1}] / td[2] / a').click()
                        d = dt
                        print(d)
                        break

                #se a data esta indefinida é inserida a nova data
                if d == 'Data Não D':
                    self.nav.find_element('xpath','// *[ @ id = "dadosdaproposta"] / div[1] / a / button').click()
                    time.sleep(2)
                    self.nav.find_element('xpath','// *[ @ id = "data-0"] / button').click()
                    time.sleep(2)
                    self.nav.find_element('xpath', '// *[ @ id = "dataNaoDefinidaEditar"]').click()
                    self.nav.find_element('xpath','// *[ @ id = "eventoverifica-grupo"]').send_keys(date)
                    self.nav.find_element('xpath', '// *[ @ id = "informarlocal"] / label').click()

                    self.nav.find_element('xpath', '// *[ @ id = "atualizarData"] / div[3] / button[2]').click()
                    time.sleep(2)
                    self.nav.find_element('xpath', '// *[ @ id = "continuar"]').click()

                #acessar
                time.sleep(3)
                self.nav.find_element('xpath','// *[ @ id = "content-wrapper"] / div[2] / div / div[1] / button[1]').click()
                time.sleep(2)
                self.nav.find_element('xpath','//*[@id="myModalConcluirVenda"]/div/div/form/div[2]/button').click()
                time.sleep(3)
                self.nav.find_element('xpath','// *[ @ id = "content-wrapper"] / button').click()
                time.sleep(1)
                self.nav.find_element('xpath','// *[ @ id = "btnformwhatsapp2"]').click()
                time.sleep(1)
                #desmarca opções de formulário
                self.nav.find_element('xpath', '//*[@id="formmsgwhats"]/input[5]').click()
                self.nav.find_element('xpath', ' // *[ @ id = "formmsgwhats"] / input[6]').click()
                #gera formulário
                self.nav.find_element('xpath', '// *[ @ id = "formmsgwhats"] / center / button').click()
                time.sleep(5)

                #localiza o link do formulário e envia
                link = self.nav.find_element('xpath', '//*[@id="carregamentointerno"]/div[2]/input').get_attribute('value')
                self.nav.close()
                return link

            #foi tentado carregar lista de orçamentos, mas não foi encontranto
            except NoSuchElementException:
                self.nav.close()
                return "Orçamento não localizado - Pode ser que seu orçamento tenha expirado, por favor solicite novo orçamento!"

        #retorno caso a data esteja no formato incorreto ou já tenha passado
        self.nav.close()
        return "Data inválida"


    def insert_information(self, data, informacao):
        if not AutomationMe._is_valid_date(data):
            return "Data Inválida"

        self.nav.find_element('xpath', '//*[@id="element3"]').click()
        time.sleep(1)
        self.nav.find_element('xpath', '// *[ @ id = "element3"] / ul / li[1] / a').click()
        time.sleep(3)
        paginas = self.nav.find_elements('class name', 'paginacao')

        for s in range(2, len(paginas) + 1):
<<<<<<< HEAD

=======
            print(s)
>>>>>>> e63fb76eddb842d7fb413f0a839108f4ca7c3624
            try:
                datas = self.nav.find_elements('tag name', 'tr')
                for i in range(len(datas) - 1):
                    elemento = self.nav.find_element('xpath', f'//*[@id="carregalista"]/div[1]/div/table/tbody/tr[{i+1}]/td[1]/a')
                    dt = elemento.text[:10]
<<<<<<< HEAD
=======
                    print(dt)
>>>>>>> e63fb76eddb842d7fb413f0a839108f4ca7c3624

                    if dt == data:

                        elemento.click()
                        time.sleep(3)
                        self.nav.find_element('xpath','// *[ @ id = "informacoesgerais"] / div / div / div').click()
                        time.sleep(4)
                        self.nav.find_element('xpath','//*[@id="cke_editor"]').click()
                        time.sleep(3)

                        self.nav.switch_to.frame(self.nav.find_element('xpath','//*[@id="cke_1_contents"]/iframe'))
                        self.nav.find_element('xpath', '/html/body').send_keys("\n" + informacao)
                        self.nav.switch_to.default_content()
                        time.sleep(3)
                        self.nav.find_element('xpath','// *[ @ id = "carregamentointerno"] / form / div[2] / button').click()
                        time.sleep(3)
                        self.nav.close()
                        return "Informações Cadastradas"


            except NoSuchElementException:
                self.nav.close()
                return "Evento não localizado"

            self.nav.find_element('xpath', f'//*[@id="carregalista"]/div[2]/ul/li[{s + 1}]/a').click()
            time.sleep(3)

        self.nav.close()
        return "Evento não localizado"

    def anexar_arquivo(self, data, arquivo):
        if not AutomationMe._is_valid_date(data):
            return "Data Inválida"

        self.nav.find_element('xpath', '//*[@id="element3"]').click()
        time.sleep(1)
        self.nav.find_element('xpath', '// *[ @ id = "element3"] / ul / li[1] / a').click()
        time.sleep(3)
        paginas = self.nav.find_elements('class name', 'paginacao')

        for s in range(2, len(paginas) + 1):
            print(s)
            try:
                datas = self.nav.find_elements('tag name', 'tr')
                for i in range(len(datas) - 1):
                    elemento = self.nav.find_element('xpath', f'//*[@id="carregalista"]/div[1]/div/table/tbody/tr[{i + 1}]/td[1]/a')
                    dt = elemento.text[:10]
                    print(dt)

                    if dt == data:
                        elemento.click()
                        time.sleep(3)

                        return "Arquivo Anexado"


            except NoSuchElementException:
                self.nav.close()
                return "Evento não localizado"

            self.nav.find_element('xpath', f'//*[@id="carregalista"]/div[2]/ul/li[{s + 1}]/a').click()
            time.sleep(3)

        self.nav.close()
        return "Evento não localizado"


    @staticmethod
    def _is_valid_date(data):

        data_atual = datetime.now()
        try:
            data_evento = datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
           return False

        if data_evento > data_atual:
            return True
        else:
            return False



    #fazer contrato
    
#print(AutomationMe._is_valid_date("asdsafsadf"))
a = AutomationMe(email, senha, site)
a.login()
<<<<<<< HEAD


info = """ENTRADA NOIVO

https://www.youtube.com/watch?v=PYI09PMNazw
Ecstasy of gold

ENTRADA PAIS/PADRINHOS

https://www.youtube.com/watch?v=NlprozGcs80
Pachebel Canon in D

https://www.youtube.com/watch?v=mFWQgxXM_b8
Spring Vivaldi

NOIVA

https://www.youtube.com/watch?v=CsSiy1VgH4Y
"""

print(a.insert_information('12/04/2025', info))

=======
print(a.insert_information('07/03/2026', 'Lady Gaga'))
>>>>>>> e63fb76eddb842d7fb413f0a839108f4ca7c3624
#print(a.novo_orcamento("Empresarial", "", "Jhonatan", "61991480625", "", "Foz do Iguaçu - Paraná", ['Banda completa Corporativo', 'Rider']))
#print(a.efetuarReserva("20/01/2025", "Lucas Comin", "45 98412-4576"))


