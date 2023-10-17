from conexion.oracle_queries import OracleQueries
from controller.controller_esporteEG import Controller_EsporteEG
from model.esporteEG import EsporteEG
from model.professoresEG import ProfessoresEG

class Controller_ProfessorEG:
    def __init__(self):
        self.ctrl_esporte = Controller_EsporteEG()

    def inserir_professor(self) -> ProfessoresEG:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect() 
        
        # Solicita ao usuário o id_professor que deseja inserir
        self.listar_professores(oracle, need_connect=True)
        id_professor = int(input("Digite o id_professor (NOVO): "))

        if self.verifica_existencia_professor(oracle, id_professor):
            # Solicita ao usuário os dados para preencher o novo professor
            nome = input("Nome do professor (NOVO): ")
            qtde_turmas = int(input("Quantidade de turmas do professor (NOVO): "))


            # Lista os esportes cadastrados
            self.ctrl_esporte.listar_esportes(oracle, need_connect=True)

            id_esporte = int(input("id_esporte que o professor da aula: "))

            esporte = self.valida_esporte(oracle, id_esporte)
            if esporte == None:
                return None

            oracle.write(f"insert into professoresEG values ({id_professor}, '{nome}', '{qtde_turmas}', {esporte.get_id_esporte()})")
            # Persiste (confirma) as alterações
            oracle.conn.commit()

            # Recupera os dados do novo Professor criando transformando em um DataFrame
            df_professor = oracle.sqlToDataFrame(f"select id_professor, nome, qtde_turmas, id_esporte from professoresEG where id_professor = {id_professor}")
            
            # Cria um novo objeto Professor
            novo_professor = ProfessoresEG(df_professor.id_professor.values[0], df_professor.nome.values[0], df_professor.qtde_turmas.values[0], esporte)

            # Exibe os atributos do Professor
            print(novo_professor.to_string())
            # Retorna o objeto novo_professor para utilização posterior, caso necessário
            return novo_professor
        else:
            print(f"Professor com id_professor = {id_professor} já cadastrado!")


    def atualiza_professor(self) -> ProfessoresEG:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o id_professor do professor a ser atualizado
        self.listar_professores(oracle, need_connect=True)
        id_professor = int(input("id do professor que deseja alterar os dados: "))

        # Verifica a existencia do professor no banco
        if not self.verifica_existencia_professor(oracle, id_professor):
            # Solicita ao usuário os novos dados do professor
            nome = input("Nome do professor (NOVO): ")
            qtde_turmas = int(input("Quantidade de turmas do professor: "))
            id_esporte = int(input("Id do esporte que o professor da aula: "))

            # faz a validação para ver se o esporte existe na base de dados
            esporte = self.valida_esporte(oracle, id_esporte)
            if esporte == None:
                return None
            
            oracle.write(f"update professoresEG set nome = '{nome}', qtde_turmas = {qtde_turmas}, id_esporte = {esporte.get_id_esporte()} where id_professor = {id_professor}")

            # Recupera os dados do novo professor criado transformando em um DataFrame
            df_professor = oracle.sqlToDataFrame(f"select id_professor, nome, qtde_turmas, id_esporte from professoresEG where id_professor = {id_professor}")

            # Cria um novo objeto ProfessoresEG
            professor_atualizado = ProfessoresEG(df_professor.id_professor.values[0], df_professor.nome.values[0], df_professor.qtde_turmas.values[0], esporte)

            # Exibe os dados do professor atualizado
            print(professor_atualizado.to_string())
            return professor_atualizado
        
        else: 
            print(f"O professor de id = {id_professor} não existe no banco! ")
            return None


    def excluir_professor(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o id_professor que deseja excluir
        self.listar_professores(oracle, need_connect=True)
        id_professor = int(input("Id do professor que deseja excluir: "))

        # Verifica a existencia do professor
        if not self.verifica_existencia_professor(oracle, id_professor):
            # Recupera os dados do professor transformando em um DataFrame
            df_professor = oracle.sqlToDataFrame(f"select id_professor, nome, qtde_turmas, id_esporte from professoresEG where id_professor = {id_professor}")

            # Valida id_esporte
            esporte = self.valida_esporte(oracle, df_professor.id_esporte.values[0])

            opcao_excluir = input(f"Tem certeza que deseja excluir o professor {df_professor.nome.values[0]} [S ou N]: ")

            if opcao_excluir in "Ss":
                # Remove o professor da tabela
                oracle.write(f"delete from professoresEG where id_professor = {id_professor}")

                # faz a validação para ver se o esporte existe na base de dados
                esporte = self.valida_esporte(oracle, int(df_professor.id_esporte.values[0]))
                if esporte == None:
                    return None
                
                # Cria um novo objeto ProfessoresEG
                professor_excluido = ProfessoresEG(df_professor.id_professor.values[0], df_professor.nome.values[0], df_professor.qtde_turmas.values[0], esporte)

                print("Professor removido! ")
                print(professor_excluido.to_string())
        
        else:
            print(f"O professor de id = {id_professor} não está na base de dados ")





    def listar_professores(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
            select id_professor, nome, qtde_turmas, id_esporte from professoresEG
        """
        if need_connect:
            oracle.connect()
            print(oracle.sqlToDataFrame(query))
            print("")


    def valida_esporte(self, oracle: OracleQueries, id_esporte:int=None) -> EsporteEG:
        if self.ctrl_esporte.verifica_existencia_esporte(oracle, id_esporte):
            print(f"O esporte {id_esporte} informado não existe na base de dados")
            return None
        else: 
            oracle.connect()
            # recupera os dados do esporte transformando em um dataFrame
            df_esporte = oracle.sqlToDataFrame(f"select id_esporte, nome, coordenador from esporteEG where id_esporte = {id_esporte}")

            # Cria um novo objeto EsporteEG
            esporte = EsporteEG(df_esporte.id_esporte.values[0], df_esporte.nome.values[0], df_esporte.coordenador.values[0])
            return esporte


    def verifica_existencia_professor(self, oracle: OracleQueries, id_professor:int=None) -> bool:
        # Recupera os dados do professor transformando em um DataFrame
        df_professor = oracle.sqlToDataFrame(f"select id_professor, nome from professoresEG where id_professor = {id_professor}")
        return df_professor.empty