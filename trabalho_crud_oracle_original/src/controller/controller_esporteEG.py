from model.esporteEG import EsporteEG
from conexion.oracle_queries import OracleQueries

class Controller_EsporteEG:
    def __init__(self):
        pass

    def inserir_esporte(self) -> EsporteEG:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        self.listar_esportes(oracle, need_connect=True)
        id_esporte = input("id do esporte (NOVO): ")

        # Verifica se o esporte existe na base de dados
        if self.verifica_existencia_esporte(oracle, id_esporte):
            nome = input("nome do esporte (novo): ")
            coordenador = input("nome do coordenador: ")

            oracle.write(f"insert into EsporteEG values ('{id_esporte}', '{nome}', '{coordenador}')")
            
            # Persiste (confirma) as alterações
            oracle.conn.commit()

            # Recupera os dados do novo esporte criado transformando em um DataFrame
            df_esporte = oracle.sqlToDataFrame(f"select id_esporte, nome, coordenador from EsporteEG where id_esporte = '{id_esporte}'")

            # Cria um novo objeto EsporteEG
            novo_esporte = EsporteEG(id_esporte, df_esporte.nome.values[0], df_esporte.coordenador.values[0])

            # Exibe os atributos do novo esporte
            print("")
            print(novo_esporte.to_string())
            
            # Retorna o objeto novo_esporte para utilização posterior, caso necessário
            return novo_esporte

        else:
            print(f"O esporte de id {id_esporte} já está cadastrado")
            return None


    def atualizar_esporte(self) -> EsporteEG:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        self.listar_esportes(oracle, need_connect=True)
        id_esporte = input("Id do esporte que deseja atualizar os dados: ")

        # Verifica se o esporte existe na base de dados
        if not self.verifica_existencia_esporte(oracle, id_esporte):
            # solicita a nova descriçao do esporte
            novo_nome_esporte = input("Novo nome do Esporte: ")
            novo_nome_coordenador = input("Novo nome do coordenador: ")

            # Atualiza o nome do esporte existente
            oracle.write(f"update EsporteEG set nome = '{novo_nome_esporte}' where id_esporte = '{id_esporte}' ")

            # Atualiza o coordenador do esporte existente
            oracle.write(f"update EsporteEG set coordenador = '{novo_nome_coordenador}' where id_esporte = '{id_esporte}' ")

            # Recupera os dados do novo esporte criado transformando em um DataFrame
            df_esporte = oracle.sqlToDataFrame(f"select id_esporte, nome, coordenador from EsporteEG where id_esporte = {id_esporte}")

            # Cria um novo obejto esporte
            esporte_atualizado = EsporteEG(id_esporte, df_esporte.nome.values[0], df_esporte.coordenador.values[0])

            # Exibe os atributos do novo esporte
            print(esporte_atualizado.to_string())
            # Retorna o objeto esporte_atualizado para utilização posterior, caso necessário
            return esporte_atualizado
        else:
            print(f"O id_esporte {id_esporte} não existe.")
            return None


    def excluir_esporte(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        self.listar_esportes(oracle, need_connect=True)
        id_esporte = input("Id do esporte que deseja excluir: ")

        # Verifica se o esporte existe na base de dados
        if not self.verifica_existencia_esporte(oracle, id_esporte):

            # Recupera os dados do novo esporte criado transformando em um DataFrame
            df_esporte = oracle.sqlToDataFrame(f"select id_esporte, nome, coordenador from EsporteEG where id_esporte = {id_esporte}")

            opcao_excluir = input(f"Tem certeza que deseja excluir o esporte {df_esporte.nome.values[0]} [S ou N]: ")

            if opcao_excluir in "Ss":
                # Pede uma confirmação ao usuário
                print("Atenção, caso o esporte possua professores ou alunos vinculados, também serão excluídos")
                opcao_excluir = input(f"Tem certeza que deseja excluir o esporte {df_esporte.nome.values[0]} [S ou N]: ")

                if opcao_excluir in "Ss":

                    # Remove o esporte da tabela e as entidades que possuem alguma referência com o esporte
                    oracle.write(f"delete from AlunosEG where id_esporte = {id_esporte}")
                    oracle.write(f"delete from ProfessoresEG where id_esporte = {id_esporte}")
                    oracle.write(f"delete from EsporteEG where id_esporte = {id_esporte}")

                    # Cria um novo obejto esporte exlcuido
                    esporte_excluido = EsporteEG(id_esporte, df_esporte.nome.values[0], df_esporte.coordenador.values[0])

                    # Exibe os atributos do esporte excluido
                    print(esporte_excluido.to_string())
        else:
            print(f"O id_esporte {id_esporte} não existe.")

    def listar_esportes(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
            select id_esporte, nome, coordenador from esporteEG
        """
        if need_connect:
            oracle.connect()
            print(oracle.sqlToDataFrame(query))
            print("")

    def verifica_existencia_esporte(self, oracle:OracleQueries, id_esporte:int=None) -> bool:
        # Recupera os dados do novo esporte criado transformando em um DataFrame
        df_esporte = oracle.sqlToDataFrame(f"select id_esporte, nome from EsporteEG where id_esporte = {id_esporte}")
        return df_esporte.empty